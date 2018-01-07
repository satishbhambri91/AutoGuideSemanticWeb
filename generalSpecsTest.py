from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore

from rdflib import plugins

app = Flask(__name__)


# whatever webpage we want to connect and we name the function below it the same
@app.route("/generalSpecs", methods=['GET', 'POST'])
def generalSpecs():
    if request.method == 'GET':
        return render_template("generalSpecs.html")
    elif request.method == 'POST':
        mfrName = request.form['mfrName']

        # mfrName = input_func(mfrName1)

        model = request.form['modelName']
        # model = input_func2(model1)
        year = request.form['year']
        sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                            SELECT ?transmission ?highwayFuel ?cityFuel ?combinedFuel ?driveSys WHERE{
                              
                              ?node auts:hasMfrName """ + "\""+mfrName+"\""+ """.
                              ?node auts:hasModel """ + "\""+model+"\""+ """.
                              ?node auts:hasTransmission ?transmission.
                              ?node auts:givenByCity ?cityFuel.
                              ?node auts:givenByCombined ?combinedFuel.
                              ?node auts:givenByHighway ?highwayFuel.
                              ?node auts:hasDriveSys ?driveSys
                            
                              
                            } LIMIT 5""")

        l = []
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l.append(result["transmission"]["value"])
            l.append(result["highwayFuel"]["value"] )
            l.append(result["cityFuel"]["value"])
            l.append(result["combinedFuel"]["value"])
            l.append(result["driveSys"]["value"])

        l = [s.encode('utf-8') for s in l]
        detail = l
        return render_template('generalSpecs.html', details=detail)


if __name__ == "__main__":
    app.run(debug=True)