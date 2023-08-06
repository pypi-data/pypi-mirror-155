from fractions import Fraction

import h5py
import numpy as np
from scipy.linalg import block_diag
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from molcas_suite.generate_input import MolcasComm, MolcasInput, Alaska, \
    Mclr, MolcasEmil
from angmom_suite.crystal import project_CF
from angmom_suite.basis import apply_unary, apply_binary, sf2ws, sf2ws_spin, \
    unitary_transform, eigh_perturbation, make_angmom_ops_from_mult
from .distortion import Distortion, Dx

ang2bohr = 1.88973


class LVC:

    def __init__(self, V0th, W1st, sf_smult=None, sf_amfi=None, sf_angm=None,
                 quax=None, ion=None, coords=None, verbose=False):

        # LVC data
        self.V0th = V0th
        self.W1st = W1st
        self.GS_ener = np.min([val for vals in V0th.values() for val in vals])
        self.nstate = sum([len(v0) for v0 in V0th.values()])

        # Spin multiplicities
        self.sf_smult = sf_smult

        self.sf_amfi = sf_amfi
        self.sf_angm = sf_angm

        self.quax = quax

        self.coords = coords

        if verbose:
            if self.coords is None:
                raise ValueError("Missing coords argument with verbose=True.")

            self.print_trans_rot_invariance()
            self.print_grad_norm()

    def print_grad_norm(self):

        num = len(self.W1st)
        fig, axes = plt.subplots(nrows=num, ncols=1, squeeze=False)
        fig.set_size_inches(4, num * 4)

        for idx, (mult, w1st) in enumerate(self.W1st.items()):
            grad_norm = np.linalg.norm(w1st, axis=(2, 3))
            axes[idx][0].title.set_text(f"Spin Multiplicity = {mult}")
            mat = axes[idx][0].matshow(grad_norm, norm=LogNorm())
            fig.colorbar(mat)

        plt.savefig("coupling_norm.pdf", dpi=600)

    def print_trans_rot_invariance(self):
        """Evaluates translational and rotational invariance along and around
        all three coordinate axes
        """

        num = len(self.W1st)
        nrm = np.sqrt(self.coords.shape[0])

        fig, axes = plt.subplots(nrows=num, ncols=3, squeeze=False)
        fig.set_size_inches(12, num * 4)

        for idx, (mult, w1st) in enumerate(self.W1st.items()):
            for vdx, (vec, lab) in enumerate(zip(np.identity(3), 'xyz')):
                inv = np.abs(np.einsum('ijkl,l->ij', w1st, vec / nrm)) / \
                             np.linalg.norm(w1st, axis=(2, 3))
                axes[idx][vdx].title.set_text(
                    f"axis = {lab}, Spin Multiplicity = {mult}")
                mat = axes[idx][vdx].matshow(inv, norm=LogNorm())
            fig.colorbar(mat, ax=axes[idx].tolist())

        plt.savefig("translational_invariance.pdf", dpi=600)

        fig, axes = plt.subplots(nrows=num, ncols=3, squeeze=False)
        fig.set_size_inches(12, num * 4)

        for idx, (mult, w1st) in enumerate(self.W1st.items()):
            for vdx, (ax, lab) in enumerate(zip(np.identity(3), 'xyz')):
                vec = np.array([np.cross(c, ax) for c in self.coords])
                inv = np.abs(np.einsum('ijkl,kl->ij', w1st,
                                       vec / np.linalg.norm(vec))) / \
                    np.linalg.norm(w1st, axis=(2, 3))
                axes[idx][vdx].title.set_text(
                    f"axis = {lab}, Spin Multiplicity = {mult}")
                mat = axes[idx][vdx].matshow(inv, norm=LogNorm())
            fig.colorbar(mat, ax=axes[idx].tolist())

        plt.savefig("rotational_invariance.pdf", dpi=600)

    @property
    def ws_spin(self):
        return np.array(make_angmom_ops_from_mult(self.sf_smult)[0:3])

    def to_file(self, f_lvc):

        with h5py.File(f_lvc, 'w') as h:

            # LVC data
            for mult in np.unique(self.sf_smult):
                mult_grp = h.create_group(str(mult))
                mult_grp.create_dataset('V0th', data=self.V0th[mult])
                mult_grp.create_dataset('W1st', data=self.W1st[mult])

            if self.sf_amfi is not None:
                h.create_dataset('SFS_AMFIint', data=self.sf_amfi)

            if self.sf_angm is not None:
                h.create_dataset('SFS_angmom', data=self.sf_angm)

            if self.sf_smult is not None:
                h.create_dataset('spin_mult', data=self.sf_smult)

            if self.quax is not None:
                h.create_dataset('quax', data=self.quax)

    @classmethod
    def from_file(cls, f_lvc):

        V0th = {}
        W1st = {}

        with h5py.File(f_lvc, 'r') as h:
            # Spin multiplicities
            sf_smult = h['spin_mult'][...]

            # LVC data
            for mult in np.unique(sf_smult):
                mult_grp = h[str(mult)]
                V0th[mult] = mult_grp['V0th'][...]
                W1st[mult] = mult_grp['W1st'][...]

            try:
                sf_amfi = h['SFS_AMFIint'][...]
            except KeyError:
                sf_amfi = None

            try:
                sf_angm = h['SFS_angmom'][...]
            except KeyError:
                sf_angm = None

            try:
                quax = h['quax'][...]
            except KeyError:
                quax = None

        return cls(V0th, W1st, sf_smult=sf_smult, sf_amfi=sf_amfi,
                   sf_angm=sf_angm, quax=quax)

    def evaluate_lvc_transformation(self, distortion, dx=Dx()):

        coords = distortion.evaluate() * ang2bohr

        V0 = [self.V0th[mult] for mult in np.unique(self.sf_smult)]
        W1 = [self.W1st[mult] for mult in np.unique(self.sf_smult)]

        # Introduce diagonal shift of sf energies to improve numerical accuracy
        # this is done per multiplicity (since there are no coupling elements
        # between roots of different spin)
        V_dia = [np.diag(v0 - v0[0]) + (np.einsum('ijkl,kl->ij', w1, coords)
                 if distortion else 0.0) for v0, w1 in zip(V0, W1)]
        V_grad = [np.einsum('ijkl,kl->ij', w1, dx.vectors() * ang2bohr)
                  if dx else None for w1 in W1]

        # todo: make pretty
        if dx:
            ener_shifted_vecs, T_sf_blks, ener_dx_vecs, T_sf_dx_blks = zip(
                *[eigh_perturbation(v, g) for v, g in zip(V_dia, V_grad)])
        else:
            ener_shifted_vecs, T_sf_blks, _, _ = zip(
                *[eigh_perturbation(v, g) for v, g in zip(V_dia, V_grad)])
            ener_dx_vecs = None
            T_sf_dx_blks = None

        # Undo diagonal shift to yield original absolute energies
        ener_vecs = [e + v0[0] for e, v0 in zip(ener_shifted_vecs, V0)]

        T_sf, T_sf_dx = apply_unary(lambda x: block_diag(*x), [T_sf_blks, T_sf_dx_blks])
        ener, ener_dx = apply_unary(np.concatenate, [ener_vecs, ener_dx_vecs])
        
        return ener, T_sf, ener_dx, T_sf_dx

    def evaluate_HSO_matrix(self, distortion, dx=Dx()):

        ener, T_sf, ener_dx, T_sf_dx = \
            self.evaluate_lvc_transformation(distortion, dx)

        _ener = ener - self.GS_ener

        _sf_amfi, _sf_amfi_dx = \
            unitary_transform(self.sf_amfi, T_sf, None, T_sf_dx)

        # todo: how to treat constant diagonal shift
        H_so, H_so_dx = apply_binary(
            lambda x, y: x + y,
            apply_unary(lambda x: sf2ws(np.diag(x), self.sf_smult),
                        [_ener, ener_dx]),
            apply_unary(lambda x: sf2ws_spin(1.j * x, self.sf_smult),
                        [_sf_amfi, _sf_amfi_dx])
        )

        return H_so, H_so_dx

    def evaluate_spin_orbit_coupling(self, distortion, dx=Dx()):
        H_so, H_so_dx = self.evaluate_HSO_matrix(distortion, dx)
        so_ener, soco, so_ener_dx, soco_dx = eigh_perturbation(H_so, H_so_dx)

        return so_ener, soco, so_ener_dx, soco_dx

    def evaluate_energy(self, soc, distortion, dx=Dx()):
        if soc:
            return self.evaluate_spin_orbit_coupling(distortion, dx)[0::2]
        else:
            return self.evaluate_lvc_transformation(distortion, dx)[0::2]

    def evaluate_Bkq(self, distortion, dx=Dx(), **kwargs):

        # evaluate LVC transformation
        ener, T_sf, ener_dx, T_sf_dx = \
                self.evaluate_lvc_transformation(distortion, dx)

        # evaluate SOC
        so_ener, soco, so_ener_dx, soco_dx = \
            self.evaluate_spin_orbit_coupling(distortion, dx)

        # Transform angmom operators to basis of distorted geometry
        sf_angm, sf_angm_dx = \
            unitary_transform(self.sf_angm, T_sf, None, T_sf_dx)

        ws_angm, ws_angm_dx = \
            apply_unary(sf2ws, [sf_angm, sf_angm_dx], self.sf_smult)

        # Transform angmom operators to SO-basis of distorted geometry
        so_angm, so_angm_dx = \
            unitary_transform(ws_angm, soco, ws_angm_dx, soco_dx)

        so_spin, so_spin_dx = \
            unitary_transform(self.ws_spin, soco, None, soco_dx)

        return [None if x is None else list(x.values()) for x in project_CF(
            so_ener, so_spin, so_angm, **kwargs, so_ener_dx=so_ener_dx,
            so_spin_dx=so_spin_dx, so_angm_dx=so_angm_dx)]


def generate_lvc_input(old_path, old_proj, num_root, jobiph_idx,
                       mclr_kwargs=None, alaska_kwargs=None):

    # Circular range generator from
    # https://stackoverflow.com/questions/40970290/circular-range-in-python
    def crange(start, end, modulo):
        if start > end:
            while start < modulo:
                yield start
                start += 1
            start = 0

        while start < end:
            yield start
            start += 1

    files = [
        MolcasEmil('copy', src, dest) for src, dest in [
            (f"{old_path}/{old_proj}.RunFile", "$Project.RunFile"),
            (f"{old_path}/{old_proj}.OneInt", "$Project.OneInt"),
            (f"{old_path}/{jobiph_idx}_IPH", "$Project.JobIph"),
            (f"{old_path}/{old_proj}.ChDiag", "$Project.ChDiag"),
            (f"{old_path}/{old_proj}.ChMap", "$Project.ChMap"),
            (f"{old_path}/{old_proj}.ChRed", "$Project.ChRed"),
            (f"{old_path}/{old_proj}.ChRst", "$Project.ChRst"),
            (f"{old_path}/{old_proj}.ChVec1", "$Project.ChVec1"),
            (f"{old_path}/{old_proj}.QVec00", "$Project.QVec00")
        ]
    ]

    input_name = r"lvc_root{:0" + str(len(str(num_root))) + r"}.input"

    for iroot in range(1, num_root + 1):

        inp = []

        if num_root % 2 == 0:
            if iroot <= num_root // 2:
                jrange = crange(
                    iroot % num_root,
                    (iroot + num_root // 2) % num_root,
                    num_root
                )

            else:
                jrange = crange(
                    iroot % num_root,
                    (iroot + num_root // 2 - 1) % num_root,
                    num_root
                )
        else:
            jrange = crange(
                iroot % num_root,
                (iroot + num_root // 2) % num_root,
                num_root
            )

        inp.append(MolcasComm('Gradient'))

        if mclr_kwargs:
            inp.append(Mclr(sala="{}".format(iroot), **mclr_kwargs))

        inp.append(Alaska(root="{}".format(iroot),
                          **{} if alaska_kwargs is None else alaska_kwargs))

        for jroot in jrange:

            inp.append(MolcasComm('Nonadiabatic coupling'))

            if mclr_kwargs:
                inp.append(Mclr(nac="{} {}".format(iroot, jroot + 1),
                                **mclr_kwargs))

            inp.append(Alaska(nac="{} {}".format(iroot, jroot + 1),
                              **alaska_kwargs or {}))

        MolcasInput(
            *files, *inp,
            title="LVC parametrisation generated by spin-phonon_suite"
        ).write(input_name.format(iroot))
