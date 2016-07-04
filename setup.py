from codecs import open
from setuptools import setup
from setuptools import find_packages

from libmt94x import __version__


def read_file(filepath):
    with open(filepath, 'rb+', 'utf-8') as f:
        content = f.read()

    return content.strip()


setup(
    name='libmt94x',
    description='This library generates bank statements in MT940/MT942 format',
    long_description=(
        '%s\n\n%s' % (
            read_file('README.rst'),
            read_file('HISTORY.rst'),
        )
    ),
    version=__version__,
    url='https://github.com/gingerpayments/libmt94x',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
