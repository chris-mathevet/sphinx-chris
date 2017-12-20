from setuptools import setup, find_packages

setup(
    name='sphinx-easypython',
    version='0.1',
    author='Julien Robert',
    author_email='julien.robert@univ-orleans.fr',
    packages=find_packages(),
    install_requires=[],
    dependency_links=['https://gitlab.com/jrobert/easypython-testeur/master#egg=easypython-testeur-0.13'],
)
