from .java import Segmenter
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('stanford_segmenter').version
except DistributionNotFound:
    __version__ = 'Undefined'

__all__ = ['__version__', 'Segmenter']
