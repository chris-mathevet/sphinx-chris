import jsonpickle
import sys

entree = sys.stdin.readline()

def verifie(combinaison, combinaisonProp):
    combinaisonSol = combinaison[:]
    res={"blanc":0,"noir":0}
    for (indice, elem) in enumerate(combinaisonProp):
        if combinaisonSol[indice]==elem:
            res["blanc"] = res["blanc"]+1
            combinaisonSol[indice] = None
        elif elem in combinaisonSol:
            res["noir"]+=1
            combinaisonSol[combinaisonSol.index(elem)] = None
    return res


def feedback(combinaison, listeReponses):
    for (i, (combi, reponse)) in enumerate(listeReponses):
        rep = verifie(combinaison, combi)
        if rep!= reponse:
            return "Faux, cette combinaison donnerait " +  str(rep["noir"]) + " Noir et " + str(rep["blanc"]) + " Blanc sur la ligne " + str(i+1)
    return False


listeReponses = [(("G","J","G","R","B"),{"noir":3,"blanc":0}),
                (("R","J","V","B","G"),{"noir":3,"blanc":1}), 
                (("J","V","R","G","J"),{"noir":2,"blanc":1}),
                (("G","R","B","J","V"),{"noir":4,"blanc":0}),
                (("V","G","J","B","V"),{"noir":0,"blanc":3}),
                ]

def test_entree(entree):
    lettres = entree.split()
    if len(lettres)!=5:
            return jsonpickle.dumps({"_valide": False , "_messages":{"erreur":["Votre solution doit consister en 5 lettres majuscules, séparées par des espaces et correspondant aux couleurs des pions"]}})
    if(not set(lettres).issubset({"V","B","J","G","R"})):
            return jsonpickle.dumps({"_valide": False , "_messages":{"erreur":["Les seules couleurs valables sont R,V,B,J et G"]}})
    retours = feedback(lettres,listeReponses)
    if not retours :
        return jsonpickle.dumps({"_valide": True , "_messages":{}})
    else:
        return jsonpickle.dumps({"_valide": False , "_messages":{"erreur":[retours]}})

print(test_entree(entree))



