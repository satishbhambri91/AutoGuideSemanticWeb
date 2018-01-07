from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore

from rdflib import plugins

app = Flask(__name__)


# whatever webpage we want to connect and we name the function below it the same
@app.route("/ratings", methods=['GET', 'POST'])
def ratings():
    if request.method == 'GET':
        return render_template("ratings.html")
    elif request.method == 'POST':
        # input_func = raw_input()
        # input_func2 = raw_input()
        mfrName = request.form['mfrName']

        # mfrName = input_func(mfrName1)

        model = request.form['modelName']
        # model = input_func2(model1)
        year = request.form['year']
        sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                                SELECT ?exterior ?interior ?comfort ?liability ?build ?overall WHERE{
                                  
                                  ?node auts:hasMfrName """ + "\""+mfrName+"\"" """.
                                  ?node auts:hasModel """ + "\""+model+"\"" """.
                                  ?node auts:basedOnInterior ?interior.
                                  ?node auts:basedOnExterior ?exterior.
                                  ?node auts:basedOnBuild ?build.
                                  ?node auts:basedOnComfort ?comfort.
                                  ?node auts:basedOnLiability ?liability.
                                  ?node auts:basedOnOverallRating ?overall.
                                  
                                } LIMIT 5""")

        l = []
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l.append(result["exterior"]["value"])
            l.append(result["interior"]["value"])
            l.append(result["comfort"]["value"])
            l.append(result["liability"]["value"])
            l.append(result["build"]["value"])
            l.append(result["overall"]["value"])

        l = [s.encode('utf-8') for s in l]
        detail = l
        return render_template('ratings.html', details=detail)


if __name__ == "__main__":
    app.run(debug=True)