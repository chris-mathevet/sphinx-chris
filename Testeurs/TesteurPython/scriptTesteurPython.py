__author__ = 'julien'

import importlib
import sys
import traceback
import inspect
import time
import json

class resultats:
    def __init__(self):
        self._valide=True
        self._messages={}
        self._temps=None
    def invalide(self,raison,message):
        self._valide=False
        if raison in self._messages:
            self._messages[raison].append(message)
        else:
            self._messages[raison]=[message]
    def temps(self,t):
        self.temps=t
    def __repr__(self):
        if self._valide:
            return str(self._messages)
        return str(self._messages)
    def dumps(self):
        return json.dumps(self.__dict__)
    def to_dict(self):
        return self.__dict__
    def loads(chaine):
        d=json.loads(chaine)
        self._valide=d["_valide"]
        self._messages=d["_messages"]
        self._temps=d["_temps"]




old_stdout=None

def drop_stdout(f):
    def g(*args,**kwargs):
        global old_stdout
        try:
            (old_stdout,sys.stdout)=(sys.stdout,old_stdout)
            return f(*args,**kwargs)
        finally:
            (old_stdout,sys.stdout)=(sys.stdout,old_stdout)
    return g

class Erreur(Exception):
    def __init__(self,erreur,exception):
        self.erreur = erreur
        self.exception=exception


def remplir_ex(e,pile,limit=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    i=0
    while(exc_traceback.tb_next and i<pile):
        i=i+1
        exc_traceback=exc_traceback.tb_next
    fe=traceback.format_exception(exc_type, exc_value,exc_traceback,limit=limit)
    return (Erreur(str(e), str(''.join(fe))))

# reste pour l'exemple ? (à supprimer ?)
#def remplir_ex_syn(e):
#    return remplir_ex(e,100,limit=0)


## Prend en entree un nom de fichier et renvoie le module ouvert du fichier
@drop_stdout
def ouvre_module(fichier):
    try:
       module=importlib.import_module(fichier)
       return module
    except Exception as e:
       ex=remplir_ex(e,100,limit=0)
    raise ex

@drop_stdout
def test_fonction(fonction,entrees):
    """
    :param fonction:
    :param entrees: une liste d'entrees
    :return: liste de couples (entree,sortie)
    Leve une exception si besoin.
    """
    pile=traceback.extract_stack()
    try:
        res=[]
        for i in entrees:
            res.append((i,fonction(*i)))
        return res
    except Exception as e:
        ex=remplir_ex(e,len(pile)+3)
        raise ex


class ExercicePython:
    def charger_module(self,nom_module):
        try:
            self.module_ens=ouvre_module(nom_module)
            return True
        except Erreur as e:
            self.messagesErreur.append( str(e) )
            return False

    def parser_module(self):
        solution = [ (nom,fun) for nom,fun in self.module_ens.__dict__.items() if "solution" in dir(fun) ]

        if solution:
            (self.nom_solution,self.solution)=solution[0]
        else:
            print("ERREUR : le decorateur solution ne doit pas etre defini")
        self.arguments=inspect.getargspec(self.solution).args
        self.entrees_visibles=self.module_ens.__dict__.get("entrees_visibles",[])
        self.entrees_invisibles=self.module_ens.__dict__.get("entrees_invisibles",[])
        if all(not isinstance(i,tuple) for i in self.entrees_visibles):
            self.entrees_visibles=[(x,) for x in self.entrees_visibles]
        if all(not isinstance(i,tuple) for i in self.entrees_invisibles):
            self.entrees_invisibles=[(x,) for x in self.entrees_invisibles]

        if(solution and (self.entrees_visibles or self.entrees_invisibles)):
            self.messages.append( "Solutions et entrées, tout y est !" )
        else:
            if(self.entrees_visibles or self.entrees_invisibles):
                self.messagesErreur.append( "Il y a des entrées mais pas de quoi tester" )
                return False
            elif solution:
                self.messagesErreur.append( "Il faut des entrées")
                return False
            else:
                self.messagesErreur.append( "Il faut des entrées et de quoi tester" )
                return False
        if(self.entrees_visibles and not self.entrees_invisibles):
            self.messagesInfo.append( "Toutes les entrées sont visibles!" )
        if(self.entrees_invisibles and not self.entrees_visibles):
            self.messagesInfo.append("Toutes les entrées sont invisibles!")
        return True

    def tester_solution_ens(self):
        try:
            time0=time.time()
            self.solutions_visibles=test_fonction(self.solution,self.entrees_visibles)
            self.solutions_invisibles=test_fonction(self.solution,self.entrees_invisibles)
            temps=time.time()-time0
            self.temps=temps
            return True
        except Erreur as e:
            self.error=True
            self.messagesErreur.append( str(e) )
            return False

#    def afficher(self):
#        print(self.toDict())

    def toDict(self):
        attrs=["messages","messagesErreur","messagesInfo","entrees_visibles","entrees_invisibles","solutions_visibles","solutions_invisibles","temps","nom_solution","arguments"]
        res={attr:self.__dict__[attr] for attr in attrs if self.__dict__[attr] }
        res["solutions_visibles"]=[(str(list(x))[1:-1],str(y)) for (x,y) in self.solutions_visibles]
        res["solutions_invisibles"]=[(str(list(x))[1:-1],str(y)) for (x,y) in self.solutions_invisibles]
        return res

    def __init__(self,module):
        self.messages=[]
        self.messagesErreur=[]
        self.messagesInfo=[]
        self.module_ens=None
        self.entrees_visibles=[]
        self.entrees_invisibles=[]
        self.solutions_visibles=[]
        self.solutions_invisibles=[]
        self.temps=None
        self.solution=None
        self.nom_solution=None
        self.arguments=None
        self.module_charge=False
        if (self.charger_module(module) and self.parser_module()):
            self.module_charge=True
        self.tester_solution_ens()

    def tester_solution_etu(self,nom_module_etu):
        resultat=resultats()
        if not self.module_charge:
            resultat.invalide("Erreur","Impossible de charger la solution")
            return resultat
        try:
            module_etu=ouvre_module(nom_module_etu)
        except Erreur as e:
            resultat.invalide("Erreur",e.exception + " " + e.erreur)
            return resultat

        if not self.nom_solution in dir(module_etu):
            resultat.invalide("Vous n'avez pas respecté l'énoncé","Votre programme doit contenir une fonction "+self.nom_solution)
            return resultat
        try:
            time0=time.time()
            fonction_etudiant=getattr(module_etu,self.nom_solution)
            soletu_vi=test_fonction(fonction_etudiant,self.entrees_visibles)
            soletu_invi=test_fonction(fonction_etudiant,self.entrees_invisibles)
            temps=time.time()-time0
            resultat.temps(temps)
        except Erreur as e:
            resultat.invalide("Erreur d'exécution",e.exception + " "+e.erreur)
            return resultat
        zip_visibles=[x for x in zip(self.solutions_visibles,soletu_vi)]
        zip_invisibles=zip(self.solutions_invisibles,soletu_invi)

        for ((ent_ens,sor_ens),(ent_etu,sor_etu)) in zip_visibles:
            if sor_ens!=sor_etu :
                resultat.invalide("Votre fonction ne fait pas ce qui est attendu","Sur l'entrée "+repr(ent_ens)+" votre programme a renvoyé "+repr(sor_etu)+" alors qu'on attendait "+repr(sor_ens))

        for ((ent_ens,sor_ens),(ent_etu,sor_etu)) in zip_invisibles:
            if sor_ens!=sor_etu :
                resultat.invalide("Votre fonction ne fait pas ce qui est attendu","Votre fonction ne renvoie pas ce qui est attendu pour au moins une entrée invisible")
                break

        return resultat


if __name__ == "__main__" :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--infos", help="renvoie des informations sur le module enseignant",action="store_true")
    args = parser.parse_args()
    if args.infos:
        e = ExercicePython("ModuleEns")
        e.tester_solution_ens()
        print(json.dumps(e.toDict()))
    else:
        e = ExercicePython("ModuleEns")
        e.tester_solution_ens()
        print(e.tester_solution_etu("ModuleEtu").dumps())
