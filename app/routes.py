from logging import NullHandler
from flask import Flask, request, url_for, render_template, flash
from app import app, models

ONTO_ID = 0 

@app.route('/', methods=['GET'])
def page_index():
    return render_template('index.html')

@app.route('/formul/list', methods=['GET'])
def page_formulations():
    titles_prop = [('name','Formulation'), ('stability','Stability'), ('oiliness','Oiliness'),('viscosity','Viscosity'), ('absorption','Absorption rate'), ('sensorialProfile','Sensorial profile')]
    data_prop = models.getFormulationProp()
    titles_heur = [('name','Name'), ('A1','A1'), ('A2','A2'),('A3','A3'), ('B11','B11'), ('B12','B12'), ('B13','B13'), ('C11','C11'), ('C12','C12'), ('C2','C2'), ('C21','C21'), ('C22','C22'), ('C23','C23'), ('C31','C31'), ('C32','C32'), ('C33','C33'), ('C4','C4'), ('C5','C5'), ('C6','C6'), ('C7','C7'), ('C8','C8')]
    data_heur = models.getHeurValidatedByFormulation()
    titles_spec = [('name','Name'),('price','Price ($US per Kg)'), ('surfactantQte','Total Surfactant Qte'),('surfactantNb','Nb Surfactant'), ('thickenerQte','Total Thickener Qte'), ('oilyPhaseQte','Total Oily Phase'),('ratio','HLB/RHLB balance'),('highEmolQte','High emollience qte'),('medEmolQte','Med emollience qte'),('lowEmolQte','Low emollience qte') ]
    data_spec = models.formulations()
    return render_template('formulations.html', titles_prop = titles_prop, data_prop= data_prop,titles_heur = titles_heur, data_heur= data_heur, titles_spec= titles_spec, data_spec= data_spec, show_actions=True, new_url=url_for('page_formul_new'))

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
        
    ingredients = models.listIngredientsPerType()
    ing_types = list(ingredients.keys())
    return render_template('formulation_new.html', ingredients = ingredients, ing_types= ing_types, formulation = formulation)

""" @app.route('/formul/fork', methods=['GET', 'POST'])
def page_formul_fork():
    #copy
    return render_template('formulation_edit.html', ingredients = ingredients, ing_types= ing_types, formulation = formulation) """

@app.route('/formul/<path:name>/edit', methods=['GET', 'POST'])
def page_formul_edit(name):

    formulIRI = f"https://purl.org/ontocosmetic#{name}"
    formulname= models.getLabels(formulIRI)


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
        flash('Formulation has been updated.', 'info')
    else:
        formulation = models.getDosages(formulIRI)
        
    ingredients = models.listIngredientsPerType()
    ing_types = list(ingredients.keys())
    return render_template('formulation_edit.html', ingredients = ingredients, ing_types= ing_types, formulation = formulation, formulname=formulname)

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
        recommendedIng = models.getRecommendedIngredients(heuristics) 
        if not heuristics:
            flash('Nothing corresponds to the request.', 'warning')
    else:
        heuristics = None
        selected["property"] = None
        selected["value"] = None
        recommendedIng = None
    product_properties = models.getProductPropOfHeuristic()
    properties_values = models.valueProdProperties(product_properties)
    return render_template('formulation-from-result.html',responsive=True, responsive_class='table-responsive-sm', properties_data= product_properties, properties_values_data=properties_values, heuristics_data= heuristics, selected_data= selected, recommended_ing = recommendedIng)

@app.route('/properties', methods=['GET'])
def page_properties():
    properties = models.properties()
    #properties_values = models.valuePerProperties()
    titles = [('name','Name'), ('description','Description'), ('substanceType', 'Substance Type')]
    return render_template('properties.html',responsive=True, responsive_class='table-responsive-sm', titles= titles, properties_data= properties)