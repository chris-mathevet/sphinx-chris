from setuptools import setup, find_packages

setup(
    name='sphinx-easypython',
    version='0.21',
    author='Julien Robert',
    author_email='julien.robert@univ-orleans.fr',
    packages=find_packages(),
    install_requires=['sphinx>=1.8', 'PyYAML>=3', 'docker_exerciseur @ git+https://github.com/chris-mathevet/exerciseur-chris.git#egg=docker_exerciseur'],
    dependency_links=['https://github.com/chris-mathevet/exerciseur-chris.git#egg=docker_exerciseur'],
)
