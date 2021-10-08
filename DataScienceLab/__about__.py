import os.path

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__commit__",
    "__author__",
    "__email__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "DataScienceLab"
__summary__ = "Collection of tools for working with Data Science"
__uri__ = "https://pypi.org/"

__version__ = "0.1.8"

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = "Mathias Brønd Sørensen"
__email__ = "mabrsr@rm.dk"
