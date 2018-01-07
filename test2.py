
from flask import Flask, render_template, json
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore





sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

    SELECT ?node ?y WHERE{

    ?node auts:hasModel ?y.

    } LIMIT 5""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#abc = json.loads(results)
for result in results["results"]["bindings"]:
    print (result["node"]["value"])
    print (result["y"]["value"])

#print abc