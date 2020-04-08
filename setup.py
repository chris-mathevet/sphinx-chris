from setuptools import setup, find_packages

setup(
    name='sphinx-easypython',
    version='0.21',
    author='Julien Robert',
    author_email='julien.robert@univ-orleans.fr',
    packages=find_packages(),
    install_requires=['sphinx>=1.8', 'PyYAML>=3', 'docker_exerciseur @ git+https://gitlab.com/FlorentBecker2/docker-exerciseur.git@dev#egg=docker_exerciseur'],
    dependency_links=['https://gitlab.com/jrobert/easypython-testeur.git#egg=easypython_testeur', 'https://gitlab.com/FlorentBecker2/docker-exerciseur.git@dev#egg=docker_exerciseur'],
)
