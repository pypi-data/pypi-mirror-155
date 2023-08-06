import numpy as np
import h5py
import findiff
from itertools import combinations, product
from functools import reduce

from .distortion import Distortion, Dx, DistortionInfo


class Derivative(DistortionInfo):

    def sample_func(self, func, along, dx):
        """
        Sample function (derivative) values on grid.

        Parameters
        ----------
            func : callable
                Callable to compute values
            along : tuple of ints
                Distortion axes along which to read the function
            dx : Dx object
                Specifies directions and orders of analytic derivation

        Returns
        -------
            numpy.ndarray
                A N-dimensional array of which the first M dimensions span
                the distortion grid (2 * nsteps + 1), each containing the
                function data evaluated at that distortion point along the
                axes specified in 'along' indexed in the following way:
                -nsteps, -nsteps + 1, ..., 0, ..., +nsteps - 1, +nsteps.
                M is equal to the size of 'along'.
        """
        def grid(along, root=Distortion()):
            """
            Helperfunction which recursively traverses 'along' from the front
            to build function data grid for numerical derivation

            Parameters
            ----------
                along : tuple of ints
                    Distortion axes along which to compute the output
                root : Distortion object, optional
                    Recursively built distortion object
            """

            # todo: take into account non-square grids from order > 1
            if along:
                return np.array([
                    grid(along[1:], root + self.make_distortion({along[0]: i}))
                    for i in range(-self.nsteps, self.nsteps + 1)])
            else:
                print("Distortion: {:10} - Derivative: {:10}".format(
                    str(root), str(dx)), end='\r')
                return func(root, dx)

        return grid(along)

    def write_points(self, f_out, func, max_order=1):
        """
        Wrapper of write_dfun_dx() which generates the data header.

        Parameters
        ----------
            f_out : str
                Name of the output file
            func : callable
                Callable to compute values
            max_order : int, optional
                Maximum order of derivatives

        Returns
        -------
            None
        """
        with open(f_out, 'w') as f:
            f.truncate(0)

            func.check_order(max_order)

            # Generate data header
            f.write(' '.join(["md" + str(i+1) for i in range(max_order)] +
                             ["displ" + str(i+1) for i in range(max_order)] +
                             ["dx" + str(i+1) for i in range(max_order)] +
                             [func.item]) + '\n')

            self.write_dfun_dx(f, func, max_order)

    def write_dfun_dx(self, f, func, max_order):
        """
        Write derivative data to file

        Parameters
        ----------
            f : file object
                File object of the output file
            func : callable
                Callable to compute values
            max_order : int, optional
                Maximum order of derivatives

        Returns
        -------
            None
        """
        def write_values(along, order):
            # generate Dx object containing derivation information
            dx = sum([self.make_dx(a, o) for a, o in zip(along, order)], Dx())

            # calculate partial derivatives
            dfun_dx = self.calc_dfun_dx(func, along, dx)

            # generate fd sampling mesh
            fd_grd = np.meshgrid(
                    *([np.arange(-self.nsteps, self.nsteps+1)] * max_order),
                    indexing='ij')

            # shape of function evaluation
            fn_shape = dfun_dx.shape[max_order:]

            # generate function index mesh
            fn_grd = np.meshgrid(
                    *[np.arange(1, dim+1) for dim in fn_shape],
                    indexing='ij')

            for fd_idc, fun in zip(
                    zip(*[dim.flatten() for dim in fd_grd]),
                    dfun_dx.reshape((-1, *fn_shape))):

                for fn_idc, val in zip(
                        zip(*[dim.flatten() for dim in fn_grd]),
                        fun.flatten()):

                    f.write((
                        " {}" * max_order +  # output dimension
                        " {}" * max_order +  # distortion step
                        " {}" * max_order +  # derivation indices
                        " {}" +  # function value
                        " {}" * len(fn_shape) + '\n'  # function indices
                    ).format(*[m + 1 for m in along], *fd_idc, *order, val,
                             *fn_idc))

        def generate_order(num):
            # generate all ways to distribute max_order derivations among num axes
            return filter(lambda x: sum(x) <= max_order,
                          product(range(1, max_order + 1), repeat=num))

        # write function values
        for along in combinations(self.distortion_idc, max_order):
            write_values(along, (0,))

        # write derivative values
        for along in combinations(self.distortion_idc, max_order):
            for order in generate_order(len(along)):
                write_values(along, order)

    def compute_derivatives(self, func, order, along=()):
        """
        Calculates the derivative of a function at the centre of a uniform
        grid along multiple dimensions

        Parameters
        ----------
            func : callable
                Callable to compute values
            order : int
                order of derivation
            along : tuple of ints, optional
                Distortion axes along which to compute the output

        Returns
        -------
            numpy.ndarray
                N-dimensional array containing the N-th derivative element of
                the function along the distortion axes specified by its
                indices. N = order argument.
        """

        dim = len(along)

        func.check_order(order)

        if order == dim:
            # calculate function derivative in the centre of grid (i.e. eq)
            dx = sum([self.make_dx(a, 1) for a in along], Dx())
            return self.calc_dfun_dx(func, along, dx)[(self.nsteps,) * dim]

        elif order > dim:
            derivatives = [self.compute_derivatives(func, order, along+(i,))
                           for i in self.distortion_idc]
            return np.array(derivatives)

    def transform(self, basis, func, order=1):

        # function to recursively transform each dimension
        def trafo(dim):
            if dim == 0:
                return self.compute_derivatives(func, order)
            elif dim > 0:
                return np.einsum('ji,...ik->j...k', trans_mtx, trafo(dim - 1))

        # transformation matrix constituted of backtransformation to atomic
        # coordinates and transformation into the choosen basis
        trans_mtx = np.einsum(
            'ijk,ljk->il', basis, self.distortion_mtx[self.distortion_idc])

        return trafo(order)


def print_tau_style(derivatives, freqs, f_name):

    with open(f_name, 'w') as f:
        f.truncate(0)

        for mdx, freq in enumerate(freqs):

            f.write(("Vibration: {:d} Energy (cm-1): {} Rank (k), order (q) "
                     "and derivatives up to 3rd order\n").format(mdx+1, freq))

            for kdx, k in enumerate(range(2, 7, 2)):
                for qdx, q in enumerate(range(-k, k+1)):

                    # generate kq collective index
                    kq = kdx * (2*kdx + 3) + qdx

                    f.write(("{:^ d} {:^ d}  {: 14.9f}  {: 14.9f}  {: 14.9f}\n"
                             ).format(k, q, 0, 0, derivatives[mdx, kq]))


class Finite(Derivative):

    def calc_dfun_dx(self, func, along, dx):
        """
        Calculates the n-th derivative along specific distortions

        Parameters
        ----------
            func : callable
                Callable to compute values
            along : tuple of ints
                Distortion axes along which to compute the output
            dx : Dx object
                Specifies directions and orders of derivation

        Returns
        -------
            numpy.ndarray
                Derived function data in the shape as returned by sample_func()
        """

        analytic_dx, numerical_dx = dx.split(
                min(func.max_analytic_order, dx.order))

        # evaluate function values
        fun_vals = self.sample_func(func, along, analytic_dx)

        if numerical_dx.order == 0:
            # differential operator is identity
            diff_op = lambda x: x # todo: make prettier with Findiff package
        else:
            # generate differential operator
            diff_op = reduce(lambda x, y: x * y,
                [findiff.FinDiff(adx, self.steps[a], dx[a]) # todo: accuaracy
                 for adx, a in enumerate(along) if a in dx.keys()])

        return diff_op(fun_vals)


class Polynomial(Derivative):
    # Notes for Jon
    # -------------
    # use sample_func() to retrieve function values on a grid from HDF5
    # CFPs have to be present at (distortions/{pos,neg}/step/mode)
    # provide compute_derivatives() to be used as a api downstream
    # for debugging use --points flag which prints all values/dx to file
    pass
