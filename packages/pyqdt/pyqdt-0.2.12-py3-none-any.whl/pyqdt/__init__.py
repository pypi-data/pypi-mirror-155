# -*- coding: utf-8 -*-

from .wraps import *
from .quotedata import *
# from .technical_analysis import *
import multiprocessing

try:
    if multiprocessing.get_start_method() != 'spawn':
        multiprocessing.set_start_method('spawn')
except:
    pass

__version__ = '0.2'

__all__ = [
    'JQWraps',
    'QuoteData',
    '__version__'
]
