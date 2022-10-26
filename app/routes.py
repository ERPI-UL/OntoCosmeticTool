from logging import NullHandler
from flask import Flask, request, url_for, render_template, flash
from app import app, models

ONTO_ID = 0 

@app.route('/', methods=['GET'])
def page_index():
    return render_template('index.html')

@app.route('/formul/list', methods=['GET'])
def page_formulations():
    titles = [('name','Name'), ('surfactantQte','Total Surfactant Qte'), ('thickenerQte','Total Thickener Qte'),('surfactantNb','Nb Surfactant'), ('oilyPhaseQte','Total Oily Phase'), ('price','Price (per Kg)')]
    data = models.formulations()
    return render_template('formulations.html', titles= titles, data= data, show_actions=True, new_url=url_for('page_formul_new'))

@app.route('/formul/<path:name>', methods=['GET', 'POST'])
def page_formul_details(name):
    iri = f"https://purl.org/ontocosmetic#{name}"

    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    act = request.args.get("action", "")
    models.actionOnFormulation(iri, ONTO_ID, act) 

    formulation_data = models.formulation(iri)
    heuristics_data = models.heuristicsValidatedByFormulation(iri)

    return render_template('formulation_details.html', formul= formulation_data, heur = heuristics_data)

@app.route('/formul/new', methods=['GET', 'POST'])
def page_formul_new():

    if request.form.get("action_add", False):
        nbDosage = request.form.get("nbDosages", 0)
        iris= []
        quantities = []
        for dosageId in range(1,int(nbDosage)+1):        
            iris.append(request.form.get(f"iri{dosageId}", ""))
            quantities.append(request.form.get(f"quantity{dosageId}", ""))
        iris.append(request.form.get("iri_last", ""))
        quantities.append(request.form.get("quantity_last", ""))
        formulation = []
        for i in range(len(iris)):
            formulation.append({'iri': iris[i], 'qte': quantities[i]})

    elif request.form.get("action_save", False):
        nbDosage = request.form.get("nbDosages", 0)
        iris= []
        quantities = []
        for dosageId in range(1,int(nbDosage)+1):        
            iris.append(request.form.get(f"iri{dosageId}", ""))
            quantities.append(request.form.get(f"quantity{dosageId}", ""))
        iris.append(request.form.get("iri_last")) if request.form.get("iri_last") else None
        quantities.append(request.form.get("quantity_last")) if request.form.get("quantity_last") else None
        print(iris)
        print(quantities)
        models.saveFomulation(iris, quantities)
        formulation = []
        flash('Formulation has been saved.', 'info')
    else:
        formulation = []
        
    ingredients = models.listerIngredientsPerType()
    ing_types = list(ingredients.keys())
    return render_template('formulation_new.html', ingredients = ingredients, ing_types= ing_types, formulation = formulation)

@app.route('/heuristics', methods=['GET'])
def page_heuristics():
    titles = [('name','Name'), ('description','Description'), ('ingType','Ingredient type affected'),('ingProperty','Input ingredient property'),('ingPropertyValue','Ingredient property value'),('prodProperty','Product property'),('prodPropertyValue','Product property value')]
    data = models.heuristics()
    return render_template('heuristics.html',responsive=True, responsive_class='table-responsive-sm', titles= titles, data= data)

@app.route('/formul/new_from_res', methods=['GET', 'POST'])
def page_formul_from_res():
    selected = {}
    if request.form.get("get_heuristic", False):
        selected["property"]= request.form.get("product_property", None)
        selected["value"]= request.form.get("product_property_value", None)
        heuristics = models.getHeuristic(selected["property"], selected["value"])
        print(heuristics)
        if not heuristics:
            flash('Nothing correspond to the request.', 'warning')
    else:
        heuristics = None
        selected["property"] = None
        selected["value"] = None
    product_properties = models.getProductPropOfHeuristic()
    properties_values = models.valueProdProperties(product_properties)
    return render_template('formulation-from-result.html',responsive=True, responsive_class='table-responsive-sm', properties_data= product_properties, properties_values_data=properties_values, heuristics_data= heuristics, selected_data= selected)

@app.route('/properties', methods=['GET'])
def page_properties():
    properties = models.properties()
    #properties_values = models.valuePerProperties()
    titles = [('name','Name'), ('description','Description'), ('substanceType', 'Substance Type')]
    return render_template('properties.html',responsive=True, responsive_class='table-responsive-sm', titles= titles, properties_data= properties)