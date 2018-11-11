from setuptools import setup, find_packages

setup(
    name='sphinx-easypython',
    version='0.1',
    author='Julien Robert',
    author_email='julien.robert@univ-orleans.fr',
    packages=find_packages(),
    install_requires=['sphinx>=1.8'],
    dependency_links=['git+https://gitlab.com/jrobert/easypython-testeur.git#egg=easypython_testeur'],
)
