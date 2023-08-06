import numpy as np
import h5py


C0 = np.float(299792458)
BOHR2M = np.float(5.29177210903e-11)
AMU = np.float(1.66053906660e-27)
HARTREE2J = np.float(4.3597447222071e-18)
H_PCK = np.float(6.62607015E-34)


class Harmonic:
    """Set of indenpendent quantum harmonic oscillators defined by their
    frequencies, displacements and reduced masses. The coordinate system
    follows the same conventions as the Gaussian software, i.e. the cartesian
    displacements are normalised and the normalisation constant is absorbed
    into the reduced mass.

    Parameters
    ----------
    freqs : np.array
        Array of harmonic frequencies in cm^-1.
    displacements : np.array
        K x N x 3 array containing the normalised displacement vectors.
    red_masses : np.array
        Array of the reduced masses.

    Attributes
    ----------
    freqs : np.array
        Array of harmonic frequencies in units of cm^-1.
    displacements : np.array
        K x N x 3 array containing the normalised displacement vectors.
    red_masses : np.array
        Array of the reduced masses in units of amu.
    natoms : int
        Number of atoms.
    nmodes : int
        Number of modes.
    force_const : np.array
        Array of force constants in units of mdyne/ang or N/cm.
    zpd : np.array
        Array of zero point displacements in ang.
    """

    def __init__(self, freqs, red_masses, displacements):
        self.freqs = freqs
        self.displacements = displacements
        self.red_masses = red_masses

        if not (displacements.shape[0] == freqs.shape[0] and
                displacements.shape[0] == red_masses.shape[0]):
            raise ValueError("Dimensions of HO parameters do not match.")

        self.natoms = displacements.shape[1]
        self.nmodes = displacements.shape[0]

    @property
    def force_const(self):
        # 10^5: N -> milliDyne, 10^-10: m^-1 -> ang^-1
        # final unit: mDyne/ang or N/cm
        return 1e8 * 1e-10 * \
            (2 * np.pi * self.freqs * 100)**2 * C0**2 * self.red_masses * AMU

    @property
    def zpd(self):
        # 10^10: m -> ang
        return 1e10 * np.sqrt(H_PCK * self.freqs * C0 / self.force_const)

    def to_file(self, h_file):

        with h5py.File(h_file, 'w') as h:
            h['/'].attrs.create('num_modes', self.natoms)
            h['/'].attrs.create('num_atoms', self.natoms)
            h.create_dataset('displacements', data=self.displacements)
            h.create_dataset('frequencies', data=self.freqs)
            h.create_dataset('reduced_masses', data=self.red_masses)

    def subset_atoms(self, active_atom_idc=None):
        if active_atom_idc is None:
            return self
        else:
            return self.__class__(self.freqs, self.red_masses,
                                  self.displacements[:, active_atom_idc])

    @classmethod
    def from_file(cls, h_file):

        with h5py.File(h_file, 'r') as h:
            displacements = h['displacements'][...]
            freqs = h['frequencies'][...]
            red_masses = h['reduced_masses'][...]

        return cls(freqs, red_masses, displacements)

    @classmethod
    def analysis(cls, hessian, masses, trans=True, rot=True, coords=None):

        natom = masses.shape[0]

        mwhess = hessian / np.sqrt(np.repeat(masses, 3)[np.newaxis, :] *
                                   np.repeat(masses, 3)[:, np.newaxis])

        eig, vec = np.linalg.eigh(mwhess)

        if trans:
            tra_frame = [np.array([d * np.sqrt(m) for m in masses for d in v])
                         for v in np.identity(3)]
            ntra = 3
        else:
            tra_frame = []
            ntra = 0

        if rot:
            # compute principle axis frame
            nrot, _, vec_inertia = principle_axis_inertia(masses, coords)

            # convert coordinates to principle axis frame
            # _coords = shift_to_com(masses, coords) @ vec_inertia.T
            _coords = shift_to_com(masses, coords)

            rot_frame = \
                [np.array([d * np.sqrt(m) for m, c in zip(masses, _coords)
                           for d in np.cross(c, v)])
                 for v in vec_inertia[:, (3 - nrot):].T]
        else:
            rot_frame = []
            nrot = 0

        nrotra = ntra + nrot
        nmodes = 3 * natom - nrotra

        rotra_frame = \
            np.array([d / np.linalg.norm(d) for d in tra_frame + rot_frame])

        if len(rotra_frame) != 0:
            # detect rigid body motions
            int_mask = np.logical_not(np.isclose(
                np.sum((rotra_frame @ vec)**2, axis=0), 1.0, rtol=1e-1))
            # Schmidt orthogonalisation
            new_frame, _ = np.linalg.qr(
                np.column_stack((rotra_frame.T, vec[:, int_mask])))
            # set coordinate frame to internal coordiantes
            frame = new_frame[:, nrotra:]

            # transfrom Hessian to internal coordinate frame and project out
            # rigid body motions
            eig, vec = np.linalg.eigh(frame.T @ mwhess @ frame)
            cart = frame @ vec / np.sqrt(np.repeat(masses, 3)[:, np.newaxis])

        else:
            cart = vec / np.sqrt(np.repeat(masses, 3)[:, np.newaxis])

        freqs = np.sqrt(eig * (HARTREE2J / BOHR2M**2 / AMU) /
                        (4*np.pi**2 * C0**2) + 0.j) / 100
        _freqs = np.vectorize(lambda x: -x.imag if x.imag else x.real)(freqs)

        red_masses = 1 / np.sum(cart**2, axis=0)
        displacements = \
            np.reshape((cart * np.sqrt(red_masses)).T, (nmodes, natom, 3))

        return cls(_freqs, red_masses, displacements)


def shift_to_com(masses, coords):
    com = np.sum(masses[:, np.newaxis] * coords, axis=0) / np.sum(masses)
    return coords - com


def principle_axis_inertia(masses, coords):

    _coords = shift_to_com(masses, coords)

    inertia = np.zeros((3, 3))
    inertia[0, 0] = np.sum(masses * (_coords[:, 1]**2 + _coords[:, 2]**2))
    inertia[1, 1] = np.sum(masses * (_coords[:, 2]**2 + _coords[:, 0]**2))
    inertia[2, 2] = np.sum(masses * (_coords[:, 0]**2 + _coords[:, 1]**2))
    inertia[1, 0] = -np.sum(masses * (_coords[:, 0] * _coords[:, 1]))
    inertia[2, 0] = -np.sum(masses * (_coords[:, 0] * _coords[:, 2]))
    inertia[2, 1] = -np.sum(masses * (_coords[:, 1] * _coords[:, 2]))
    inertia[0, 1] = inertia[1, 0]
    inertia[0, 2] = inertia[2, 0]
    inertia[1, 2] = inertia[2, 1]

    eig_inertia, vec_inertia = np.linalg.eig(inertia)
    rank = np.linalg.matrix_rank(inertia)

    if rank > 1:
        return rank, eig_inertia, vec_inertia
    else:
        raise ValueError("Rank of moment of inertia tensor smaller than one.")

