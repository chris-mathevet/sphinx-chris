__author__ = 'julien'


import os
import subprocess
import json
import resource,psutil
import sys

nomClasse = sys.argv[1]


def limite_resources():
        pid = os.getpid()
        ps = psutil.Process(pid)
        resource.setrlimit(resource.RLIMIT_CPU, (4, 4))

def tester():
        resultat = {}
        classpath=".:"+"hamcrest-core-1.3.jar:"+"junit-4.12.jar"

        process = subprocess.Popen(["javac","-cp",classpath,nomClasse], stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=limite_resources)
        output, erreur_compilation_solution = process.communicate()
        if erreur_compilation_solution or process.returncode<0:
            resultat["Erreur de compilation"]=[erreur_compilation_solution.decode() if erreur_compilation_solution else "Arret de la compilation qui prenait trop de temps." ]
            return {"_valide":False, "_messages":resultat}


        process = subprocess.Popen(["javac","-cp",classpath,"MaClasseTest.java"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=limite_resources)
        output, erreur_compilation_test = process.communicate()
        if erreur_compilation_test or process.returncode<0:
            resultat["Erreur de compilation"]=[erreur_compilation_test.decode() if erreur_compilation_test else "Arret de la compilation qui prenait trop de temps." ]
            return {"_valide":False, "_messages":resultat}

        process = subprocess.Popen(["javac","-cp",classpath,"TesteurEasyPython.java"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=limite_resources)
        output, erreur_compilation_test = process.communicate()
        if erreur_compilation_test or process.returncode<0:
            resultat["Erreur de compilation"]=[erreur_compilation_test.decode() if erreur_compilation_test else "Arret de la compilation qui prenait trop de temps." ]
            return {"_valide":False, "_messages":resultat}

        process = subprocess.Popen(["java","-cp",classpath,"TesteurEasyPython"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=limite_resources)
        output, erreur_execution = process.communicate()

        if output:
            resultat["Votre code ne fait pas ce qui est attendu"]=[]
            for line in output.decode().splitlines():
                resultat["Votre code ne fait pas ce qui est attendu"].append(line)
            return {"_valide":False, "_messages":resultat}
        if erreur_execution:
            resultat["Erreur à l'exécution"]=[erreur_execution.decode()] # Est ce que ça peut arriver ??
            return {"_valide":False, "_messages":resultat}
        if process.returncode<0:
            resultat["Erreur à l'exécution"]=["Votre code a du être arrêté car prenait trop de temps"]
            return {"_valide":False, "_messages":resultat}
        return {"_valide":True, "_messages":{}}


if __name__ == "__main__":
    print(json.dumps(tester()))
