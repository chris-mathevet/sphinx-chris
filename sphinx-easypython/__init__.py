# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _
from docutils.parsers.rst import directives
import os
import requests
import json
import yaml
from docker_exerciseur.exerciseur import Exerciseur
from sphinx.util import logging

#os.environ['NO_PROXY'] = 'localhost'
API_URI = os.environ.get("PCAP_API_SERVER","pcap-api:8000/pcap")
logger = logging.getLogger(__name__)

class EasyPythonNode(nodes.Element):
    pass


class Exemples(nodes.Admonition, nodes.Element):
    pass


class EasyPythonDirective(Directive):

    def getExercice(self, pathDossierModuleEns, options):
        exerciseur = Exerciseur.avec_type(pathDossierModuleEns, self.options['language'], **(self.options.get("extra_yaml",{})))
        #        image = exerciseur.construire()
        files = {'moduleEns': exerciseur.empaquète().vers_cbor()}
        data = {"auteur" : "nobody", "titre":"default", "metaInfos": "{}", 'type': self.options["language"]}
        data.update(options)
        res = requests.post("http://"+API_URI+"/api/exercice/",
                                data=data, files=files)
        try:
            dico = res.json()
            logger.warning(dico)
            data["metaInfos"] = dico["metaInfos"]
            if 'traceback' in dico:
                logger.error((dico["traceback"]))
            return dico
        except Exception as e:
                raise Exception("Requete: " + "http://"+API_URI+"/api/exercice/" + "  reponse: "+ res.content.decode("utf-8"))

    required_arguments = 1
    optional_arguments = 0


    def yaml_option(texte):
        try:
            return yaml.safe_load(texte)
        except Exception as e:
            raise ValueError("YAML parse error :" + str(e))

    option_spec = {
        "language": directives.unchanged,
        "uuid": directives.unchanged,
        "titre": directives.unchanged,
        "nomclasse": directives.unchanged,
        "nom_classe_test": directives.unchanged,
        "extra_yaml": yaml_option,
        "tags": yaml_option,
    }

    possibleMeta = {"nomclasse", "nom_classe_test"}

    def run(self):
        if self.options["language"]=="python":
            self.options["language"] = "Jacadi"
        env = self.state.document.settings.env
        (relative_filename, absolute_filename) = env.relfn2path(
            self.arguments[0])
        metas = {"nom_classe_test": os.path.basename(os.path.splitext(absolute_filename)[0])}
        metas.update({x: self.options[x]
                      for x in self.possibleMeta if x in self.options})
        if "extra_yaml" in self.options:
            metas["extra_yaml"] = self.options["extra_yaml"]
        self.options.update({"metainfos": metas})
        logger.info("tags:" + str(self.options.get("tags",[])))
        logger.info("OPTIONS:" + str(self.options) + relative_filename)

        donnees = self.getExercice(absolute_filename, self.options) if env.app.config.easypython_production else {
            'hashCode': '1234',
            'metaInfos': {},
        }
        if donnees.get("metaInfos",None) and "erreurs" in donnees["metaInfos"]:
            logger.warning("ATTENTION, des erreurs sont renvoyees par pcap-api:\n" + str(donnees["metaInfos"]["erreurs"]))
        if(self.options["language"] in ["Jacadi"]):
            zoneExercice = EasyPythonNode()
            exemples = Exemples()
            entrees = donnees["metaInfos"].get("entrees_visibles", [])
            sorties = donnees["metaInfos"].get("sorties_visibles", [])
            exemples["exemples"] = sorties
            exemples["nom_solution"] = donnees["metaInfos"].get("nom_solution", "votre_fonction")
            exemples["arguments"] = donnees["metaInfos"].get("arguments", [])
            if "nom_solution" in donnees["metaInfos"] and "arguments" in donnees["metaInfos"]:
                zoneExercice["prototype_solution"] = "def " + donnees["metaInfos"]["nom_solution"] + \
                    "(" + ','.join(donnees["metaInfos"]
                                   ["arguments"]) + "):\n    return None"
            else:
                zoneExercice["prototype_solution"] = "Votre fonction"
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
        arguments = ", ".join(entree)
        appel = "{}({})".format(node["nom_solution"], arguments)
        self.body.append("<li class='list-group-item'> L'appel <code>" + appel + "</code> doit renvoyer <code>" + str(sortie) + "</code>.</li>")
    self.body.append("</ul>")

highlighting={"Jacadi":"python", "PackagePython": "python"}

def visit_easypython_node(self, node):
    self.body.append("<div hash='" + node["hash"] + "' language='" +
                     highlighting.get(node["language"], node["language"]) + "' class='easypython clearfix'>")
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
    app.add_css_file("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.59.4/codemirror.min.css")
    app.add_css_file("pcap_base.css")
    app.add_js_file("pcap.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/codemirror@5.59.4/lib/codemirror.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/codemirror@5.59.4/mode/python/python.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/codemirror@5.59.4/mode/clike/clike.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/rxjs@6.5.4/bundles/rxjs.umd.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/@convergence/convergence@1.0.0-rc.5/convergence.global.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/@convergence/input-element-bindings@0.3.4/browser/convergence-input-element-bindings.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/@convergence/color-assigner@0.3.0/umd/color-assigner.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/@convergencelabs/codemirror-collab-ext@0.1.2/umd/codemirror-collab-ext.min.js")
    app.add_js_file("https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js")
    app.connect('config-inited', add_static)

    app.add_config_value('easypython_production', "READTHEDOCS" in os.environ, 'html')
    api_route = os.environ.get("PCAP_API_URI",'/pcap/api/')
    app.add_config_value('easypython_api_route', api_route , 'html')
    app.add_node(EasyPythonNode, html=(visit_easypython_node,
                                       depart_easypython_node), latex=(visit_latex, latex_departure))
    app.add_node(Exemples, html=(visit_exemples_node,
                                 depart_easypython_node), latex=(visit_latex, latex_departure))

    app.add_directive('easypython', EasyPythonDirective)

    return {'version': '0.1'}   # identifies the version of our extension
