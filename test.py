from flask import Flask, request, render_template
# from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore


from rdflib import plugins
app = Flask(__name__)

#whatever webpage we want to connect and we name the function below it the same
@app.route("/homepage")
def homepage():
        return render_template("homepage.html")
    # elif request.method == 'POST':
    #     projectpath = request.form['projectFilepath']
    #     sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
    #     if projectpath is None or projectpath == " ":
    #         sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>
    #
    #                     SELECT ?node ?y WHERE{
    #
    #                       ?node auts:hasModel ?y.
    #
    #                     } LIMIT 5""")
    #     else:
    #         sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>
    #
    #                     SELECT ?node ?y WHERE{
    #
    #                       """ + projectpath + """ auts:hasModel ?y.
    #
    #                     } LIMIT 5""")
    #
    #     l = " "
    #     sparql.setReturnFormat(JSON)
    #     results = sparql.query().convert()
    #     # for result in results["results"]["bindings"]:
    #     #     l += (result["y"]["value"] + "\n")
    #     projectFilepath  = l
    #     detail = results
    #     return render_template('homepage.html', details=detail)



if __name__ == "__main__":
    app.run(debug=True)