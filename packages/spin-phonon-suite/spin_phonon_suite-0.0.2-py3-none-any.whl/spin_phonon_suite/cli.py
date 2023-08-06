#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError, \
                     RawDescriptionHelpFormatter
import sys
import os
import re
import numpy as np

import xyz_py as xyzp
from molcas_suite.extractor import make_extractor as make_molcas_extractor
from gaussian_suite.extractor import make_extractor as make_gaussian_extractor
from hpc_suite.action import ParseKwargs, BooleanOptionalAction
from hpc_suite import parse_dict_key_only, parse_dict, SecondaryHelp
import angmom_suite

from .distortion import Distortion, Dx, DistortionInfo
from .derivative import Finite, print_tau_style
from .func import make_func
from .lvc import LVC, generate_lvc_input
from .vibrations import Harmonic


# Action for secondary function help message
class FunctionHelp(SecondaryHelp):
    def __call__(self, parser, namespace, values, option_string=None):

        if namespace.function == 'cfp':
            angmom_suite.read_args(['cfp', '--help'])
        else:
            raise ValueError("Supply valid option to function argument.")


def generate_distortion_func(args):

    labels, coords = xyzp.load_xyz(args.input)
    coords = np.array(coords)

    sp_data = DistortionInfo.from_file(args.distortion_info)

    coords = np.array(coords) + \
        sp_data.make_distortion(args.distortion.axes).evaluate()

    if args.origin:
        origin = [lab.split('.')[0] for lab in labels].index(args.origin)
        coords -= coords[origin]

    xyzp.save_xyz(args.output, labels, coords)


def init_func(args):
    sp_data = DistortionInfo.from_args(args)
    sp_data.to_file(args.distortion_info)


def lvc_func(args):

    sp_data = DistortionInfo.from_file(args.distortion_info)

    V0th = {}
    W1st = {}

    sf_smult = make_molcas_extractor(args.rassi, ("rassi", "spin_mult"))[()]
    ener = make_molcas_extractor(args.rassi, ("rassi", "SFS_energies"))[()]

    for smult, nroots in zip(*np.unique(sf_smult, return_counts=True)):
        V0th[smult] = ener[smult == sf_smult]
        W1st[smult] = np.zeros((nroots, nroots, sp_data.natoms, 3))

    for grad_file in args.grad:

        grad = make_molcas_extractor(grad_file, ("gradients", None))

        for lab, val in iter(grad):
            smult, root = lab
            W1st[smult][root-1, root-1] = val

        nacs = make_molcas_extractor(grad_file, ("nacs", "CI"))

        for lab, val in iter(nacs):
            smult, root1, root2 = lab
            W1st[smult][root1-1, root2-1] = W1st[smult][root2-1, root1-1] = val

    sf_amfi = make_molcas_extractor(args.rassi, ("rassi", "SFS_AMFIint"))[()]
    sf_angm = make_molcas_extractor(args.rassi, ("rassi", "SFS_angmom"))[()]
    coords = make_molcas_extractor(
        args.rassi, ("rassi", "center_coordinates"))[()]

    lvc = LVC(V0th, W1st, sf_smult=sf_smult, sf_amfi=sf_amfi, sf_angm=sf_angm,
              coords=coords, verbose=True)

    lvc.to_file(args.lvc_data)


def vib_func(args):

    ext = os.path.splitext(args.vib_output)[-1]

    if ext in ['.out', '.log']:
        log = args.vib_output
        freqs = make_gaussian_extractor(log, ("freq", "frequency"))[1]
        modes = make_gaussian_extractor(log, ("freq", "displacement"))[1]
        red_masses = make_gaussian_extractor(log, ("freq", "reduced_mass"))[1]

        if args.mass:
            raise ValueError("The --mass argument is not available with freq "
                             "data read from Gaussian text output.")

        ho = Harmonic(freqs, red_masses, modes)

    elif ext == '.fchk':
        fchk = args.vib_output
        hess = make_gaussian_extractor(fchk, ('fchk', 'hessian'))[()]
        masses = make_gaussian_extractor(fchk, ('fchk', 'atomic_mass'))[()]
        coords = make_gaussian_extractor(fchk, ('fchk', 'coordinates'))[()]

        for idx, mass in args.mass.items():
            masses[int(idx) - 1] = mass

        ho = Harmonic.analysis(hess, masses, coords=coords, trans=args.trans,
                               rot=args.rot)

    else:
        raise ValueError("Wrong file type. Gaussian output or formatted check"
                         "point file required.")
    subset = None if args.active_atoms is None else \
         [idx - 1 for idc in args.active_atoms for idx in idc]

    ho.subset_atoms(subset).to_file(args.vibration_info)


def summary_func(args):

    # read spin-phonon data
    sp_data = DistortionInfo.from_file(args.distortion_info)

    distortion_list = sp_data.generate_distortion_list()
    distortion_str = ' '.join([str(d) for d in distortion_list])

    distortion_count = len(distortion_list)

    if args.count:
        print(distortion_count)

    elif args.distortions:
        print(distortion_str)

    else:
        print("Number of distortion calculations: {}".format(distortion_count))
        print("Distortion list: {}".format(distortion_str))


def prepare_func(args, unknown_args):

    if args.program == 'tau':
        # CFP args
        if args.lvc_data:
            cfp_args = angmom_suite.read_args(['cfp'] + unknown_args)
            cfp_args.theta = True
            cfp_args.space = cfp_args.space or cfp_args.ion.casscf_terms('s')
            cfp_args.symbol = cfp_args.symbol or {
                'l': cfp_args.ion.ground_term,
                'j': cfp_args.ion.ground_level
                }[cfp_args.basis]
            func_kwargs = vars(cfp_args)

        else:
            func_kwargs = {}

        # derivative args
        setattr(args, 'function', 'CFPs')
        setattr(args, 'zpd_unit', True)
        setattr(args, 'order', 1)
        setattr(args, 'max_analytic_order', None)
        setattr(args, 'format', 'tau')

        # EQ_CFPs.dat
        kq_idc = angmom_suite.crystal.stevens_kq_indices[:27]
        cfp_vals = make_func(args, **func_kwargs)(Distortion(), Dx())
        cfp_data = np.column_stack((np.ones(27), kq_idc, cfp_vals))
        np.savetxt('EQ_CFPs.dat', cfp_data,
                   fmt=['%2d', '%2d', '% 2d', '%16.8f'])

        # CFP_derivatives.dat
        derivatives_func(args, **func_kwargs)

        # mode_energies.dat
        ho = Harmonic.from_file(args.vibration_info)
        np.savetxt('mode_energies.dat', ho.freqs, fmt='%16.8f',
                   header="Frequency (cm-1)", comments='')


def derivatives_func(args, unknown_args=None, **func_kwargs):

    if args.method == "findiff":
        dx = Finite.from_file(args.distortion_info)

    # parse extra function kwargs
    if not func_kwargs and unknown_args:
        if args.function == 'CFPs':
            func_kwargs = vars(angmom_suite.read_args(['cfp'] + unknown_args))
        elif not unknown_args:
            func_kwargs = {}
        else:
            raise ValueError("Unused extra arguments not known to the parser.")

    func = make_func(args, max_numerical_order=dx.order,
                     max_analytic_order=args.max_analytic_order, **func_kwargs)

    # prints derivatives and function values on the input grid
    if args.format == 'points':
        dx.write_points(
            args.function + "_points.dat", func, max_order=args.order)
        return

    ho = Harmonic.from_file(args.vibration_info)

    # remove normalisation and convert to units of zero point displacement
    conv = np.sqrt(ho.red_masses) * (ho.zpd if args.zpd_unit else 1.0)
    dQ = dx.transform(ho.displacements, func, args.order) * conv[:, np.newaxis]

    if args.format == 'tau':  # print central derivatives in tau style input

        if not args.order == 1:
            raise ValueError("Only first order derivatives with tau format.")

        if not args.function == 'CFPs':
            raise ValueError("Only function=CFPs possible with tau format.")

        print_tau_style(dQ, ho.freqs, 'CFP_polynomials.dat')

    else:  # print central derivatives to file
        pass


def generate_lvc_input_func(args):

    # todo: make prettier by parsing numbers directly to list of ints using
    # parse_range and a custom action which flattens, check also other uses of
    # parse_range if flattened

    # todo: replace dict by global definition
    roots_dict = {'dy': [18]}

    if args.num_roots:
        num_roots = [int(n) for n in args.num_roots]
    elif args.ion:
        num_roots = roots_dict[args.ion.lower()]
    else:
        sys.exit("Invalid specification of the number of roots.")

    iph_idc = range(1, len(num_roots) + 1) \
            if args.jobiph is None else [int(i) for i in args.jobiph]

    for num_root, iph_idx in zip(num_roots, iph_idc):
        if args.dry:
            input_name = r"lvc_root{:0" + str(len(str(num_root))) + r"}"
            print(' '.join([input_name.format(i) for i in range(1, num_root + 1)]))
        else:
            generate_lvc_input(args.old_path, args.old_project, num_root, iph_idx,
                               mclr_kwargs=args.mclr, alaska_kwargs=args.alaska)


def parse_range(string):
    """
    adapted from https://stackoverflow.com/questions/6512280/accept-a-range-of-
    numbers-in-the-form-of-0-5-using-pythons-argparse
    """

    # match numbers in hyphen separated range
    # capture first and second string of digits, don't capture hyphon
    splt = re.match(r'(\d+)(?:-(\d+))?$', string)

    if not splt:
        raise ArgumentTypeError("'" + string + "' is not a range of number. " +
                "Expected forms like '0-5' or '2'.")

    # extract start and end of range, if single number is given -> end = start
    start = splt.group(1)
    end = splt.group(2) or start

    return list(range(int(start), int(end)+1))


def read_args(arg_list=None):
    description = '''
    A package for dealing with Spin-Phonon coupling calculations.
    '''

    epilog = '''
    Lorem ipsum.
    '''

    parser = ArgumentParser(
            description=description,
            epilog=epilog,
            formatter_class=RawDescriptionHelpFormatter
            )

    subparsers = parser.add_subparsers(dest='prog')

    distort = subparsers.add_parser('generate_distortion')
    distort.set_defaults(func=generate_distortion_func)

    distort.add_argument('input', type=str,
            help='Input file containing the xyz-coordinates of the equilibrium structure.')

    distort.add_argument('output', type=str,
            help='Output file containing the xyz-coordinates of the distorted structure.')

    distort.add_argument('-D', '--distortion_info', type=str,
            help='HDF5 database file containing the normal mode displacement vectors.')

    distort.add_argument('--origin', type=str,
            help='Label of atom which stays fixed at the origin during distortion.')

    distort.add_argument('-d', '--distortion', required=True, type=Distortion.parse,
            help='Tuple consisting of <direction> (pos|neg) / <step_num> / <mode_index> ...')

    init = subparsers.add_parser('init')
    init.set_defaults(func=init_func)

    init.add_argument('-D', '--distortion_info', type=str,
            help='HDF5 database containing information about the distortion.')

    init.add_argument('--num_atoms', type=int, default=1,
            help='Number of atoms.')

    init.add_argument('--freq_gaussian', type=str,
            help='Gaussian output containing the normal mode information.')

    init.add_argument('--mode_wise', nargs='*', default=None, type=parse_range,
            help='Mode indices to be included in distortions calculations ' +
            '- activates mode-wise distortions.')

    init.add_argument('--atomic', nargs='*', default=None, type=parse_range,
            help='Atomic indices to be included in distortion calculations ' +
            '- activates atomic distortions.')

    init.add_argument('--num_steps', type=int, default=1,
            help='Number of distortion steps.')

    init.add_argument('--order', type=int, default=1,
            help='Order of distortion.')

    init.add_argument('--constant_step', type=float,
            help='Step size factor for constant displacement.')

    info = subparsers.add_parser('summary')
    info.set_defaults(func=summary_func)

    info.add_argument(
        '-D', '--distortion_info',
        help='HDF5 database containing the spin-phonon information.')

    select = info.add_mutually_exclusive_group(required=True)

    select.add_argument('--distortions', default=False, action='store_true',
            help='Print list of distortions.')

    select.add_argument('--count', default=False, action='store_true',
            help='Print number of distortions.')

    derive = subparsers.add_parser('derivatives')
    derive.set_defaults(func=derivatives_func)

    derive.add_argument(
        '-H', '--Help', action=FunctionHelp,
        help='show help message for additional arguments and exit'
    )

    derive.add_argument('function', type=str,
            help='Function to derive.')

    derive.add_argument('--method', type=str, default="findiff",
            choices=["findiff", "polynomial"],
            help='Differentiation method')

    evaluation = derive.add_mutually_exclusive_group(required=True)

    evaluation.add_argument('-G', '--grid_data', type=str,
            help='HDF5 database containing the function values at distorted geometries.')

    evaluation.add_argument('-L', '--lvc_data', type=str,
            help='HDF5 database containing the LVC parameters.')

    derive.add_argument('-V', '--vibration_info', type=str,
            help='HDF5 database containing information about the vibrations.')

    derive.add_argument('-D', '--distortion_info', type=str,
            help='HDF5 database containing the distortion information.')

    derive.add_argument('--order', type=int, default=1,
            help='Order of derivative.')

    derive.add_argument(
        '--max_analytic_order',
        type=int,
        help=('Maximum analytic derivative order available for function.'
              'Defaults to 0 for grid data and 1 for LVC function data.')
    )

    derive.add_argument(

        '--format',
        choices=['tau', 'points'],
        help='Output in <CFP_polynomials.dat> style.'
    )

    derive.add_argument('--zpd_unit', default=False, action='store_true',
            help='Convert to units of zero point displacement.')

    inp = subparsers.add_parser('generate_input')
    inp.set_defaults(func=generate_lvc_input_func)

    inp.add_argument('old_project', type=str,
            help='Project name of preceding Molcas calculation.')

    inp.add_argument('--old_path', type=str, default='../',
            help='Path to WorkDir of preceding Molcas calculation.')

    roots = inp.add_mutually_exclusive_group(required=True)

    roots.add_argument('--num_roots', nargs='+',
            help='Number of states per JOBIPH.')

    roots.add_argument('--ion', type=str,
            help='Label of the metal center, e.g. Dy.')

    inp.add_argument('--jobiph', nargs='+',
            help='Indices of Molcas JOBIPH wavefunction files *_IPH.')
    
    inp.add_argument(
        '--mclr',
        nargs='+',
        default=None,
        type=parse_dict_key_only,
        action=ParseKwargs,
        help='Manually run mclr with custom options, e.g. thre=1e-8',
        metavar='name=value')

    inp.add_argument(
        '--alaska',
        nargs='+',
        default=None,
        type=parse_dict_key_only,
        action=ParseKwargs,
        help='Run alaska with custom options, e.g. cuto=1e-8',
        metavar='name=value')

    inp.add_argument('--dry', default=False, action='store_true',
            help='Dry-run which prints files to be created')

    lvc = subparsers.add_parser('lvc')
    lvc.set_defaults(func=lvc_func)

    lvc.add_argument(
        '-D', '--distortion_info',
        type=str,
        help='HDF5 database containing information about the distortion.'
    )

    lvc.add_argument(
        '-L', '--lvc_data',
        type=str,
        help='HDF5 database output containing the LVC data.'
    )

    lvc.add_argument(
        '--grad',
        type=str,
        nargs='+',
        help='Molcas output file(s) containing gradients and NACs.'
    )

    lvc.add_argument(
        '--rassi',
        type=str,
        help=('Molcas *.rassi.h5 output file containing AMFI integrals, '
              'SF_ANGMOM operators and the spin multiplicities.')
    )

    vibrate = subparsers.add_parser('vib')
    vibrate.set_defaults(func=vib_func)

    vibrate.add_argument(
        '-V', '--vibration_info',
        type=str,
        help='HDF5 database containing information about the vibrations.'
    )

    vibrate.add_argument(
        '--vib_output',
        type=str,
        help='Output of a vibration calculation.'
    )

    vibrate.add_argument(
        '--mass',
        type=parse_dict,
        default={},
        nargs='+',
        action=ParseKwargs,
        help='Modify atomic masses for isotopic substitiution.',
        metavar='atom_index=mass'
    )

    vibrate.add_argument(
        '--trans',
        action=BooleanOptionalAction,
        default=True,
        help='Project out three rigid body translations.'
    )

    vibrate.add_argument(
        '--rot',
        action=BooleanOptionalAction,
        default=True,
        help='Project out three rigid body rotations.'
    )

    vibrate.add_argument(
        '--active_atoms',
        nargs='*',
        type=parse_range,
        help=('Atomic indices active during spin-phonon coupling. Effectively'
              ' subsets the displacement vectors. Useful if coupling is '
              'evaluated with a subset of the atoms present in the vibrational'
              ' calculation.')
    )

    prepare = subparsers.add_parser('prep')
    prepare.set_defaults(func=prepare_func)

    prepare.add_argument('program',
        choices=['tau'],
        help='Program for which to prepare inputs.')

    data = prepare.add_argument_group('database files')

    data.add_argument(
        '-G', '--grid_data',
        help=('HDF5 database containing the function values at distorted '
              'geometries.')
    )

    data.add_argument(
        '-L', '--lvc_data',
        help='HDF5 database containing the LVC parameters.')

    data.add_argument(
        '-V', '--vibration_info',
        help='HDF5 database containing information about the vibrations.')

    data.add_argument(
        '-D', '--distortion_info',
        help='HDF5 database containing the distortion information.')

    prepare.add_argument('--method', type=str, default="findiff",
            choices=["findiff", "polynomial"],
            help='Differentiation method')


    # If arg_list==None, i.e. normal cli usage, parse_args() reads from
    # "sys.argv". The arg_list can be used to call the argparser from the
    # back end.

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    _args, _ = parser.parse_known_args(arg_list)

    # select parsing option based on sub-parser
    if _args.prog in ['derivatives', 'prep']:
        args, hpc_args = parser.parse_known_args(arg_list)
        args.func(args, hpc_args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)


def main():
    read_args()
