from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='kasearch',
    version='0.0.1',
    description='Optimized tool for antibody sequence search',
    license='BSD 3-clause license',
    maintainer='Tobias Hegelund Olsen; Brennan Abanades Kenyon',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    maintainer_email='tobias.olsen@stats.ox.ac.uk',
    packages=find_packages(include=('kasearch', 'kasearch.*')),
    package_data={
        '': ['*.txt']
    },
    install_requires=[
        'numpy',
        'numba',
    ],
)
