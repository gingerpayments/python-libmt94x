from setuptools import setup
from setuptools import find_packages

from ginger_libmt94x import __version__


setup(
    name='ginger-libmt94x',
    description='This library generates bank statements in MT940/MT942 format',
    version=__version__,
    url='https://bitbucket.org/gingerpayments/ginger-libmt94x',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
