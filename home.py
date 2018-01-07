from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
from rdflib.plugins import stores
from rdflib.plugins.stores import sparqlstore
from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def homepage():
        return render_template("homepage.html")

@app.route("/usedcars")
def usedcars():
        return render_template("usedcars.html")

# @app.route("/carsearch", methods=['GET', 'POST'])
# def carsearch():
#     return render_template('carsearch.html')

@app.route("/contactus")
def contactus():
        return render_template("contactus.html")

@app.route("/aboutus")
def aboutus():
        return render_template("aboutus.html")

@app.route("/pricing", methods=['GET', 'POST'])
def pricing():
    if request.method == 'GET':
        return render_template("pricing.html", details={})
    elif request.method == 'POST':

        # input_func = raw_input()
        # input_func2 = raw_input()
        minPrice = request.form['minPrice']

        # mfrName = input_func(mfrName1)

        maxPrice = request.form['maxPrice']
        # model = input_func2(model1)
        # year = request.form['year']
        sparql = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                                        SELECT ?cost ?model ?mfrName WHERE{

                                          ?node auts:hasMfrName ?mfrName.
                                          ?node auts:hasModel ?model.
                                          ?node auts:hasCost ?cost.
                                          FILTER((?cost > """ + "\"" + minPrice + "\"" + """ ) && (?cost < """ + "\"" + maxPrice + "\"" + """))
                                

                                        } LIMIT 5""")

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        i = 1
        l = defaultdict(dict)
        # l[i] = {}
        j = 0
        for k in results['results']['bindings']:
            j+=1


        for result in results['results']['bindings']:
            l[i]["Cost"] = (result["cost"]["value"])
            l[i]["Model"] = (result["model"]["value"])
            l[i]["MfrName"] = (result["mfrName"]["value"])
            # l = [s.encode('utf-8') for s in l]
            i+=1

        # l = [s.encode('utf-8') for s in l]
        detail = l

        return render_template("pricing.html", details=detail)


@app.route("/GeneralSpecifications", methods=['GET', 'POST'])
def GeneralSpecifications():
    if request.method == 'GET':
        return render_template("GeneralSpecifications.html", details = {})
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

                                    SELECT ?transmission ?highwayFuel ?cityFuel ?combinedFuel ?driveSys WHERE{

                                      ?node auts:hasMfrName """ + "\"" + mfrName + "\"" + """.
                                      ?node auts:hasModel """ + "\"" + model + "\"" + """.
                                      ?node auts:hasTransmission ?transmission.
                                      ?node auts:givenByCity ?cityFuel.
                                      ?node auts:givenByCombined ?combinedFuel.
                                      ?node auts:givenByHighway ?highwayFuel.
                                      ?node auts:hasDriveSys ?driveSys


                                    } LIMIT 5""")

        l = {}
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l["Transmission"] = (result["transmission"]["value"])
            l["Highway Fuel Average"] = (result["highwayFuel"]["value"])
            l["City Fuel Average"] = (result["cityFuel"]["value"])
            l["Combined Fuel"] = (result["combinedFuel"]["value"])
            l["Drive System"] = (result["driveSys"]["value"])

        #l = [s.encode('utf-8') for s in l]
        detail = l
        return render_template('GeneralSpecifications.html', details=detail)

@app.route("/TechnicalSpecifications", methods=['GET', 'POST'])
def TechnicalSpecifications():
    if request.method == 'GET':
        return render_template("TechnicalSpecifications.html", details={"Air ASP" : "NA", "Cylinders" : "NA", "Bore": "NA", "Stroke": "NA", "Compression Ratio" : "NA", "Weight":"NA", "Symboling": "NA" })
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

                            SELECT ?cyl ?bore ?year ?stroke ?compRatio ?airAsp ?weight ?symboling WHERE{
                              ?node auts:hasMfrName """ + "\"" + mfrName + "\"" """.
                              ?node auts:hasModel """ + "\"" + model + "\"" """.
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

        l = {}
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l["Air ASP"] = (result["airAsp"]["value"])
            l["Cylinders"] = (result["cyl"]["value"])
            l["Bore"] = (result["bore"]["value"])
            l["Stroke"] = (result["stroke"]["value"])
            l["Compression Ratio"] = (result["compRatio"]["value"])
            l["Weight"] = (result["weight"]["value"])
            l["Symboling"] = (result["symboling"]["value"])

        #l = [s.encode('utf-8') for s in l]
        # projectFilepath = l
        detail = l
        return render_template('TechnicalSpecifications.html', details=detail)


@app.route("/performance123", methods=['GET', 'POST'])
def performance123():
    if request.method == 'GET':
        return render_template("performance123.html", details={"Manufacturer":"NA", "Model":"NA", "RPM":"NA", "HorsePower": "NA"} )
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

                            ?node auts:hasMfrName """ + "\"" + mfrName + "\"" """.
                              ?node auts:hasModel """ + "\"" + model + "\"" """.
                              ?node auts:hasHP ?hp.
                              ?node auts:hasRPM ?rpm.

                              ?node1 auts:hasMfrName ?mfr.
                              ?node1 auts:hasModel ?model.
                              ?node1 auts:hasHP ?hp.
                              ?node1 auts:hasRPM ?rpm.

                            } LIMIT 1""")

        l = {}
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            l["Manufacturer"] = (result["mfr"]["value"])
            l["Model"] = (result["model"]["value"])
            l["RPM"] = (result["rpm"]["value"])
            l["HorsePower"] = (result["hp"]["value"])

        #l = [s.encode('utf-8') for s in l]
        detail = l


        return render_template('performance123.html', details=detail)


@app.route("/review", methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template("review.html", details={"Exterior":"NA", "Interior":"NA", "Comfort":"NA", "Liability": "NA", "Build" : "NA", "Overall_Rating" : "NA"})
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

                                  ?node auts:hasMfrName """ + "\"" + mfrName + "\"" """.
                                  ?node auts:hasModel """ + "\"" + model + "\"" """.
                                  ?node auts:basedOnInterior ?interior.
                                  ?node auts:basedOnExterior ?exterior.
                                  ?node auts:basedOnBuild ?build.
                                  ?node auts:basedOnComfort ?comfort.
                                  ?node auts:basedOnLiability ?liability.
                                  ?node auts:basedOnOverallRating ?overall.

                                } LIMIT 5""")

        l = {}
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # sparql.setReturnFormat(JSON)
        # results = sparql.query().convert()
        for result in results['results']['bindings']:
            l["Exterior"]= (result["exterior"]["value"])
            l["Interior"] = (result["interior"]["value"])
            l["Comfort"] = (result["comfort"]["value"])
            l["Liability"]=(result["liability"]["value"])
            l["Build"] = (result["build"]["value"])
            l["Overall_Rating"] = (result["overall"]["value"])

       # l = [s.encode('utf-8') for s in l]
        detail = l
        return render_template('review.html', details=detail)


@app.route("/compare", methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        return render_template("compare.html", details1={}, details2= {}, details3={})
    elif request.method == 'POST':
        # input_func = raw_input()
        # input_func2 = raw_input()
        mfrName1 = request.form['mfrName1']
        mfrName2 = request.form['mfrName2']
        mfrName3 = request.form['mfrName3']
        # mfrName = input_func(mfrName1)

        model1 = request.form['modelName1']
        model2 = request.form['modelName2']
        model3 = request.form['modelName3']
        # model = input_func2(model1)
        year1 = request.form['year1']
        year2 = request.form['year2']
        year3 = request.form['year3']

        sparql1 = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql1.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                                SELECT ?exterior ?interior ?comfort ?liability ?build ?overall WHERE{

                                  ?node auts:hasMfrName """ + "\"" + mfrName1 + "\"" """.
                                  ?node auts:hasModel """ + "\"" + model1 + "\"" """.
                                  ?node auts:basedOnInterior ?interior.
                                  ?node auts:basedOnExterior ?exterior.
                                  ?node auts:basedOnBuild ?build.
                                  ?node auts:basedOnComfort ?comfort.
                                  ?node auts:basedOnLiability ?liability.
                                  ?node auts:basedOnOverallRating ?overall.

                                } LIMIT 5""")

        l1 = {}
        sparql1.setReturnFormat(JSON)
        results1 = sparql1.query().convert()
        # sparql1.setReturnFormat(JSON)
        # results1 = sparql1.query().convert()
        for result in results1['results']['bindings']:
            l1["Exterior Ratings"] = (result["exterior"]["value"])
            l1["Interior Ratings"] = (result["interior"]["value"])
            l1["Comfort Ratings"] = (result["comfort"]["value"])
            l1["Liability Ratings"] = (result["liability"]["value"])
            l1["Build Ratings"] = (result["build"]["value"])
            l1["Overall Ratings"] = (result["overall"]["value"])

        #l1 = [s.encode('utf-8') for s in l1]
        detail1 = l1


        sparql2 = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql2.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                                        SELECT ?exterior ?interior ?comfort ?liability ?build ?overall WHERE{

                                          ?node auts:hasMfrName """ + "\"" + mfrName2 + "\"" """.
                                          ?node auts:hasModel """ + "\"" + model2 + "\"" """.
                                          ?node auts:basedOnInterior ?interior.
                                          ?node auts:basedOnExterior ?exterior.
                                          ?node auts:basedOnBuild ?build.
                                          ?node auts:basedOnComfort ?comfort.
                                          ?node auts:basedOnLiability ?liability.
                                          ?node auts:basedOnOverallRating ?overall.

                                        } LIMIT 5""")

        l2 = {}
        sparql2.setReturnFormat(JSON)
        results2 = sparql2.query().convert()
        # sparql2.setReturnFormat(JSON)
        # results2 = sparql2.query().convert()
        for result in results2['results']['bindings']:
            l2["Exterior Ratings"] = (result["exterior"]["value"])
            l2["Interior Ratings"] = (result["interior"]["value"])
            l2["Comfort Ratings"] = (result["comfort"]["value"])
            l2["Liability Ratings"] = (result["liability"]["value"])
            l2["Build Ratings"] = (result["build"]["value"])
            l2["Overall Ratings"] = (result["overall"]["value"])

        #l2 = [s.encode('utf-8') for s in l2]
        detail2 = l2

        sparql3 = SPARQLWrapper('http://localhost:3030/Combined/sparql')
        sparql3.setQuery(""" PREFIX auts: <http://www.vehicularguide.com/ontologies/automobiles.owl#>

                                                SELECT ?exterior ?interior ?comfort ?liability ?build ?overall WHERE{

                                                  ?node auts:hasMfrName """ + "\"" + mfrName3 + "\"" """.
                                                  ?node auts:hasModel """ + "\"" + model3 + "\"" """.
                                                  ?node auts:basedOnInterior ?interior.
                                                  ?node auts:basedOnExterior ?exterior.
                                                  ?node auts:basedOnBuild ?build.
                                                  ?node auts:basedOnComfort ?comfort.
                                                  ?node auts:basedOnLiability ?liability.
                                                  ?node auts:basedOnOverallRating ?overall.

                                                } LIMIT 5""")

        l3 = {}
        sparql3.setReturnFormat(JSON)
        results3 = sparql3.query().convert()
        # sparql3.setReturnFormat(JSON)
        # results3 = sparql3.query().convert()
        for result in results3['results']['bindings']:
            l3["Exterior Ratings"] = (result["exterior"]["value"])
            l3["Interior Ratings"] = (result["interior"]["value"])
            l3["Comfort Ratings"] = (result["comfort"]["value"])
            l3["Liability Ratings"] = (result["liability"]["value"])
            l3["Build Ratings"] = (result["build"]["value"])
            l3["Overall Ratings"] = (result["overall"]["value"])

       # l3 = [s.encode('utf-8') for s in l3]
        detail3 = l3

        return render_template('compare.html', details1=detail1, details2=detail2, details3=detail3)




if __name__ == "__main__":
    app.run(debug=True)