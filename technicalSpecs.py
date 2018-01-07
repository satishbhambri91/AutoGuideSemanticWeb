from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
from json import JSONDecoder
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore

from rdflib import plugins

app = Flask(__name__)


# whatever webpage we want to connect and we name the function below it the same
@app.route("/technicalSpecs", methods=['GET', 'POST'])
def technicalSpecs():
    if request.method == 'GET':
        return render_template("technicalSpecs.html")
    elif request.method == 'POST':

        #input_func = raw_input()
        #input_func2 = raw_input()
        mfrName = request.form['mfrName']

       # mfrName = input_func(mfrName1)

        model = request.form['modelName']
        #model = input_func2(model1)
        year = request.form['year']

        sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                            SELECT ?cyl ?bore ?year ?stroke ?compRatio ?airAsp ?weight ?symboling WHERE{
                              ?node auts:hasMfrName """ + "\""+mfrName+"\"" """.
                              ?node auts:hasModel """ + "\""+model+"\"" """.
                              ?node auts:hasModelYear ?year.
                              ?node auts:hasCyl ?cyl.
                              ?node auts:hasAirAsp ?airAsp.
                              ?node auts:hasStroke ?stroke.
                              ?node auts:hasBore ?bore.
                              ?node auts:isGivenByWeight ?weight.
                              ?node auts:hasCompRatio ?compRatio.
                              ?node auts:basedOnSymboling ?symboling.
                            
                            } 
                            LIMIT 5""")

        l = []
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l.append(result["airAsp"]["value"])
            l.append(result["cyl"]["value"] )
            l.append(result["bore"]["value"] )
            l.append(result["stroke"]["value"] )
            l.append(result["compRatio"]["value"] )
            l.append(result["weight"]["value"] )
            l.append(result["symboling"]["value"])

        l = [s.encode('utf-8') for s in l]
        # projectFilepath = l
        detail = l
        return render_template('technicalSpecs.html', details=detail)


if __name__ == "__main__":
    app.run(debug=True)