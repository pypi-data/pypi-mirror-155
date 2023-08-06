from setuptools import find_packages, setup
import sys
sys.path.append('kiraML')
from _version import __version__ 

setup(
    name='kiraML',
    packages=find_packages(include=['kiraML']),
    version=__version__,
    description='The KiraML library',
    author='Kira Learning',
    license='MIT',
    install_requires=['scikit-learn', 'matplotlib'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
