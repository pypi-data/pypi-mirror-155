from setuptools import setup, find_packages

setup(
    name ='jhfunnycode',
    version = '1.0.1',
    description = 'life is fun',
    author = 'i_enable',
    author_email = None,
    url = None,
    install_requires = [],
    package_dir={"": "jhfunny"},
    packages=find_packages(where="jhfunny"),
)
