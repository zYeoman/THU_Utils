from setuptools import setup
from setuptools import find_packages

__author__  = "Yongwen Zhuang (zhuangyw.thu@gmail.com)"
__version__ = "0.0.4"
__license__ = "GPLv3"
__doc__     = "THU Utils: Tools for tsinghua students"

setup(
    name        = "thu_utils",
    version     = __version__,
    description = __doc__,
    author      = __author__,
    license     = __license__,
    package     = find_packages(),
    install_requires = [
        'lxml',
        'bs4',
        'prettytable',
        'requests'
    ],
)

