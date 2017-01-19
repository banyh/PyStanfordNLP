from .java import Segmenter, conv2cn, conv2tw
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('stanford_segmenter').version
except DistributionNotFound:
    __version__ = 'Undefined'

__all__ = ['__version__', 'Segmenter', 'conv2cn', 'conv2tw']
