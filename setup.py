from codecs import open
from setuptools import setup

from libmt94x import __version__


def read_file(filepath):
    with open(filepath, 'rb+', 'utf-8') as f:
        content = f.read()

    return content.strip()


CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
]


setup(
    name='python-libmt94x',
    version=__version__,
    author='Ginger Payments',
    author_email='dev@gingerpayments.com',
    description='This library generates bank statements in MT940/MT942 format',
    long_description=(
        '%s\n\n%s' % (
            read_file('README.rst'),
            read_file('HISTORY.rst'),
        )
    ),
    url='https://github.com/gingerpayments/python-libmt94x',
    license='MIT',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=['libmt94x'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Unidecode<0.5',  # translates unicode characters to ascii
        'pycountry<2.0',  # provides currency codes
    ],
)
