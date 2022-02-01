from setuptools import setup

setup(
    name="sequence",
    version="0.3.0",
    author="Xiaoliang Wu, Joaquin Chung, Alexander Kolar, Eugene Wang, Tian Zhong, Rajkumar Kettimuthu, Martin Suchara",
    author_email="xwu64@hawk.iit.edu, chungmiranda@anl.gov, akolar@anl.gov, eugenewang@yahoo.com, tzh@uchicago.edu, kettimut@mcs.anl.gov, msuchara@anl.gov",
    description="Simulator of Quantum Network Communication: SEQUENCE-Python is a prototype version of the official SEQUENCE release.",
    # packages = find_packages('src'),
    packages=['sequence', 'sequence.app', 'sequence.kernel', 'sequence.components',
              'sequence.network_management', 'sequence.entanglement_management', 'sequence.qkd',
              'sequence.resource_management', 'sequence.topology', 'sequence.utils'],
    package_dir={'sequence': 'src'},
    install_requires=[
        'numpy<1.22',
	    'matplotlib',
        'pandas',
        'qutip>=4.6.0',
        'tqdm>=4.54.0',
        'networkx',
        'mpi4py',
        'pytest-mpi',
    ],
)
