import re
import h5py
import numpy as np
from collections import defaultdict
from .vibrations import Harmonic

class DistortionInfo:

    def __init__(self, method, natoms, ndisto, distortion_idc,
                 distortion_mtx=None, order=1, nsteps=0, steps=None):

        self.method = method
        self.natoms = natoms
        self.ndisto = ndisto
        self.distortion_idc = distortion_idc
        self.order = order
        self.nsteps = nsteps
        self.steps = steps

        self._distortion_mtx = distortion_mtx

    @property
    def distortion_mtx(self):
        if self.method == 'atomic':
            return np.identity(3 * self.natoms).reshape((-1, self.natoms, 3))
        else:
            return self._distortion_mtx

    @classmethod
    def from_file(cls, h_file):

        with h5py.File(h_file, 'r') as h:
            method = h.attrs['method']
            natoms = h.attrs['num_atoms']
            ndisto = h.attrs['num_disto']
            distortion_idc = h['distortion_idc'][...]
            order = h.attrs['order']
            nsteps = h.attrs['num_steps']

            if nsteps > 0:
                steps = h['step_size'][...]
            else:
                steps = None

            try:
                distortion_mtx = h['distortion_mtx'][...]
            except KeyError:
                distortion_mtx = None

        return cls(method, natoms, ndisto, distortion_idc,
                   distortion_mtx=distortion_mtx, order=order,
                   nsteps=nsteps, steps=steps)

    @classmethod
    def from_args(cls, args):
        # parse distortion method
        method, ndisto, distortion_idc = resolve_distortion_method(args)

        if args.num_steps > 0:
            steps = resolve_step_sizes(args, args.num_atoms, distortion_idc)
        else:
            steps = None

        if method == 'mode_wise':
            distortion_mtx = \
                Harmonic.from_file(args.vibration_info).displacements
        else:
            distortion_mtx = None

        return cls(method, args.num_atoms, ndisto, distortion_idc,
                   distortion_mtx=distortion_mtx, order=args.order,
                   nsteps=args.num_steps, steps=steps)

    def to_file(self, h_file=None):

        with h5py.File(h_file, 'w') as h:
            h['/'].attrs.create('method', self.method)
            h['/'].attrs.create('num_atoms', self.natoms)
            h['/'].attrs.create('num_disto', self.ndisto)
            h.create_dataset('distortion_idc', data=self.distortion_idc)
            h['/'].attrs.create('order', self.order)
            h['/'].attrs.create('num_steps', self.nsteps)

            if self.steps is not None:
                h.create_dataset('step_size', data=self.steps)

            if self._distortion_mtx is not None:
                h.create_dataset('distortion_mtx', data=self._distortion_mtx)

    def generate_distortion_list(self, order=None, multi=[]):

        if order is None:
            order = self.order

        single = {Distortion((i, j))
                  for i in self.distortion_idc
                  for j in range(-self.nsteps, self.nsteps+1)}

        if order == 1:
            return single

        elif order > 1:
            multi = self.generate_distortion_list(order-1, multi)
            return {m + n for m in single for n in multi}

        else:
            raise ValueError("Distortion order out of range.")

    def make_distortion(self, axes):

        d = Distortion(
            *axes.items(),
            vec={axis: self.distortion_mtx[axis] for axis in axes.keys()},
            step={axis: self.steps[axis] if self.nsteps else None
                  for axis in axes.keys()}
        )

        return d

    def make_dx(self, axis, order):
        return Dx((axis, order), vec={axis: self.distortion_mtx[axis]})


class Direction:

    def __init__(self, *args, vec=None, step=None):
        axes = defaultdict(int)

        for along, order in sorted(args):
            axes[along] += order

        # filter zeros
        self.axes = dict(filter(lambda x: x[1] != 0, axes.items()))

        self.vec = {} if vec is None else {
            a: v for a, v in vec.items() if a in axes.keys()}
        self.step = {} if step is None else {
            a: s for a, s in step.items() if a in axes.keys()}

    def items(self):
        return self.axes.items()

    def keys(self):
        return self.axes.keys()

    def values(self):
        return self.axes.values()

    def __getitem__(self, key):
        return self.axes[key]

    def pop(self):
        axis, nsteps = list(self.items())[0]
        return self - self.__class__((axis, +1 if nsteps > 0 else -1))

    def split(self, n, _head=None):
        if _head is None:
            _head = self.__class__()

        if n > 0:
            tail = self.pop()
            head = _head + self - tail
            return tail.split(n - 1, head)
        else:
            return _head, self

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(*self.items(), *other.items(),
                                  vec={**self.vec, **other.vec},
                                  step={**self.step, **other.step})

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            inv = [(along, -order) for along, order in other.items()]
            return self.__class__(*self.items(), *inv,
                                  vec={**self.vec, **other.vec},
                                  step={**self.step, **other.step})

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.axes == other.axes

    # takes care of falsey
    def __len__(self):
        return len(self.axes)

    def __repr__(self):
        return '{}({})'.format(
                (self.__class__).__name__,
                ', '.join(['({}, {})'.format(a, n) for a, n in self.items()])
                )

    def __hash__(self):
        return hash(self.__repr__())


class Distortion(Direction):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = len(self.axes)

    def evaluate(self):
        return np.sum([self.vec[a] * self.step[a] * n
                       for a, n in self.items()], axis=0)
    
    @classmethod
    def parse(cls, string):
        # remove multiple occuring, leading and trailing '/'
        _str = re.sub('^\/', '', re.sub('\/$', '', re.sub('\/+', '/', string)))
        # split string at '/' and reshape to three column array
        distortion_raw = zip(*[iter(_str.split('/'))] * 3)

        # convert to correct types + convert to zero based distortion indexing
        distortion = sum([
                cls((int(d[2])-1, (1 if d[0] == 'pos' else -1) * int(d[1])))
                for d in distortion_raw], cls())

        return distortion

    def __str__(self):
        return '/'.join(['{}/{}/{}'.format(
                             'pos' if n > 0 else 'neg', abs(n), a+1)
                         for a, n in self.items()]) or '/'


class Dx(Direction):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.order = sum(self.values())

    def __str__(self):
        return '/'.join(['{}/{}'.format(a+1, n)
                         for a, n in self.items()]) or '/'

    def vectors(self):
        if self.order == 0:
            return None
        elif self.order == 1:
            return list(self.vec.values())[0]
        else:
            return [self.vec[key] for key in self.keys()]


def resolve_distortion_method(args):
    """Helper for the cli interface resolving the distortion method relevant
    arguments.
    """

    if args.mode_wise is not None:
        method = "mode_wise"

        distortion_idc = {int(m) - 1 for grp in args.mode_wise for m in grp}
        ndisto = len(distortion_idc)

    elif args.atomic is not None:
        method = "atomic"

        distortion_idc = {3 * (int(a) - 1) + c
                          for grp in args.atomic
                          for a in grp
                          for c in range(3)}
        ndisto = len(distortion_idc)

    else:
        raise ValueError("No distortion method specified.")

    return method, ndisto, list(distortion_idc)


def resolve_step_sizes(args, natoms, distortion_idc):

    step_list = [0.0 for _ in range(3 * natoms)]

    if args.constant_step:
        for idx in distortion_idc:
            step_list[idx] = args.constant_step

    else:
        print("Warning: Invalid step size specification. "
              "Only analytic derivatives.")

    return step_list
