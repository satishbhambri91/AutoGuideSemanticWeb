from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore


from rdflib import plugins
app = Flask(__name__)



# whatever webpage we want to connect and we name the function below it the same
@app.route("/performance", methods=['GET', 'POST'])
def performance():
    if request.method == 'GET':
        return render_template("performance.html")
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

                            SELECT ?mfr ?model ?rpm ?hp WHERE{
  
                            ?node auts:hasMfrName """ + "\""+mfrName+"\"" """.
                              ?node auts:hasModel """ + "\""+model+"\"" """.
                              ?node auts:hasHP ?hp.
                              ?node auts:hasRPM ?rpm.
                              
                              ?node1 auts:hasMfrName ?mfr.
                              ?node1 auts:hasModel ?model.
                              ?node1 auts:hasHP ?hp.
                              ?node1 auts:hasRPM ?rpm.
  
                            } LIMIT 5""")

        l = []
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l.append(result["mfr"]["value"])
            l.append(result["model"]["value"])
            l.append(result["rpm"]["value"])
            l.append(result["hp"]["value"])

        l = [s.encode('utf-8') for s in l]
        detail = l
        return render_template('performance.html', details=detail)



if __name__ == "__main__":
    app.run(debug=True)