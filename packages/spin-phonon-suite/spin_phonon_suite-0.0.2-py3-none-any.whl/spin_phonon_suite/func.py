import h5py
import sys

from .distortion import Dx
from .lvc import LVC
from angmom_suite.multi_electron import Ion


def make_func(parser_args, max_numerical_order=None, max_analytic_order=None,
              **kwargs):

    if parser_args.grid_data and not parser_args.lvc_data:
        f_name = parser_args.grid_data
        max_analytic_order = \
            0 if max_analytic_order is None else max_analytic_order
        func_cls = HDF5reader

    elif parser_args.lvc_data and not parser_args.grid_data:
        f_name = parser_args.lvc_data
        max_analytic_order = \
            1 if max_analytic_order is None else max_analytic_order
        func_cls = LVCmodel

    else:
        raise ValueError("Provide one of: --grid_data or --lvc_data.")

    return func_cls(f_name, parser_args.function,
                    max_analytic_order=max_analytic_order,
                    max_numerical_order=max_numerical_order, **kwargs)


class Func:

    def __init__(self, item, max_analytic_order=0, max_numerical_order=0,
                 **kwargs):
        self.item = item
        self.max_analytic_order = max_analytic_order
        self.max_numerical_order = max_numerical_order
        self.max_order = (max_analytic_order or 0) + (max_numerical_order or 0)
        self.func_kwargs = kwargs

    def _func(self, distortion, dx=Dx()):
        pass

    def __call__(self, distortion, dx):
        self.check_order(distortion.order)
        return self._func(distortion, dx)

    def check_order(self, order):

        if order > self.max_order:
            raise ValueError(
                "Requested derivative order = {} higher than order of "
                "distortions = {}.".format(order, self.max_order))


class LVCmodel(Func):
    def __init__(self, file_name, item, max_analytic_order=1,
                 max_numerical_order=0, **kwargs):
        self.item = 'CFPs'

        lvc = LVC.from_file(file_name)

        if self.item == 'CFPs':
            self.func = lvc.evaluate_Bkq

        super().__init__(item, max_analytic_order=max_analytic_order,
                         max_numerical_order=max_numerical_order or 0,
                         **kwargs)

    def _func(self, distortion, dx=Dx()):
        return self.func(distortion, dx, **self.func_kwargs)[dx.order]


class HDF5reader(Func):

    def __init__(self, file_name, item, max_analytic_order=0,
                 max_numerical_order=1, **kwargs):
        self.file_name = file_name

        if kwargs:
            raise ValueError("Unresolved kwargs in HDF5reader.")

        super().__init__(item, max_analytic_order=max_analytic_order,
                         max_numerical_order=max_numerical_order)

    def _func(self, root, dx=Dx()):
        path = str(root)
        with h5py.File(self.file_name, 'r') as h:
            # read and format function data
            return h['{}/{}'.format(path, self.item)][...]
