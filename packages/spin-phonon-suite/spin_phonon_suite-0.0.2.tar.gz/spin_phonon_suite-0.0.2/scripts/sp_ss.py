#!/usr/bin/env python3

import numpy as np
import numpy.linalg as LA
import sys
import argparse
import os
import spglib
from phonopy import Phonopy
from phonopy.file_IO import parse_FORCE_SETS
from phonopy.structure.cells import get_cell_parameters
from phonopy.interface.vasp import read_vasp
from phonopy.harmonic.dynmat_to_fc import DynmatToForceConstants
from phonopy.api_phonopy import get_dynamical_matrix
from collections import Counter
import xyz_py as xyzp
import molcas_suite.generate_input as msgi
import molcas_suite.generate_job as msgj
import gaussian_suite.gen as ggen
import gaussian_suite.cd_extractor as gcde
import multiprocessing as mp
import copy


def read_user_args():
    '''
    Parse the user-defined options.

    Returns
    -------
        args (object): object containing the user-defined options.

    Raises:
        Error: .

    '''

    description = """
    Program to prepare solid state spin-phonon jobs using VASP data.

    Available sub-programs:
        sp_ss charges ...      # Run first.
        sp_ss equilibrium ...  # Run second.
        sp_ss distorted ...    # Run last.
    """

    epilog = '''
    To display options for a specific program, use sp_ss SUB-PROGRAMNAME -h
    '''

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers()

    # Charges mode
    description_charges = '''

    Prepare Gaussian input files to calculate charges and dipoles of full
    molecules within the central unitcell of the supercell
    '''

    epilog_charges = '''

    Submit individual Gaussian jobs with ./submit_charges_jobs.sh

    The program will generate the following files required by the subsequent\
 "equilibrium" run.
        - An xyz file of the supercell
        - "gaussian_rosetta.dat", with information on translation-related atoms
        - A set of Gaussian log files containing charges and dipoles

    '''
    charges_parser = subparsers.add_parser(
        'charges',
        description=description_charges,
        epilog=epilog_charges,
        formatter_class=argparse.RawDescriptionHelpFormatter
       )

    charges_parser.set_defaults(func=charges_func)

    charges_parser.add_argument(
        'POSCAR_file', type=str, help='VASP file containing the unitcell data.'
       )
    charges_parser.add_argument(
        'FORCE_SETS', type=str, help='PHONOPY FORCE_SETS file.'
       )
    charges_parser.add_argument(
        'force_expansion', type=int, nargs=3,
        help='Supercell expansion used to obtain the force constants in \
              Phonopy, e.g. 1 1 1.'
       )
    charges_parser.add_argument(
        'molecules', type=str, nargs='+',
        help='Chemical formula, charge, and spin multiplicity of each \
              molecule present in the unit cell\
              Example: YC34H58 1 1 BC24F20 -1 1 H20 0 1'
       )
    charges_parser.add_argument(
        '--dim', type=int, nargs=3,
        help='Supercell expansion, e.g. 3 3 3. If absent, the lattice vectors\
              are used to guess an isotropic expansion.'
       )
    charges_parser.add_argument(
        '--functional', type=str, default='pbe', metavar='<option>',
        choices=['pbe', 'pbe0', 'b3lyp', ],
        help='DFT functional. \
              Options: pbe, pbe0, b3lyp. Default: pbe.'
       )
    charges_parser.add_argument(
        '--basis_set', type=str, default='cc-pVTZ', metavar='<option>',
        choices=['cc-pVTZ', 'cc-pVDZ', "cc-pVQZ"],
        help='Basis set for all atoms. Default: cc-pVTZ.'
       )

    # EQUILIBRIUM mode
    description_equilibrium = '''

    Prepare OpenMolcas equilibrium input file.
    Run after "charges".
    '''

    equilibrium_parser = subparsers.add_parser(
        'equilibrium',
        description=description_equilibrium,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    equilibrium_parser.set_defaults(func=equilibrium_func)

    equilibrium_parser.add_argument(
        'supercell',
        type=str,
        help='File containing the supercell xyz coordinates,\
              generated with "charges" mode.'
    )
    equilibrium_parser.add_argument(
        'symbol',
        type=str,
        nargs=2,
        help='Atomic symbols identifying the metal centers in Gaussian and\
              Molcas jobs, respectively.'
    )
    equilibrium_parser.add_argument(
        'charge',
        type=int,
        help='Charge of the metal-containing molecule'
    )
    equilibrium_parser.add_argument(
        'n_active_elec',
        type=int,
        help='Number of active electrons'
    )
    equilibrium_parser.add_argument(
        'n_active_orb',
        type=int,
        help='Number of active orbitals'
    )
    equilibrium_parser.add_argument(
        'n_coord_atoms',
        type=int,
        help='Number of atoms coordinated to central atom'
    )
    equilibrium_parser.add_argument(
        '--gaussian_rosetta',
        type=str,
        default='gaussian_rosetta.dat',
        help='Output file created with "charges" mode. \
            Default: gaussian_rosetta.dat.',
        metavar="<file_name>"
    )
    # DISTORT mode
    decription_distort = '''

    Prepare OpenMolcas distorted input files.
    Run after "equilibrium".
    Note that all Gaussian log files must be present in the current directory.
    '''
    epilog_distort = '''
    OpenMolcas files will be generated in the corresponding subfolder:
        q_point/direction/vib_X/input

    '''

    distort_parser = subparsers.add_parser(
        'distort',
        description=decription_distort,
        epilog=epilog_distort,
        formatter_class=argparse.RawDescriptionHelpFormatter
       )

    distort_parser.set_defaults(func=distort_func)

    distort_parser.add_argument(
        'POSCAR_file', type=str, help='VASP file containing the unitcell data.'
       )
    distort_parser.add_argument(
        'FORCE_SETS', type=str, help='Phonopy FORCE_SETS file.'
       )
    distort_parser.add_argument(
        'force_expansion', type=int, nargs=3,
        help='Supercell expansion used to obtain the force constants in \
              Phonopy, e.g. 1 1 1.'
       )
    distort_parser.add_argument(
        'eq_out', type=str, help='OpenMolcas output file at the equilibrium.'
       )
    distort_parser.add_argument(
        'SUPERCELL', type=int, nargs=3,
        help='Supercell expansion. It MUST match --dim from "charges" mode.'
       )
    distort_parser.add_argument(
        'symbol',
        type=str,
        nargs=2,
        help='Atomic symbols identifying the metal centers in Gaussian and\
              Molcas jobs, respectively.'
    )
    distort_parser.add_argument(
        'charge',
        type=int,
        help='Charge of the metal-containing molecule'
    )
    distort_parser.add_argument(
        'n_active_elec',
        type=int,
        help='Number of active electrons'
    )
    distort_parser.add_argument(
        'n_active_orb',
        type=int,
        help='Number of active orbitals'
    )
    distort_parser.add_argument(
        'n_coord_atoms',
        type=int,
        help='Number of atoms coordinated to central atom'
    )
    distort_parser.add_argument(
        'n_rassi_states',
        type=int,
        help='Number of states in ground spin orbit term'
    )
    distort_parser.add_argument(
        '--inporb', type=str, default=None, metavar='<file>',
        help='Equilibrium RasOrb file. Default: `eq_out`.RasOrb.'
       )
    distort_parser.add_argument(
        '--gaussian_rosetta', type=str, default='gaussian_rosetta.dat',
        metavar='<filename>',
        help='Output file created with "charges" mode. Default: gaussian_rosetta.dat.' # noqa
       )
    distort_parser.add_argument(
        '--phonon_threshold', type=float, default=None, metavar='<value>',
        help='Energy threshold (cm-1) to discard phonons. \
              Default: Total CF splitting + 1%%.'
       )
    distort_parser.add_argument(
       '--n_threads', type=int, default=8, metavar='<value>',
       help='Number of threads used in the CSF queue system. Default: 8.'
      )
    distort_parser.add_argument(
        '--hpc', type=str, default='condor', metavar='<option>',
        choices=['csf', 'condor', 'aws'],
        help='HPC architecture for OpenMolcas distortion calculations \
              Default: condor. \
              Options: [csf, condor, aws]'
       )

    # Hidden argument to actually run program
    # rather than just create job.sh file
    for par in [charges_parser, equilibrium_parser, distort_parser]:
        par.add_argument(
            '--run',
            action='store_true',
            help=argparse.SUPPRESS
        )

    args = parser.parse_args()

    # If arg_list==None, i.e. normal cli usage, parse_args() reads from
    # "sys.argv". The arg_list can be used to call the argparser from the
    # back end
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_args()
    args.func(args)

    return args


def submit_self(script_name, message=""):
    '''
    Write a jobscript to run this program on the CSF

    Parameters
    ----------
        user_args (list): List of command line arguments to this program

    Keyword arguments:
        script_name  (str) : Jobscript file name
        nprocs       (int) : Number of processors

    Returns
    -------
        None
    '''

    # Check if in conda env
    try:
        conda_env = os.environ["CONDA_PREFIX"]
    except KeyError:
        conda_env = ''

    # Create jobscript to run in csf queue
    with open(script_name, 'w') as js:

        js.write("#!/bin/bash --login\n")
        js.write("#$ -S /bin/bash\n")
        js.write("#$ -N {}\n".format(script_name.split('.')[0]))
        js.write("#$ -cwd\n")
        # High mem node since phonopy constructs the lattice as M @ M
        js.write("#$ -l mem256 \n\n")

        js.write("module load tools/env/proxy2\n\n")

        if conda_env:
            js.write("conda activate {}\n\n".format(conda_env))

        js.write("python ")
        for arg in sys.argv:
            js.write("{} ".format(arg))

        # Add --run argument to run program
        js.write("--run\n")

    print()
    os.system('qsub {}'.format(script_name))
    print()

    if message:
        print(message)


def charges_func(user_args):
    """
    Wrapper for charges mode
    """

    if not user_args.run:

        message = "When this job is finished, run "
        message += "\033[0;32m"
        message += "./submit_charges.sh"
        message += "\033[0m"
        message += " to submit the resulting Gaussian jobs \n"
        message += "Gaussian files are located in the "
        message += "\033[0;34m"
        message += "gaussian_charges"
        message += "\033[0m"
        message += " directory"
        submit_self("generate_gauss_charges.sh", message=message)
        exit()

    # Check number of molecules, charges, and spin multiplicities match
    if len(user_args.molecules) % 3:
        exit('\n*** Error ***\n\
                Inconsistent number of \
                molecules, charges, and multiplicities.\n')

    # Read VASP POSCAR with phonopy interface
    # calling read_vasp() returns an instance of the PhonopyAtoms class
    unitcell = read_vasp(user_args.POSCAR_file)

    # Parse chemical formulae and charges given by user
    molecules = parse_user_formulae(user_args.molecules)
    formulae = [i for i, _, _ in molecules]

    # Check that the indicated chemical formulae add up to the POSCAR info
    compare_poscar_to_formulae(formulae, unitcell)

    # Calculate the distortion supercell expansion
    if user_args.dim is None:
        # Use lattice vectors to guess an isotropic expansion.
        dsc_expansion = isotropic_expansion(unitcell.totuple()[0])
    else:
        # Use user-defined expansion
        dsc_expansion = user_args.dim

    # Generate Phonopy objects for distortion supercell and unitcell
    supercell, unitcell = generate_supercell(
        unitcell,
        user_args.FORCE_SETS,
        dsc_expansion,
        user_args.force_expansion
    )

    # Break tuple
    dsc_lat_vecs, dsc_frac_coords, dsc_atomic_numbers = supercell.totuple()

    # Fractional to cartesian coordinates
    dsc_cart_coords = transform_coordinates(
        dsc_lat_vecs,
        dsc_frac_coords,
        to_cartesian=True
    )

    # Get atomic symbols
    dsc_atomic_symbols = xyzp.num_to_lab(
        dsc_atomic_numbers,
        numbered=False
    )
    dsc_atomic_symbols = np.array(dsc_atomic_symbols)

    # Find the unique atoms in the distortion supercell
    # Get the indices of atoms in the central unitcell
    # (relative to distortion supercell)
    uc_indices_atom = find_central_unitcell(
        dsc_frac_coords,
        dsc_expansion
    )

    # Save unedited distortion supercell
    xyzp.save_xyz(
        "distortion_supercell.xyz", dsc_atomic_symbols, dsc_cart_coords
    )

    # Generate symmetry information
    sym_ds = spglib.get_symmetry_dataset(
        (dsc_lat_vecs, dsc_frac_coords, dsc_atomic_numbers)
    )


    equiv_atoms = sym_ds['equivalent_atoms']

    print("Hall number:", sym_ds["number"])
    P = sym_ds["transformation_matrix"] # standardised to input
    W = sym_ds["std_rotation_matrix"] # standardised to idealised
    p = sym_ds["origin_shift"]
    original_lattice = dsc_lat_vecs
    ideal_lattice = sym_ds["std_lattice"]
    ideal_f_coords = sym_ds["std_positions"]
    ideal_a_nums = sym_ds["std_types"]
    ideal_at_symbs = xyzp.num_to_lab(ideal_a_nums, numbered=False)
    primitive_lattice = sym_ds["primitive_lattice"]
    standard_lattice = LA.inv(P) @ original_lattice.T

    print()
    print("Original lattice:\n", original_lattice)
    print("Primitive lattice:\n", primitive_lattice)
    print("Standardised lattice:\n", standard_lattice)
    print("Idealised lattice:\n", ideal_lattice)

    print()
    print("input --> standard transformation matrix:\n", LA.inv(P))
    print("standard --> ideal transformation matrix :\n", W)
    print("spglib's origin shift:\n", p)

    unique = np.unique(equiv_atoms)

    print("Unique indices are:")
    print(unique)

    pure_rots = []
    pure_trans = []

    for it, (rot, trans) in enumerate(zip(sym_ds["rotations"], sym_ds["translations"])):
        if np.trace(rot) == 3 and np.sum(trans) == 0:
            print("Identity, whatever!")
        elif np.trace(rot) == 3:
            print("pure translation ({}):".format(it), trans)
            pure_rots.append(rot)
        elif np.sum(trans) == 0:
            print("pure rotation ({}):".format(it), rot)
            pure_trans.append(trans)

    # Apply pure rotations
    new_fcoords = np.empty([3, 1])
    new_labs = np.empty([1], dtype=str)

    print(np.shape(ideal_f_coords))

    for rot in pure_rots:
        new_fcoords = np.hstack([new_fcoords, rot @ ideal_f_coords.T])
        new_labs = np.hstack([new_labs, ideal_at_symbs])

    new_ccoords = transform_coordinates(
        ideal_lattice,
        new_fcoords.T,
        to_cartesian=True
    )

    ideal_c_coords = transform_coordinates(
        ideal_lattice,
        ideal_f_coords,
        to_cartesian=True
    )

    xyzp.save_xyz("ideal.xyz", ideal_at_symbs, ideal_c_coords)
    xyzp.save_xyz("rot_build.xyz", new_labs, new_ccoords)
    xyzp.save_xyz(
        "unique.xyz",
        dsc_atomic_symbols[unique],
        dsc_cart_coords[unique]
    )

    exit()

    # From the symmetry relations, extract the pure translations only
    relations_trans = discriminate_symm_ops(
        symmetry,     # spglib symmetry object
        dsc_frac_coords,  # supercell fractional coordinates
        dsc_expansion     # supercell expansion dimensions
    )


    # Get dictionary of {"formula": indices}
    # for each entity (molecules/ions, broken or complete) in distortion
    # supercell
    entities = xyzp.find_entities(
        dsc_atomic_symbols,
        dsc_cart_coords
    )

    # Create dictionary of complete molecules {formula:indices} of distortion
    # supercell which match user provided formula
    dsc_molecules = {}
    for form in formulae:
        formstr = xyzp.formdict_to_formstr(form)
        try:
            dsc_molecules[formstr] = entities[formstr]
        except KeyError:
            sys.exit(
                "Specified formula {} not present in \
                 distortion supercell".format(
                     formstr
                )
            )

    # Create dictionary of complete molecules {formula:indices} of distortion
    # supercell which have at least one atom in the central unit cell
    uc_molecules = {xyzp.formdict_to_formstr(form): [] for form in formulae}
    [
        uc_molecules[xyzp.formdict_to_formstr(form)].append(indices)
        for form in formulae
        for indices in list(dsc_molecules[form]) if set(indices).intersection(
            uc_indices_atom
        )
    ]

    # List of indices of full molecules which have at least one atom in
    # central unit cell
    uc_indices_mol = np.array(flatten(list(uc_molecules.values())))

    # Save central unit cell
    xyzp.save_xyz(
        "unitcell.xyz",
        dsc_atomic_symbols[uc_indices_mol],
        dsc_cart_coords[uc_indices_mol]
    )

    # Save distortion supercell
    f_name = "supercell_{:d}_{:d}_{:d}.xyz".format(*dsc_expansion)

    xyzp.save_xyz(
        f_name,
        dsc_atomic_symbols,
        dsc_cart_coords,
        verbose=False
    )

    # Generate Gaussian input files
    create_gaussian_files(
        uc_molecules,
        dsc_cart_coords,
        np.array(dsc_atomic_symbols),
        molecules,
        user_args.functional,
        user_args.basis_set
    )

    # Create file to keep track of atom indices
    # generate_gaussian_rosetta(dsc_to_uc_inds, relations_trans, dsc_expansion)

    f_name = "{}_{}_{}_{}_{}.xyz".format(
        user_args.POSCAR_file.split('.')[0], *dsc_expansion, "supercell"
    )

    xyzp.save_xyz(f_name, dsc_atomic_symbols, dsc_cart_coords, verbose=False)

    return


def discriminate_symm_ops(spglib_symm, frac_coords, dimension):
    '''
    Identify atoms related by pure translation operations.

    Parameters
    ----------
        spglib_symm  : spglib.Symmetry
            Instance of spglib symmetry object
        frac_coords : np.ndarray
            Fractional atomic coordinates, Nx3 matrix.
        dimension : list
            Integer multiples of a, b, c lattice constants.

    Returns
    -------
        dict
            Key   -> symmetrically independent atomic index
            Value -> list of atom indices related by trans
    '''

    # spglib_symm is a dictionary with keys: 'rotation', 'transation' and
    # 'equivalent_atoms'. The latter gives the mapping table from the atomic
    # indices of the input unit cell to the atomic indices of symmetrically
    # independent atom, such as [0, 0, 0, 0, 4, 4, 4, 4], where the
    # symmetrically independent atomic indices are 0 and 4.
    equiv_atoms = spglib_symm['equivalent_atoms']

    unique = np.unique(equiv_atoms)

    print("Unique indices are:")
    print(unique)

    for it, (rot, trans) in enumerate(zip(spglib_symm["rotations"], spglib_symm["translations"])):
        if np.trace(rot) == 3 and np.sum(trans) == 0:
            print("Identity, whatever!")
        elif np.trace(rot) == 3:
            print("pure translation ({}):".format(it), trans)
        elif np.sum(trans) == 0:
            print("pure rotation ({}):".format(it), rot)

    exit()
    # Atom indices related by translation
    trans_relation = {}

    # Boundaries for each dimension
    _limits = [np.linspace(0, 1, d+1) for d in dimension]
    # Flatten the list
    _limits = [item for sublist in _limits for item in sublist]

    # Loop over the symmetrically independent atomic indices of the supercell
    for it, ind in enumerate(equiv_atoms):

        # Consider only the atoms that are related by symmetry (any)
        gen = [ij for ij, val in enumerate(equiv_atoms)
               if val == ind and ij != it]

        # Calculate distances between equivalent atoms, and
        # compare to dimensions
        _trans = [
            i for i in gen
            if any(
                any(
                    np.round(lim, 5) ==
                    np.round(abs(frac_coords[i] - frac_coords[it]), 5)
                )
                for lim in _limits
            )
        ]

        # Populate the dictionary with lists of pure translations
        trans_relation[it] = _trans

    return trans_relation


def equilibrium_func(user_args):
    """
    Wrapper for equilibrium mode
    """

    if not user_args.run:

        message = "When this job is finished, ALL "
        message += "OpenMolcas files will be generated in the "
        message += "\033[0;34m"
        message += "equilibrium"
        message += "\033[0m"
        message += " subfolder\n"
        message += "Submit the jobscript with "
        message += "\033[0;32m"
        message += "qsub submit_eq.sh"
        message += "\033[0m"
        submit_self("generate_molcas_equilibrium.sh", message=message)
        exit()

    supercell_labels, supercell_coords = xyzp.load_xyz(user_args.supercell)

    # Swap diamagnetic label to paramagnetic label
    supercell_labels = np.array(
        [
         user_args.symbol[1]
         if i == user_args.symbol[0] else i for i in supercell_labels
        ]
       )

    # Create a dictionary that links supercell atom indices with charges
    # and dipoles of the full molecules within the central unitcell
    # Define the supercell atom indices of CASSCF molecule
    indices_charge_dipole = read_gaussian_rosetta(user_args.gaussian_rosetta)

    # Define the supercell atom indices of CASSCF molecule
    indices_CASSCF = get_CASSCF_mol_indices(
        user_args.gaussian_rosetta,
        user_args.symbol[0]
    )

    # Define the xfield section
    xfield = create_xfield(
        supercell_coords,
        indices_charge_dipole,
        indices_CASSCF,
        folder=os.getcwd()
    )

    # Create directory to store files
    subfolder = os.path.join(os.getcwd(), 'equilibrium')
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)

    basename = user_args.supercell.split('.')[0]
    in_file_name = '{}_eq.input'.format(basename)
    out_file_name = '{}_eq.output'.format(basename)
    sub_file_name = os.path.join(subfolder, "{}_eq.sh".format(basename))

    # Generate Molcas input file
    msgi.generate_input(
        supercell_labels[indices_CASSCF],
        supercell_coords[indices_CASSCF],
        user_args.symbol[1],
        user_args.charge,
        user_args.n_active_elec,
        user_args.n_active_orb,
        user_args.n_coord_atoms,
        os.path.join(subfolder, in_file_name),
        xfield=xfield,
        high_S_only=True,
        seward_decomp='RICD\nacCD',
        ang_central=True,
        seward_extra=[]
    )

    # Generate Molcas submission script
    msgj.gen_submission_csf(
        in_file_name,
        out_file_name,
        submit_file=sub_file_name)

    return


def error_handler(e):
    print('error')
    print(dir(e), "\n")
    print("-->{}<--".format(e.__cause__))


def distort_func(user_args):

    """
    Wrapper function for distort mode
    """

    if not user_args.run:
        message = "When this job is finished, "
        message += "submit the distorted calculations with\n"
        message += "\033[0;32m"
        message += "condor_submit_dag submit.dag"
        message += "\033[0m"
        submit_self("submit_distort.sh", message=message)
        exit()

    # # Read QUAX and SO energies
    # quax = mse.read_quax(user_args.eq_out)
    # energies = get_eq_rassi_energies(
    #     user_args.eq_out,
    #     user_args.n_rassi_states
    # )

    energies = [1000., 2]
    quax = np.ones([3, 3])

    # Phonopy object that will be modulated with a supercell
    # consistent with that used to calculate the forces
    cell_to_modulate = get_cell_to_modulate(user_args)

    # Phonopy object to access the commensurate q-vectors and
    # associated phonon energies for the indicated supercell expansion
    q_vectors = get_qvectors(user_args.POSCAR_file, user_args.SUPERCELL)

    # Create a dictionary that links supercell atom indices with charges
    #indices_charge_dipole = read_gaussian_rosetta(user_args.gaussian_rosetta)

    # Supercell atom indices of CASSCF molecule
    # indices_CASSCF = get_CASSCF_mol_indices(
    #     user_args.gaussian_rosetta,
    #     user_args.symbol[0]
    # )

    indices_CASSCF = []
    indices_charge_dipole = []

    # CSF Absolute path to RasOrb
    # Condor/AWS name of RasOrb
    if user_args.hpc == 'csf':

        # Define absolute path to local RasOrb
        if user_args.inporb is None:
            inporb = user_args.eq_out.replace(
                        user_args.eq_out.split('.')[-1],
                        'RasOrb'
                    )
        else:
            inporb = user_args.inporb

        initial_orb = os.path.join(
            os.getcwd(),
            inporb
        )
    else:

        if user_args.inporb is None:
            basename = os.path.basename(user_args.eq_out)
        else:
            basename = os.path.basename(user_args.inporb)
        initial_orb = basename.replace(
            os.path.splitext(basename)[1],
            '.RasOrb'
        )

    if user_args.phonon_threshold:
        phonon_threshold = user_args.phonon_threshold
    else:
        phonon_threshold = energies[-1] * 1.1

    distort_args = (
        phonon_threshold,
        indices_charge_dipole,
        indices_CASSCF,
        initial_orb,
        quax,
        user_args.SUPERCELL,
        user_args.symbol,
        user_args.charge,
        user_args.n_active_elec,
        user_args.n_active_orb,
        user_args.n_coord_atoms
    )

    pool = mp.Pool(4)

    for _, (q_x, q_y, q_z) in enumerate(q_vectors):
        pool.apply_async(
            distort_loop,
            args=(
                q_x,
                q_y,
                q_z,
                copy.deepcopy(cell_to_modulate)
            ) + distort_args,
            callback=lambda x: None,
            error_callback=error_handler
        )

    # Close Pool and let all the processes complete
    pool.close()
    pool.join()

    dir_list = []

# Generate list containing absolute paths to all directories
    # Loop over the q-vectors
    for _, (q_x, q_y, q_z) in enumerate(q_vectors):

        phonon_freqs = cell_to_modulate.get_frequencies((q_x, q_y, q_z))

        for ij, freq in enumerate(phonon_freqs):

            # Consider only the phonons that can effect transitions
            if freq > phonon_threshold:
                break

            for direction in [-1., 1.]:

                if direction == -1.:
                    _subfolder = 'negative'
                else:
                    _subfolder = 'positive'

                qpoint = 'q_{:2f}_{:2f}_{:2f}'.format(q_x, q_y, q_z)
                parent_folder = os.path.join(os.getcwd(), qpoint)
                subfolder = os.path.join(
                    parent_folder, _subfolder, 'vib_{}'.format(ij+1)
                )
                dir_list.append(subfolder)

    # Create dir_list.txt file
    gen_dir_list(dir_list)

    in_file_name = '{}.input'.format(user_args.symbol[1])
    out_file_name = '{}.output'.format(user_args.symbol[1])
    cfp_grab = 'grep -A 400 "GROUND ATOMIC MULTIPLET"'
    cfp_grab += ' {} > tmp.out\n'.format(out_file_name)

    cfp_grab += 'grep -E -A 115 -m 1 '
    cfp_grab += r'"Hcf \= SUM_\{k,q\} \* \[ B\(k,q\) \* O\(k,q\) \]" '
    cfp_grab += 'tmp.out > molcas_cfps.dat\n'
    cfp_grab += 'rm tmp.out\n'
    # Write the OpenMolcas job array submission script
    if user_args.hpc == 'csf':

        msgj.gen_submission_csf_array(
            in_file_name,
            out_file_name,
            len(dir_list),
            "4f",
            submit_file='submit_jobarray.sh',
            extractor=cfp_grab
        )

    else:
        if user_args.hpc == 'condor':
            aws = False
        elif user_args.hpc == 'aws':
            aws = True

        # Define absolute path to local RasOrb
        if user_args.inporb is None:
            inporb = user_args.eq_out.replace(
                         user_args.eq_out.split('.')[-1],
                         'RasOrb'
                    )  # subfolder/filename.out -> subfolder/filename.RasOrb
        else:
            inporb = user_args.inporb

        # path to rasorb file
        dir_eq_RasOrb = os.path.join(
            os.getcwd(),
            inporb
        )

        msgj.gen_submission_condor(
            in_file_name,
            out_file_name,
            "4f",
            extra_input_files=[dir_eq_RasOrb],
            extra_output_files=["molcas_cfps.dat"],
            aws=aws,
            extractor=cfp_grab
        )

    return


def get_phonon_force_constants(cell, q):
    """
    Remove mass weighting from dynamical matrix and rediagonalise to get
    force constants

    Parameters
    ----------
    cell: Phonopy object
        Phonopy object for supercell
    q_point: np.ndarray
        q point as q_x, q_y, q_z in fractional coordinates

    Returns
    -------
    np.ndarray:
        Array of force constants, one per mode in units of N m^-1
    np.ndarray:
        Array of reduced masses, one per mode in units of kg
    """

    EV2J = 1.60217733E-19  # [J eV-1]
    AMU2kg = 1.6605402E-27  # [kg AMU-1]

    # Set masses to unity and calculate dynamical matrix (hessian)
    # this is the non-mass weighted hessian
    n_atoms = len(cell._dynamical_matrix._pcell.masses)
    masses = cell._dynamical_matrix._pcell.masses*AMU2kg
    cell._dynamical_matrix._pcell.masses = [1.]*n_atoms
    cell._set_dynamical_matrix()
    cell._dynamical_matrix.run(q)
    dm = cell._dynamical_matrix.get_dynamical_matrix()

    # Diagonalise dynamical matrix to give force constants
    fc, vecs = LA.eigh(dm)
    fc = np.array([np.abs(f) for f in fc])

    # Convert from eV . Angstrom^-2 to J . m^-2 = N m^-1
    fc *= EV2J * 10E20 / (2*np.pi)

    # Calculate reduced mass as mass-weighted sum of eigenvector
    # components for each mode
    red_mass = np.zeros(3*n_atoms)
    triple_mass = np.tile(masses, (3, 1))
    triple_mass = np.reshape(triple_mass, 3*n_atoms, order='F')

    for it in range(3*n_atoms):
        red_mass[it] = 1./(np.sum(vecs[:, it]**2/triple_mass))

    return fc, red_mass


def distort_loop(q_x, q_y, q_z, cell_to_modulate, phonon_threshold,
                 indices_charge_dipole, indices_CASSCF, initial_orb, quax,
                 supercell_size, central_symbols, charge, n_active_elec,
                 n_active_orb, n_coord_atoms):
    '''
    Loop over q vectors to generate input files

    Parameters
    ----------
    cell_to_modulate: Phonopy object


    Returns
    -------
        None
    '''

    qpoint = 'q_{:2f}_{:2f}_{:2f}'.format(0., 0., 0.)
    parent_folder = os.path.join(os.getcwd(), qpoint)

    phonon_fcs, phonon_redmasses = get_phonon_force_constants(
        copy.deepcopy(cell_to_modulate),
        (0., 0., 0.)
    )

    # Define the frequencies of each q-vector
    # in wavenumbers
    phonon_freqs = cell_to_modulate.get_frequencies((0., 0., 0.)) * 33.3564095

    # Calculate thermally averaged displacements
    # *** Not done yet ***
    # thermally_averaged = calculate_thermally_averaged(phonon_freqs)

    # Loop over the frequencies and assign job to thread
    for ij, freq in enumerate(phonon_freqs):

        # Consider only the phonons that can effect transitions
        if freq*33.3564095 > phonon_threshold:  # 33.35 from THz to cm-1
            break

        # Go to -ve and +ve directions of the displacement vector
        for direction in [-1., 1.]:

            if direction == -1.:
                _subfolder = 'negative'
            else:
                _subfolder = 'positive'

            # Define the name of the subfolder
            subfolder = os.path.join(
                parent_folder, _subfolder, 'vib_'+str(ij+1)
            )

            # Create the subfolder
            if not os.path.exists(subfolder):
                os.makedirs(subfolder, exist_ok=True)

            # Modulate the supercell
            # set_modulations() takes
            #  supercell expansion as first argument
            #  list with
            # [q-point, band index (int), amplitude (float), phase (float)]
            cell_to_modulate.set_modulations(
                supercell_size,
                # [ [ (q_x, q_y, q_z), ij, direction*thermally_averaged[ij],0.] ] # noqa
                [[(q_x, q_y, q_z), ij, direction*0.01, 0.]]
                )

            # Get the modulated supercell
            # list of PhonopyAtoms objects - here only 1 dimension
            _modulated = cell_to_modulate.get_modulated_supercells()
            _modulated_tuple = _modulated[0].totuple()

            # Transform fractional to cartesian coordinates
            spcell_cartesian = transform_coordinates(
                _modulated_tuple[0],  # lattice_vectors
                _modulated_tuple[1],  # fractional positions
                to_cartesian=True
            )

            # Shift to origin here
            # missing
            _xfield = create_xfield(
                spcell_cartesian,
                indices_charge_dipole,
                indices_CASSCF,
                folder=subfolder
            )

            # Generate Molcas input file using molcas_suite package
            msgi.generate_input(
                get_atsymbols(
                    _modulated_tuple[2],
                    swap=central_symbols,
                )[indices_CASSCF],
                spcell_cartesian[indices_CASSCF],
                central_symbols[1],
                charge,
                n_active_elec,
                n_active_orb,
                n_coord_atoms,
                os.path.join(subfolder, central_symbols[1]+'.input'),
                xfield=_xfield,
                high_S_only=True,
                seward_decomp='RICD\nacCD',
                ang_central=True,
                seward_extra=[],
                initial_orb=initial_orb,
                quax=quax,
                extract_orbs=False
            )

            print("")

            # Write the phonon energy (cm-1)
            write_phonon_energy(subfolder, freq*33.3564095)

            # write the phonon force constant (??)

    return


def generate_supercell(poscar, forces_file, supercell_expansion,
                       force_expansion):
    '''
    Generate a supercell for use in the distortion calculations.
    This expansion (supercell_expansion) is on-top-of the one used to
    calculate the forces (force_expansion)

    Parameters
    ----------
    poscar : PhonopyAtoms
        Unit cell obtained from Vasp file import
    supercell_expansion : list
        Integer multiples of a, b, c lattice constants used to create
        supercell for distortions
    force_expansion : list
        Integer multiples of a, b, c lattice constants used to create
        supercell in phonon calculations (for forces)
    forces_file : str
        File containing phonopy forces
    Returns
    -------
        Phonopy
            Unit cell object
        PhonopyAtoms
            Supercell object
    '''
    # Instantiate a Phonopy object, consistent with the cell size
    # used to optimise the structure in VASP
    unitcell = Phonopy(
        poscar,
        supercell_matrix=force_expansion
    )

    # Load FORCE_SETS Phonopy file.
    unitcell.set_displacement_dataset(
        parse_FORCE_SETS(filename=forces_file)
       )

    # Create DynamicalMatrix.
    unitcell.produce_force_constants()

    # Create supercell with user specified expansion
    # and zero modulation amplitude (phonon motion)
    # i.e. no phonons are in effect (modulating)
    #      this is just a big cell
    try:
        unitcell.set_modulations(
            supercell_expansion,
            [[(0, 0, 0), 0, 0., 0.]]  # [q-point, band_index, amplitude, phase]
        )

    except MemoryError:
        exit('\n*** MemoryError ***\n\
            Requested supercell expansion exceeds available node memory\n')

    # Get the "modulated" supercell
    # returns list of modulated supercells
    # in our case there is only 1 modulated supercell
    # and it has zero phonon amplitude
    # this is just a big cell
    supercell = unitcell.get_modulated_supercells()[0]

    '''
    *** DO NOT DELETE! ***

    The above method is equivalent (for tested cases) to:

    # Instantiate a PhonopyAtoms object
    poscar = read_vasp(user_args.POSCAR_file)

    # Instantiate a Phonopy object
    _supercell = Phonopy(poscar, user_args.supercell_expansion)

    # Initialise a Supercell class calling the Phonopy method get_supercell.
    # See line 42 in
    # https://github.com/phonopy/phonopy/blob/develop/phonopy/structure/cells.py
    # get_supercell returns an instance of Supercell class,
    # whose parent class is PhonopyAtoms (see line 109).
    # that means that Supercell inherits the PhonopyAtoms class,
    # which has totuple() method.
    # Thus, the return from _supercell.get_supercell() has totuple() method

    supercell = _supercell.get_supercell()

    This is done via get_modulated_supercells() to ensure the consistency
    with the "distort" part of the program.

    '''

    return supercell, unitcell


# -------
# charges
# -------


def isotropic_expansion(lattice_vectors):
    '''
    Defines the size of the supercell based on the lattice vectors. This is a
    very arbitrary approach. Maybe generalise it based on cell volume.

    Parameters
    ----------
    lattice_vectors : np.ndarray
        3x3 matrix containing the lattice vectors

    Returns
    -------
    list
        3 integers defining the supercell expansion
    '''

    # get_cell_parameters() returns the basis vector lengths
    _lattice_constants = get_cell_parameters(lattice_vectors)

    # For small cells (< 10 Angstrom), large expansion
    if any(i < 10. for i in _lattice_constants):
        dim = 5
    # For intermediate cells, intermediate expansion
    elif any(10. <= i < 15. for i in _lattice_constants):
        dim = 3
    # For large cells, small expansion
    else:
        dim = 1

    dimension = [dim, dim, dim]

    return dimension


def get_atsymbols(atnumbers, swap=[]):
    '''
    Convert atomic numbers to atomic symbols

    Parameters
    ----------
        atnumbers : list
            Atomic numbers

    Keyword arguments:
        swap : list
            Pair of diamagnetic/magnetic atoms

    Returns
    -------
        np.ndarray
            Atomic symbols
    '''

    # Define an empty list to store atomic symbols.
    _atsymbols = []

    # Define a dictionary of supported atoms.
    Z = {
        1: 'H', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 13: 'Al', 14: 'Si',
        15: 'P', 16: 'S', 17: 'Cl', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
        23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu',
        30: 'Zn', 35: 'Br', 39: 'Y', 57: 'La', 71: 'Lu'
        }

    # Collect the atomic symbol of the provided atomic numbers.
    for key in atnumbers:
        _atsymbols.append(Z[key])

    # Change diamagnetic for magnetic metal in the labels
    if swap:
        _atsymbols = [swap[1] if i == swap[0] else i for i in _atsymbols]

    return np.array(_atsymbols)


def parse_user_formulae(molecules_list):
    '''
    Parse user-provided molecular formulae and charges.

    Parameters
    ----------
        molecules_list : list
            List of molecule, charge, multiplicity, molecule, charge,
                ... provided by user

    Returns
    -------
        list
            List of tuples, one per molecule, containing
            dict, int
            ({atomic label: number of atoms}, charge, multiplicity)
    '''

    # Define an empty list to store chemical formula and charge as tuples.
    _molecules = []

    # Loop over the chemical formulae.
    for i in range(0, len(molecules_list), 3):

        # Define the formula string.
        _mol = molecules_list[i]

        # Convert formula string into dictionary (key:symbol, val:natoms)
        _formula = xyzp.formstr_to_formdict(_mol)

        _charge = int(molecules_list[i+1])
        _mult = int(molecules_list[i+2])

        # Update the _molecules list
        _molecules.append(
            (_formula, _charge, _mult)
           )

    return _molecules


def compare_poscar_to_formulae(formulae, poscar):
    '''
    Checks that user provided formulae match that obtained from poscar

    Parameters
    ----------
        formulae : list
            User provided molecular formulae as list of dicts
        poscar : PhonopyAtoms
            Instance of PhonopyAtoms class.

    Raises
    ------
        ValueError
            If inconsistency found.

    Returns
    -------
        None
    '''

    # Get atomic symbols in unit cell from POSCAR
    unitcell_symbols = poscar.get_chemical_symbols()

    # Count number of each atomic symbol in poscar
    # and store as dictionary, key is symbol
    poscar_dict = Counter(unitcell_symbols)

    # Loop over atomic symbols `key` and ocurrences `val` in POSCAR
    for key, val in poscar_dict.items():

        # Sum number of atoms of `key` in each formula
        _natoms = 0
        for mol in formulae:
            if key in mol.keys():
                _natoms += mol[key]

        # and check that this number is an integer multiple of `val`
        if val % _natoms:
            try:
                raise ValueError
            finally:
                print(
                    '\n***Error***\n\
                    Chemical formula {} does not match the content of \
                    POSCAR file.\n'.format(key)
                )

    return


def transform_coordinates(lv, pos,
                          to_cartesian=False, to_fractional=False):
    '''
    Convert between cartesian and fractional coordinates

    Parameters
    ----------
        lv : np.ndarray
            3x3 matrix, where a,b,c are given as rows
        pos : np.ndarray
            Atomic coordinates, Nx3 matrix

    Keyword arguments:
        to_cartesian : bool, default False
            Transform fractional to cartesian coordinates
        to_fractional : bool, default False
            Transform cartesian to fractional coordinates

    Returns
    -------
        coordinates
    '''

    if to_cartesian:
        coordinates = np.asarray([np.dot(atom, lv) for atom in pos])

    if to_fractional:
        coordinates = np.asarray([np.dot(atom, LA.inv(lv)) for atom in pos])

    return coordinates


def find_central_unitcell(dsc_positions, _dimension):
    '''
    Extract atom indices in the supercell that belong to the central unitcell.

    Parameters
    ----------
        dsc_positions : list
            List of atomic positions in supercell
        _dimension : list
            Integer multiples of a, b, c lattice constants

    Returns
    -------
        list
            Indices of atoms within central unitcell
    '''

    # Defines the boundaries of the central unitcell.
    # For instance, for a [ 2, 3, 4 ] expansion, it will return
    # [ [0.50, 1.00], [0.3333, 0.6666], [0.5, 0.75] ]
    _limits = [
        np.linspace(0, 1, d+1)[int(d/2):int(d/2)+2] for d in _dimension
        ]

    # Loop over all fractional coordinates and collect the indices of the atoms
    # that fall within the central unitcell.
    central_unitcell = [it for it, coord
                        in enumerate(dsc_positions)
                        if _limits[0][0] <= coord[0] <= _limits[0][1]
                        and _limits[1][0] <= coord[1] <= _limits[1][1]
                        and _limits[2][0] <= coord[2] <= _limits[2][1]
                        ]

    return central_unitcell


def create_gaussian_files(molecules, spcell_coords, spcell_atsymbols,
                          mols_info, functional, basis_set):
    '''
    Creates gaussian .com files for CHELPG calculations

    Parameters
    ----------
        molecules (dict)         : Complete molecules within central unitcell.
                                   keys = molecular formula,
                                   vals = list of lists of atomic indices.
        spcell_coords    (array) : Supercell cartesian coordinates.
        spcell_atsymbols (list)  : supercell atomic symbols.
        mols_info        (tuple of (dict, charge, S_mult)) :
                                   Contains formulae, charge, and multiplicity
        functional (str)         : DFT functional name
        basis_set (str)          : Basis set name for all non-Stuttgart ECP

    Returns
    -------
        None
    '''

    try:
        os.mkdir("gaussian_charges")
    except FileExistsError:
        pass
    # ECPs for non-GTO atoms
    ecp_supported = {
        "Y": "stuttgart rsc 1997",
        "I": "{}-pp".format(basis_set.lower()),
        "Cr": "stuttgart rsc 1997",
        "Sn": "{}-pp".format(basis_set.lower())
    }

    # Loop over molecular formula
    for key in sorted(molecules):

        charge, multiplicity = _get_charge_mult(key, mols_info)

        # Loop over each instance of current molecular formula
        for it, indices in enumerate(molecules[key]):

            elements = xyzp.formstr_to_formdict(key).keys()

            # Set basis quality for all atoms other than ECP type
            bs_spec = {}
            ecp_spec = {}
            for ele in elements:
                if ele in ecp_supported.keys():
                    ecp_spec[ele] = ecp_supported[ele]
                else:
                    bs_spec[ele] = basis_set

            # Create Gaussian input file
            f_name = "gaussian_charges/{}_{:d}.com".format(key, it + 1)
            ggen.gen_input(
                f_name,
                spcell_atsymbols[indices],
                spcell_coords[indices],
                charge,
                multiplicity,
                functional,
                bs_spec,
                ecp_spec=ecp_spec,
                chelpg=True,
                opt=False,
                freq=False,
                extra_route=["NoSymm"],
                verbose=False
            )

    # Create a .sh file to submit all individual Gaussian jobs.
    _create_sh(molecules)

    return


def _get_charge_mult(formula, molecule_info):
    '''
    Find molecular charge for molecule specified in `formula` by comparing to
    user defined list of charges in `molecule_info`

    Parameters
    ----------
        formula : str
            Molecular formula
        molecule_info : list
            List of tuples, one per molecule, containing
            dict, int
            ({atomic label: number of atoms}, charge)

    Returns
    -------
        int
            Molecular charge
    '''

    for formdict, charge, mult in molecule_info:
        if xyzp.formdict_to_formstr(formdict) == formula:
            _charge = charge
            _mult = mult

    return _charge, _mult


def generate_gaussian_rosetta(_molecules, _trans_relations, _dimension):
    '''
    Generate file relating atom indices of individual Gaussian jobs to atom
    indices in supercell.

    Parameters
    ----------
        molecules        (dict) : Complete molecules within central unitcell.
                                  keys = molecular formula,
                                  vals = list of lists of atomic indices.
        _trans_relations (dict) : key -> symmetrically independent atomic index
                                  val -> list of atom indices related by trans
        _dimension    (list)  : Integer multiples of a, b, c lattice constants.

    Returns
    -------
        None
    '''
    # Define filename
    f_name = 'gaussian_rosetta.dat'

    # Create input file.
    with open(f_name, 'w') as f:

        f.write(
            'Relationship between the atom indices of individual molecules\
 in the central unitcell and those in the supercell.\n\
  1st column: atom index in the Gaussian jobs.\n\
  2nd column: atom index in the supercell.\n\
  Rest: atom indices related by pure translations to those in 2nd column.\n')

        # Report the arguments used to generate the job.
        f.write('Generated with:\n')
        for arg in sys.argv[1:]:
            f.write(' {}'.format(arg))
        # Provide the expansion calculated with isotropic_expansion()
        if '--dim' not in sys.argv[1:]:
            f.write(' --dim')
            for i in _dimension:
                f.write(' {}'.format(str(i)))
        f.write('\n')

        # Loop over the dictionary sorted by keys.
        for key in sorted(_molecules):

            # Loop over the indices of the molecule.
            for it, indices in enumerate(_molecules[key]):

                # Write the identifier for the molecule.
                f.write('Molecule {}_{}.com\n'.format(key, it+1))

                # Write the relationship between indices.
                for ij, val in enumerate(indices):
                    f.write('    {:d} {:d}'.format(ij, val))
                    for ik in _trans_relations[val]:
                        f.write(' {:d}'.format(ik))
                    f.write('\n')

    f.close()

    return


def _create_sh(_molecules):
    '''
    Generate jobscript to submit individual Gaussian jobs.

    Parameters
    ----------
        molecules (dict) : Complete molecules within central unitcell.
                           keys = molecular formula,
                           vals = list of lists of atomic indices.

    Returns
    -------
        None
    '''

    f_name = 'gaussian_charges/submit_charges.sh'

    # Create input file.
    with open(os.path.join(os.getcwd(), f_name), 'w') as f:
        f.write('#$ -S /bin/bash \n \n')

        for key in sorted(_molecules):

            for it, _ in enumerate(_molecules[key]):

                if "Y" in key:
                    n_cores = 8
                else:
                    n_cores = 4

                f.write('gaussian_suite submit {}_{:d}.com {} \n'.format(
                    key, it+1, n_cores))

    f.close()

    os.system('chmod +x {}'.format(f_name))

    return


# ------------
# equilibrium
# ------------


def read_gaussian_rosetta(f_rosetta):
    '''
    Retrieve information from gaussian_rosetta.dat file.

    Parameters
    ----------
        f_rosetta : str
            Filename of gaussian rosetta file generated by charges mode

    Returns
    -------
        dict
            Collection of charges and dipoles of symmetry-related
            (translation) atoms
                keys: supercell atom indices used in Gaussian jobs.
                vals: tuple containing three elements
                    1st: supercell atom indices related by translation to key
                    2nd: charge (int) of key atom
                    3rd: dipoles (array) of key atom
    '''

    # Define a dictionary with keys as atom indices (those from Gaussian jobs),
    # and values as translationally-related indices, and their
    # charges and dipoles.
    _dict = {}

    # Read the gaussian_rosetta.dat file.
    with open(f_rosetta, 'r') as f:

        for line in f:

            # Find the sections of each molecule.
            if 'Molecule' in line.split():

                molecule = line.split()[1].split('.')[0]
                f_name = "gaussian_charges/{}.log".format(molecule)

                _charges, _dipoles = gcde.get_charges_dipoles_log(f_name)

                line = next(f)

                for j in range(len(_charges)):

                    # Collect the atom indices related by pure translations.
                    # excluding the key
                    # _trans = list(map(int, line.split()[2::]))
                    # including the key so read_gaussian_rosetta can
                    # discriminate
                    # the CASSCf moiety.
                    _trans = list(map(int, line.split()[1::]))

                    # Populate the values of this key
                    _dict[int(line.split()[1])] = (
                        _trans,
                        _charges[j],
                        _dipoles[j]
                    )

                    # Do not advance one line if at the end of block
                    if j == len(_charges)-1:
                        continue
                    else:
                        line = next(f)

    # Get the indices of molecule to be treated at CASSCF level.
    # _indices_CASSCF = _identify_CASSCF_mol(user_args)

    # return _dict, _indices_CASSCF
    return _dict


def get_CASSCF_mol_indices(f_rosetta, metal_label):
    '''
    Get the supercell atom indices of the molecule to be treated at CASSCF.

    Parameters
    ----------
        f_rosetta : str
            Filename of gaussian rosetta file generated by charges mode
        metal_label : str
            Atomic label of diamagnetic central metal ion
    Returns
    -------
        np.ndarray
            Supercell atom indices
    '''

    # List to store the indices of the first found molecule
    # to be treated at CASSCF level. This is done checking whether the chemical
    # formula contains the user-provided diamagnetic atomic symbol
    # The first "matching" molecule is assumed to be the central one
    _indices_CASSCF_mol = []

    with open(f_rosetta, 'r') as f:

        for line in f:

            # Find the sections of each molecule.
            if 'Molecule' in line.split():

                # Get the atomic symbols of the molecule.
                _symbols = xyzp.formstr_to_formdict(
                    line.split()[1].split('_')[0]
                )

                _symbols = list(_symbols.keys())

                # If it is the metal-containing molecule, store the indices.
                if metal_label in _symbols:

                    # Define how many lines need to be read
                    _lines_to_read = xyzp.count_n_atoms(
                        line.split()[1].split('_')[0]
                    )

                    # Skip one line
                    line = next(f)

                    for j in range(_lines_to_read):

                        _indices_CASSCF_mol.append(int(line.split()[1]))

                        # Check for EOF
                        try:
                            line = next(f)
                        except EOFError:
                            break

                    # After storing the first found, break the loop.
                    break

                # If it not the cation, move on.
                else:
                    continue

    return _indices_CASSCF_mol


def get_index_central_atom(supercell_labels, indices_CASSCF, metal_label):
    '''
    Get the supercell atom indices of the molecule to be treated at CASSCF
    level

    Parameters
    ----------
        supercell_labels : list
            Atomic symbols of supercell.
        indices_CASSCF   : list
            Supercell atom indices of CASSCF molecule.
        metal_label : str
            Atomic label of paramagnetic central metal ion
    Returns
    -------
        int
            Index of in supercell list of central metal.
    '''

    for it, symbol in enumerate(supercell_labels[indices_CASSCF]):
        if symbol == metal_label:
            _index_central = indices_CASSCF[it]

    return _index_central


def create_xfield(sp_coords, _indices_charge_dipole, _indices_CASSCF,
                  folder=None):
    '''
    Generate the xfield content to be passed to `generate_input()`

    Parameters
    ----------
        sp_coords : np.ndarray
            Supercell cartesian coordinates
        _indices_charge_dipole : dict
            Collection of charges and dipoles of translation-related atoms
                keys: supercell atom indices used in Gaussian jobs
                vals: tuple containing
                      supercell indices (list) related by translation to key
                      charge (int) of key atom
                      dipoles (np.ndarray) of key atom
        indices_CASSCF : list
            Supercell atom indices of CASSCF molecule
        folder : str, optional
            Path to subfolder where the input is being generated

    Raises
    -------
        Error : When the sum of atoms in XFIELD and CASSCF does not add up to
                the total number of atoms in the supercell.

    Returns
    -------
        list
            Nested lists of
                cartesian coordinates (3), charge (1) and dipoles (3)
    '''

    _xfield = []

    # Define a set to keep track of visited atoms
    # Same atom can be related by translation to more than one unique atom
    # (of different full molecules)
    visited = set()

    # Loop over supercell indices
    for key, val in _indices_charge_dipole.items():

        # Check whether key corresponds to an atom index belonging to the
        # central molecule
        if key in _indices_CASSCF:

            # Collect the info of translated-related atom indices.
            # val[0][1::] as val[0] contains the key.
            for index in val[0][1::]:

                # Store only if not visited already.
                if index not in visited:

                    _xfield.append(
                        np.hstack(
                            (
                                sp_coords[index],
                                _indices_charge_dipole[key][1],
                                _indices_charge_dipole[key][2]
                            )
                        )
                    )

                    visited.update(val[0])
                # if already visited, move on.
                else:
                    continue

        # no - loop over all the trans atom indices.
        else:

            for index in val[0]:

                # Store only if not visited already.
                if index not in visited:

                    _xfield.append(
                        np.hstack(
                            (sp_coords[index],
                             _indices_charge_dipole[key][1],
                             _indices_charge_dipole[key][2])
                           )
                       )

                # if already visited, move on.
                else:
                    continue

            visited.update(val[0])

    # Check atoms add up
    if len(_xfield) + len(_indices_CASSCF) != len(sp_coords):
        exit('\n*** Error ***\n\
 Inconsistency between total number of atoms in the supercell ({}) and the\
 sum of atoms in CASSCF and XFIELD sections ({} + {} = {}).\n\
 Folder: {}.'.format(len(sp_coords),
                     len(_indices_CASSCF),
                     len(_xfield),
                     len(_indices_CASSCF) + len(_xfield),
                     folder))

    return _xfield


# -------
# distort
# -------


def get_cell_to_modulate(user_args):
    '''
    Define the cell that will be distorted by Phonopy. Use the supercell
    expansion consistent with the calculation of FORCE_SETS.

    Parameters
    ----------
        user_args (object) : User-defined arguments from argparse.

    Returns
    -------
        _unitcell (object) : Instance of PhonopyAtoms class.
    '''

    # Instantiate a PhonopyAtoms object.
    poscar = read_vasp(
        user_args.POSCAR_file
    )

    # Instantiate a Phonopy object with the expansion used to calculate
    # FORCE_SETS.
    _unitcell = Phonopy(
        poscar,
        supercell_matrix=user_args.force_expansion
    )

    # Load FORCE_SETS
    _unitcell.set_displacement_dataset(
        parse_FORCE_SETS(
            filename=user_args.FORCE_SETS
        )
    )

    # Calculate force constants
    # Needed to calculate the DynamicalMatrix
    # and get phonons later (when modulated)
    _unitcell.produce_force_constants()

    return _unitcell


def get_qvectors(f_poscar, supercell_size):
    '''
    Calculate the commensurate q-vectors with supercell expansion (the big one,
    not the one used to calculate FORCE_SETS). These are the q-points at which
    Phonopy can calculate exactly the frequency, so they are a good set to
    integrate the Brillouin zone

    Parameters
    ----------
        f_poscar : str
            POSCAR file name
        supercell_size : list
            Supercell expansion as three integers
                e.g. [3 3 3]

    Returns
    -------
        list
            Nested lists of q-points
                e.g.: [[0.0, 0.0, 0.0],[0.5, 0.0, 0.0]]
    '''

    # Read structure.
    structure = read_vasp(f_poscar)

    # Construct a Phonopy object.
    phonon = Phonopy(structure, supercell_size)

    # Construct a DynmatToForceConstants object to access
    # the commensurate q-vectors of the SUPERCELL.
    _dynmat_to_fc = DynmatToForceConstants(
        phonon.get_primitive(),
        phonon.get_supercell()
       )

    # Get the commensurate q-points.
    _q_points = _dynmat_to_fc.commensurate_points

    return _q_points


def get_eq_rassi_energies(f_molcas, n_states):

    """
    Reads molcas output file of optimised structure to get RASSI energies

    Input:
        f_molcas      (str) : Molcas output file name of equilibrium structure
    Returns
    -------
        static_energies (array) : CASSCF-SO energies of the ground 6H15/2
                                  term (cm-1)
    """

    _energies = np.zeros(n_states)

    found = False

    with open(f_molcas, "r") as f:

        for line in f:
            if 'Eigenvalues of complex Hamiltonian:' in line:
                for _ in range(6):
                    line = next(f)
                for i in range(n_states):
                    _energies[i] = next(f).split()[-1]
                found = True

    if not found:
        os.error("Error: RASSI energies not found in molcas output")

    return _energies


def gen_dir_list(directories):

    with open('dir_list.txt', "w") as f:

        for subfolder in directories:
            f.write("{}\n".format(subfolder))

    return


def write_phonon_energy(folder, energy):

    with open(os.path.join(folder, 'phonon_energy.dat'), "w") as f:

        f.write("{} (cm-1)".format(energy))

    return


def flatten(_list_to_flatten):

    _flattened = [item for sublist in _list_to_flatten for item in sublist]

    if any(isinstance(el, list) for el in _flattened):
        _flattened = flatten(_flattened)

    return _flattened


if __name__ == '__main__':

    args = read_user_args()
