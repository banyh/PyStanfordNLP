from .java import Postagger
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('stanford_postagger').version
except DistributionNotFound:
    __version__ = 'Undefined'

__all__ = ['__version__', 'Postagger']
