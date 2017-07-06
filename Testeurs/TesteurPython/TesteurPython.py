__author__ = 'julien'

import os
import shutil
from ..Testeur import Testeur

PRELUDE_SOLUTION = """def solution(fun):
    fun.solution=True
    return fun

"""


class TesteurPython(Testeur):

    def writeTestFiles(self, directory):
        with open(os.path.join(directory,"makefile"), "w") as file:
            file.write("all:\n\tpython3 scriptTesteurPython.py\n\n")
            file.write("infos:\n\tpython3 scriptTesteurPython.py --infos")

        with open(os.path.join(directory,"ModuleEns.py"), "w") as file:
            file.write(PRELUDE_SOLUTION)
            file.write(self.codeTest.decode())
        with open(os.path.join(directory,"ModuleEtu.py"), "w") as file:
            file.write(self.codeATester)
        shutil.copyfile(os.path.join(os.path.dirname(__file__),"scriptTesteurPython.py"),\
                        os.path.join(directory,"scriptTesteurPython.py"))
