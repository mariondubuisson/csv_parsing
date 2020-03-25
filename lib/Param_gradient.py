import scipy.io as spio
from collections import namedtuple

GradientParameters = namedtuple(
    'GradientParameters', ['href', 'echelle', 'rugo'])


def param_from_matlab_file(place):
    mat = spio.loadmat(place)
    href = mat['href'].item()
    echelle = mat['echelle'].item()
    rugo = mat['rugo'].item()
    return [GradientParameters(href, echelle, rugo)]
