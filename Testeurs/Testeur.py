__author__ = 'julien'

import abc
import subprocess
import tempfile
import jsonpickle


# Le testeur doit générer un makefile avec une optin all et une option infos . Chaque option doit exécuter du code qui
# affiche du json

class Testeur():
    def __init__(self, codeTest, codeATester):
        self.codeTest = codeTest
        self.codeATester = codeATester

    @abc.abstractmethod
    def writeTestFiles(self, directory):
        return

    def test(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.writeTestFiles(tmpdirname)
            sortie = subprocess.run("cd "+tmpdirname+"; make -s all", shell=True, stdout=subprocess.PIPE)
            return jsonpickle.loads(sortie.stdout.decode(), keys=True)

    def infos(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.writeTestFiles(tmpdirname)
            sortie = subprocess.run("cd "+tmpdirname+"; make -s infos", shell=True, stdout=subprocess.PIPE)
            return jsonpickle.loads(sortie.stdout.decode(), keys=True)
