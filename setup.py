from setuptools import setup
from setuptools import find_packages


setup(
    name='ginger-libmt94x',
    description='This library generates bank statements in MT940/MT942 format',
    version=open('version.txt').read(),
    url='',
    packages=find_packages(),
    namespace_packages=['ginger'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Unidecode<0.5',
        'pycountry<2.0',
        'setuptools',
    ],
    extras_require={
        'test': [
            'nose',
            'mock',
        ],
        'develop': [
            'coverage',
            'flake8',
        ],
    }
)
