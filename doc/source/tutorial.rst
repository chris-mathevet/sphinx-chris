Démarrage rapide (QuickStart)
===============================

Prérequis
++++++++++
Avoir virtualenv installé. (Sous ubuntu : ``sudo apt-get install virtualenv``)

Cela permet de créer un environnement de travail avec les outils spécifiques à la création du document.

Creation d'un virtualenv
+++++++++++++++++++++++++

Le virtualenv est stocké dans un dossier qu'il ne sera pas nécessaire de versionner, en exécutant : 

.. code::
        
        virtualenv -p python3 DOSSIERVENV

À chaque fois que vous souhaitez travailler "dans ce virtualenv", il faudra faire :

.. code::

        source DOSSIERVENV/bin/activate 


Installation de l'extension sphinx-easypython
----------------------------------------------

Au sein de ce virtualenv, installez sphinx-easypython et easypython_testeur :

.. code:: 

        pip install -e git+https://gitlab.com/jrobert/easypython-testeur.git#egg=easypython_testeur 
        pip install -e git+https://gitlab.com/jrobert/sphinx-easypython.git#egg=sphinx_easypython



Création du dépot
++++++++++++++++++

Initialisez un dépôt pour votre travail, par exemple :

.. code::

        mkdir NOMDOSSIER
        cd NOMDOSSIER
        git init


Créez un fichier readthedocs.yml contenant : 

.. code::

        build:
            image: latest

        python:
            version: 3.6
            setup_py_install: false



Créez un fichier requirements.txt :

.. code::

        pip freeze > requirements.txt

Créez le squelette de votre documentation : 

.. code::

        sphinx-quickstart

Avant de faire vos commit, n'oubliez pas de créer le fichier .gitignore qui va bien.

Poussez votre dépot git sur un dépot public.


Publication
+++++++++++++


Rendez vous sur `ReadTheDocs IUTO <http://info.iut45.univ-orleans.fr/>`_ . 

L'outil doit être suffisamment intuitif pour que vous arriviez à la publication.



