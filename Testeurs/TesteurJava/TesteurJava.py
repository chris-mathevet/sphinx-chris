__author__ = 'julien'
from ..Testeur import Testeur
from string import Template
import os
import shutil

TesteurEasyPython=Template("""
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class TesteurEasyPython {
    public static void main(String[] args) {
        Result result = JUnitCore.runClasses($NomClasseTest.class);
        for (Failure failure : result.getFailures()) {
            System.out.println(
                        (failure.getException()).getMessage()
                        );
        }
    }
}
""")



class TesteurJava(Testeur):

    def __init__(self, *args ):
        """
            entree : nomclasse, TestEnseignant, SolutionEtu
        """
        super().__init__(*args)
        self.nomClasse = "MaClasse.java"

    def writeTestFiles(self, directory):

        with open(os.path.join(directory,"MaClasseTest.java"),"w") as classe_test:
            classe_test.write(self.codeTest.decode())

        with open(os.path.join(directory,"TesteurEasyPython.java"),"w") as classe_testeur :
            classe_testeur.write(TesteurEasyPython.substitute({"NomClasseTest":"MaClasseTest"}))

        with open(os.path.join(directory,self.nomClasse),"w") as classe_solution:
            classe_solution.write(self.codeATester)

        with open(os.path.join(directory,"makefile"), "w") as file:
            file.write("all:\n\tpython3 scriptTesteurJava.py\n\ninfos:\n\techo {}")

        shutil.copyfile(os.path.join(os.path.dirname(__file__),"scriptTesteurJava.py"),\
                        os.path.join(directory,"scriptTesteurJava.py"))

        shutil.copyfile(os.path.join(os.path.dirname(__file__),"hamcrest-core-1.3.jar"),\
                        os.path.join(directory,"hamcrest-core-1.3.jar"))

        shutil.copyfile(os.path.join(os.path.dirname(__file__),"junit-4.12.jar"),\
                        os.path.join(directory,"junit-4.12.jar"))
