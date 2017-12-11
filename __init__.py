# coding: utf8
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _
from docutils.parsers.rst import directives
import os
import requests
import json

os.environ['NO_PROXY'] = 'localhost'

class EasyPythonNode(nodes.Element):
    pass

class Exemples(nodes.Admonition, nodes.Element):
    pass

class EasyPythonDirective(Directive):


    def testExercice(self, pathFichierModuleEns,options):
        from .Testeurs import TesteurPython
        if(options["language"]=="python"):
            print("Traitement du fichier"+str(pathFichierModuleEns))
            with open(pathFichierModuleEns,"rb") as e:
                testeur = TesteurPython(e.read(), "")
                #print(testeur.test())
                res = testeur.infos()
                if "messagesErreur" in res:
                    print("Fichier incorrect:")
                    for m in res["messagesErreur"]:
                        print("\t"+str(m))
                else:
                    print("\tLa fonction proposée s'appelle : " + res["nom_solution"])
                    if "solutions_visibles" in res:
                        print("\tENTREES VISIBLES DES ETUDIANTS:")
                        for (e,s) in res["solutions_visibles"]:
                            print("\t\t"+res["nom_solution"] + "(" + str(e) + ") renvoie " + str(s)) 
                    if "solutions_invisibles" in res:
                        print("\tENTREES INVISIBLES DES ETUDIANTS:")
                        for (e,s) in res["solutions_invisibles"]:
                            print("\t\t"+res["nom_solution"] + "(" + str(e) + ") renvoie " + str(s)) 
                return res


    def getExercice(self,pathFichierModuleEns,options):
        with open(pathFichierModuleEns) as fichier:
            contenu=''.join(fichier.readlines())
            headers = {'content-type': 'application/json'}
            payload={'moduleEns':contenu, 'type':self.options["language"]}
            payload.update(options)
            res=requests.post("http://localhost/api/v1/gestion_exercice/", data=json.dumps(payload), headers=headers)
            dico = res.json()
            if 'traceback' in dico:
                print(dico["traceback"])
            return dico

        """
        {'titre': 'mafonctino',
        'enonce': 'toto',
        'hashCode': '23f83f469056e5351613c4f6dc71c72b',
        'metaInfos':
           {
              'entrees_visibles': [[1, 2], [2, 3]],
              'arguments': ['x', 'y'],
              'solutions_visibles': [['1, 2', '1'], ['2, 3', '2']],
              'nom_solution': 'mafonctino',
              'messages': ['Solutions et entrees, tout y est !'],
              'temps': 0.005748748779296875,
              'solutions_invisibles': [[[1, 2], 1], [[2, 3], 2]],
              'entrees_invisibles': [[1, 2], [2, 3]]},
              'resource_uri': '/api/v1/gestion_exercice/23f83f469056e5351613c4f6dc71c72b/',
              'commentaires': '',
              'moduleEns': 'entrees_visibles = [\n        (1,2),\n        (2,3)\n]\nentrees_invisibles = [\n        (1,2),\n        (2,3)\n]\n\n@solution\ndef mafonctino(x,y):\n  return  x\n', 'auteur': '', 'date': '2016-10-21T09:28:42.557085', 'metaInfos': '{"solutions_invisibles": [[[1, 2], 1], [[2, 3], 2]], "messages": ["Solutions et entr\\u00e9es, tout y est !"], "arguments": ["x", "y"], "temps": 0.005748748779296875, "entrees_invisibles": [[1, 2], [2, 3]], "entrees_visibles": [[1, 2], [2, 3]], "nom_solution": "mafonctino", "solutions_visibles": [["1, 2", "1"], ["2, 3", "2"]]}'}
        """

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    option_spec = {
        "language": directives.unchanged,
        "uuid": directives.unchanged,
        "titre": directives.unchanged,
        "nomclasse": directives.unchanged,
    }

    possibleMeta = {"nomclasse"}
    def run(self):
        env = self.state.document.settings.env
        (relative_filename, absolute_filename)=env.relfn2path(self.arguments[0])
        metas = {"nomclasse" : os.path.basename(absolute_filename) }
        metas.update({x:self.options[x] for x in self.possibleMeta if x in self.options})
        self.options.update({"metainfos":metas})
        print("OPTIONS:" + str(self.options) + relative_filename )

        donnees= self.getExercice(absolute_filename,self.options) if env.app.config.easypython_production else {
        'hashCode': '1234',
        'metaInfos': self.testExercice(absolute_filename,self.options)
        #{
        #      'arguments': ['argument_bidon', 'argument_bidon'],
        #      'solutions_visibles': [["exemple bidon", "sortie bidon"], ["exemple bidon", "sortie bidon"]],
        #      'nom_solution': 'fonction_bidon',
        #    }
        }
        if(self.options["language"]=="python"):
            zoneExercice=EasyPythonNode()
            exemples=Exemples()
            exemples["exemples"]=donnees["metaInfos"]["solutions_visibles"]
            zoneExercice["prototype_solution"]="def " + donnees["metaInfos"]["nom_solution"] + "("+','.join(donnees["metaInfos"]["arguments"])+"):\n    return None"
            zoneExercice["hash"]= donnees["hashCode"]
            zoneExercice["language"]=self.options["language"]
            return [exemples, zoneExercice]
        if(self.options["language"]=="java"):
            zoneExercice=EasyPythonNode()
            zoneExercice["prototype_solution"]="Votre classe.."
            zoneExercice["hash"]= donnees["hashCode"]
            zoneExercice["language"]=self.options["language"]
            return [zoneExercice]

def visit_exemples_node(self, node):
        self.body.append("<ul class='list-group'>")
        for (entree,sortie) in node["exemples"]:
            self.body.append("<li class='list-group-item'> Sur l'entr&eacute;e <code>" + str(entree) + "</code> votre solution doit renvoyer <code>" + str(sortie) + "</code>.</li>")
        self.body.append("</ul>")

def visit_easypython_node(self, node):
        self.body.append("<div hash='"+node["hash"]+"' language='"+node["language"]+"' class='easypython clearfix'>")
        self.body.append(node["prototype_solution"])
        self.body.append("</div>")

def depart_easypython_node(self, node):
    pass

def latex_departure(self, node):
    pass
def visit_latex(self,node):
    pass

def setup(app):
    app.add_config_value('easypython_production', False, 'html')
    app.add_node(EasyPythonNode, html=(visit_easypython_node, depart_easypython_node), latex=(visit_latex, latex_departure))
    app.add_node(Exemples, html=(visit_exemples_node, depart_easypython_node),latex=(visit_latex, latex_departure))

    app.add_directive('easypython', EasyPythonDirective)

    return {'version': '0.1'}   # identifies the version of our extension
