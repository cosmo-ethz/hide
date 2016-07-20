
from collections import namedtuple

""" Axis definition of a beam """
AxisSpec = namedtuple("axis", ["elevation", "azimut", "frequencies"])

""" Beam definition """
BeamSpec = namedtuple("BeamSpec", ["ra", "dec", "pixels"])

ResponseSpec = namedtuple("ResponseSpec", ["pixel_idxs", "ra", "dec"])
