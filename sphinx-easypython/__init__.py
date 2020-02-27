# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _
from docutils.parsers.rst import directives
import os
import requests
import json
import yaml

#os.environ['NO_PROXY'] = 'localhost'
API_URI = os.environ.get("PCAP_API_SERVER","pcap-api:8000/pcap")

class EasyPythonNode(nodes.Element):
    pass


class Exemples(nodes.Admonition, nodes.Element):
    pass


class EasyPythonDirective(Directive):

    def test_exercice(self, pathFichierModuleEns, options):
        from easypython_testeur.TesteurPython import TesteurPython
        if options["language"] == "python":
            print("Traitement du fichier" + str(pathFichierModuleEns))
            with open(pathFichierModuleEns, "rb") as fichier_module_ens:
                testeur = TesteurPython(fichier_module_ens.read(), "", False)
                # print(testeur.test())
                res = testeur.infos()
                if "messagesErreur" in res:
                    print("Fichier incorrect:")
                    for message_erreur in res["messagesErreur"]:
                        print("\t" + str(message_erreur))
                else:
                    print("\tLa fonction s'appelle : " +
                          res["nom_solution"])
                    if "solutions_visibles" in res:
                        print("\tENTREES VISIBLES DES ETUDIANTS:")
                        for (entree, sortie) in res["solutions_visibles"]:
                            print("\t\t" + res["nom_solution"] +
                                  "(" + str(entree) + ") renvoie " + str(sortie))
                    if "solutions_invisibles" in res:
                        print("\tENTREES INVISIBLES DES ETUDIANTS:")
                        for (entree, sortie) in res["solutions_invisibles"]:
                            print("\t\t" + res["nom_solution"] +
                                  "(" + str(entree) + ") renvoie " + str(sortie))
                return res

    def getExercice(self, pathFichierModuleEns, options):
        with open(pathFichierModuleEns, encoding='utf-8') as fichier:
            contenu = ''.join(fichier.readlines())
            headers = {'content-type': 'application/json'}
            payload = {'moduleEns': contenu, 'type': self.options["language"]}
            payload.update(options)
            res = requests.post("http://"+API_URI+"/api/v1/gestion_exercice/",
                                data=json.dumps(payload), headers=headers)
            try:
                dico = res.json()
                if 'traceback' in dico:
                    print(dico["traceback"])
                return dico
            except Exception as e:
                raise Exception("Requete: " + "http://"+API_URI+"/api/v1/gestion_exercice/" + "  reponse: "+ str(res.content))


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

    required_arguments = 1
    optional_arguments = 0


    def yaml_option(texte):
        try:
            return yaml.load(texte)
        except Exception as e:
            raise ValueError("JSON parse error :" + str(e))

    option_spec = {
        "language": directives.unchanged,
        "uuid": directives.unchanged,
        "titre": directives.unchanged,
        "nomclasse": directives.unchanged,
        "nom_classe_test": directives.unchanged,
        "extra_yaml": yaml_option,
    }

    possibleMeta = {"nomclasse", "nom_classe_test"}

    def run(self):
        env = self.state.document.settings.env
        (relative_filename, absolute_filename) = env.relfn2path(
            self.arguments[0])
        metas = {"nom_classe_test": os.path.basename(os.path.splitext(absolute_filename)[0])}
        metas.update({x: self.options[x]
                      for x in self.possibleMeta if x in self.options})
        if "extra_yaml" in self.options:
            metas["extra_yaml"] = self.options["extra_yaml"]
        self.options.update({"metainfos": metas})
        print("OPTIONS:" + str(self.options) + relative_filename)

        donnees = self.getExercice(absolute_filename, self.options) if env.app.config.easypython_production else {
            'hashCode': '1234',
            'metaInfos': self.test_exercice(absolute_filename, self.options),
            #{
            #      'arguments': ['argument_bidon', 'argument_bidon'],
            #      'solutions_visibles': [["exemple bidon", "sortie bidon"], ["exemple bidon", "sortie bidon"]],
            #      'nom_solution': 'fonction_bidon',
            #    }
        }
        if donnees.get("metaInfos",None) and "erreurs" in donnees["metaInfos"]:
            print("ATTENTION, des erreurs sont renvoyees par pcap-api:\n" + str(donnees["metaInfos"]["erreurs"]))
        if(self.options["language"] == "python"):
            zoneExercice = EasyPythonNode()
            exemples = Exemples()
            exemples["exemples"] = donnees["metaInfos"]["solutions_visibles"]
            zoneExercice["prototype_solution"] = "def " + donnees["metaInfos"]["nom_solution"] + \
                "(" + ','.join(donnees["metaInfos"]
                               ["arguments"]) + "):\n    return None"
            zoneExercice["hash"] = donnees["hashCode"]
            zoneExercice["language"] = self.options["language"]
            return [exemples, zoneExercice]
        if(self.options["language"] == "java"):
            zoneExercice = EasyPythonNode()
            zoneExercice["prototype_solution"] = "Votre classe.."
            zoneExercice["hash"] = donnees["hashCode"]
            zoneExercice["language"] = self.options["language"]
            return [zoneExercice]
        #if(self.options["language"] == "generique" or self.options["language"] == "IJVM" ):
        zoneExercice = EasyPythonNode()
        zoneExercice["prototype_solution"] = "Votre réponse"
        zoneExercice["hash"] = donnees["hashCode"]
        zoneExercice["language"] = self.options["language"]
        return [zoneExercice]


def visit_exemples_node(self, node):
    self.body.append("<ul class='list-group'>")
    for (entree, sortie) in node["exemples"]:
        self.body.append("<li class='list-group-item'> Sur l'entr&eacute;e <code>" + str(
            entree) + "</code> votre solution doit renvoyer <code>" + str(sortie) + "</code>.</li>")
    self.body.append("</ul>")


def visit_easypython_node(self, node):
    self.body.append("<div hash='" + node["hash"] + "' language='" +
                     node["language"] + "' class='easypython clearfix'>")
    self.body.append(node["prototype_solution"])
    self.body.append("</div>")


def depart_easypython_node(self, node):
    pass


def latex_departure(self, node):
    pass


def visit_latex(self, node):
    pass


def add_static(app,env,*reste):
    app.config.html_static_path.append(os.path.join(os.path.dirname(__file__),'_static'))
    app.config.html_context["easypython_api_route"]=app.config.easypython_api_route

def setup(app):
    app.add_css_file("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.27.4/codemirror.min.css")
    app.add_css_file("pcap_base.css")
    app.add_js_file("pcap.js")
    app.add_js_file("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.27.4/codemirror.min.js")
    app.add_js_file("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.27.4/mode/python/python.min.js")
    app.add_js_file("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.27.4/mode/clike/clike.min.js")
    app.connect('config-inited', add_static)
    
    app.add_config_value('easypython_production', "READTHEDOCS" in os.environ, 'html')
    #api_route = os.environ.get("PCAP_API_URI",'https://www.univ-orleans.fr/iut-orleans/informatique/intra/ap/api/v1/')
    api_route = os.environ.get("PCAP_API_URI",'/pcap/api/v1')
    app.add_config_value('easypython_api_route', api_route , 'html')
    app.add_node(EasyPythonNode, html=(visit_easypython_node,
                                       depart_easypython_node), latex=(visit_latex, latex_departure))
    app.add_node(Exemples, html=(visit_exemples_node,
                                 depart_easypython_node), latex=(visit_latex, latex_departure))

    app.add_directive('easypython', EasyPythonDirective)

    return {'version': '0.1'}   # identifies the version of our extension
