from setuptools import setup, find_packages

setup(
    name ='jhfunnycode',
    version = '1.0.0',
    description = 'life is fun',
    author = 'i_enable',
    author_email = None,
    url = None,
    install_requires = [],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)