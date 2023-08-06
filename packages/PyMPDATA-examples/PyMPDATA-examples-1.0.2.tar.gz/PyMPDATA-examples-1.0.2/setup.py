""" the magick behind ``pip install ...`` """
from setuptools import setup, find_packages


def get_long_description():
    """ returns contents of README.md file """
    with open("README.md", "r", encoding="utf8") as file:
        long_description = file.read()
    return long_description


setup(
    name='PyMPDATA-examples',
    description='PyMPDATA usage examples reproducing results from literature'
                ' and depicting how to use PyMPDATA in Python from Jupyter notebooks',
    use_scm_version={"local_scheme": lambda _: "", "version_scheme": "post-release"},
    setup_requires=['setuptools_scm'],
    install_requires=['PyMPDATA',
                      'atmos_cloud_sim_uj_utils',
                      'pystrict',
                      'matplotlib',
                      'ipywidgets',
                      'scipy',
                      'pint',
                      'joblib',
                      'sympy',
                      'ghapi'],
    author='https://github.com/orgs/atmos-cloud-sim-uj/people',
    license="GPL-3.0",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=['PyMPDATA_examples', 'PyMPDATA_examples.*']),
    package_data={'': ['*/*/*.txt']},
    include_package_data=True
)
