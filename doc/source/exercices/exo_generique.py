import jsonpickle
import sys

entree = sys.stdin.readline()

def test_entree(entree):
    try:
        valeur = int(entree)
        if valeur > 3:
            return jsonpickle.dumps({"_valide": True , "_messages":{}})
        else:
            return jsonpickle.dumps({"_valide": False , "_messages":{"erreur":["Vous avez bien renvoyé un entier, mais il n'est pas strictement supérieur à 3"]}})
    except Exception as e:
        return jsonpickle.dumps({"_valide": False , "_messages":{"erreur":["Vous devez entrer un entier."]}})
    

print(test_entree(entree))
