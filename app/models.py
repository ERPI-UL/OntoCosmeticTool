from ast import Try
import os
from typing import List
import uuid
from owlready2 import *
onto = get_ontology("./app/static/OntoCosmetic-40-all.owl").load()

def format(value):
    if value:
        if type(value) is owlready2.prop.IndividualValueList or type(value) is List:
            # print(type(value.first()))
            # print(value.first())
            return ", ".join(value)
        else:
            return value
    else:
        return "-"

def getLabels(IRIs):
    if IRIs:
        if type(IRIs) is list:
            iri_label = ""
            for iri in IRIs:
                if iri.label.en.first():
                    iri_label = ", ".join([iri_label, iri.label.en.first()])
                    print(f"label {iri.label.en.first()}")
                elif iri.iri:
                    iri_label = ", ".join([iri_label, iri.iri])
                    print(f"iri {iri.iri}")
                else:
                    iri_label = ", ".join([iri_label, iri])
            return iri_label
        else:
            try: 
                return IRIs.label.en.first()
            except:
                return IRIs
    else:
        return "-"

def formulations():
    data = []
    formulations = onto.Formulation.instances()
    for formul in formulations:
        tmp_formulation = {}
        tmp_formulation['iri'] = formul.iri
        tmp_formulation['name'] = formul.name
        tmp_formulation['surfactantQte'] = formul.hasTotalSurfactantQuantity
        tmp_formulation['thickenerQte'] = formul.hasTotalThickenerQuantity
        tmp_formulation['surfactantNb'] = formul.hasNbSurfactantIng
        tmp_formulation['oilyPhaseQte'] = formul.hasTotalOilyPhase
        data.append(tmp_formulation)
    return data

def formulation(iri):
    Formulation = IRIS[iri]
    dosages = Formulation.hasDosage
    dos = []
    data = {}
    data['iri'] = Formulation.iri
    data['name'] = Formulation.name
    data['surfactQte'] = Formulation.hasTotalSurfactantQuantity
    data['thickenerQte']= Formulation.hasTotalThickenerQuantity
    data['surfactNb']= Formulation.hasNbSurfactantIng
    data['oilyPhaseQte']= Formulation.hasTotalOilyPhase
    data['stability'] = Formulation.hasProductStability
    data['oiliness'] = Formulation.hasProductOiliness
    data['viscosity'] = Formulation.hasProductViscosity
    data['price'] = Formulation.hasTotalPrice
    for Dosage in dosages:
        tmp_dosage = {}
        tmp_dosage['ing'] = Dosage.isQuantifying
        tmp_dosage['qte'] = Dosage.hasQuantity
        dos.append(tmp_dosage)
    data['dosages'] = dos
    return data

def heuristicsValidatedByFormulation(iri):
    Formulation = IRIS[iri]
    heuristics = Formulation.isValidatedBy
    heurs = []
    for Heuristic in heuristics:
        tmp_heur = {}
        tmp_heur['id'] = Heuristic.name
        tmp_heur['description'] = Heuristic.hasHeuristicDescription
        tmp_heur['prodProperty'] = Heuristic.hasHeuristicProdProp
        heurs.append(tmp_heur)
    return heurs

def heuristics():
    data = []
    heuristics = onto.Heuristic.instances()
    for Heuristic in heuristics:
        tmp_heuristic = {}
        tmp_heuristic['iri'] = Heuristic.iri
        tmp_heuristic['name'] = Heuristic.name
        tmp_heuristic['description'] = format(Heuristic.hasHeuristicDescription)
        tmp_heuristic['ingType'] = getLabels(Heuristic.hasHeuristicIngType)
        tmp_heuristic['ingProperty'] = getLabels(Heuristic.hasHeuristicIngProp)
        tmp_heuristic['ingPropertyValue'] = Heuristic.hasIngredientPropertyState
        #for product_property in Heuristic.hasHeuristicProdProp:
        #    tmp_heuristic['prodProperty'] = getLabels(product_property)
        tmp_heuristic['prodProperty'] = Heuristic.hasHeuristicProdProp
        tmp_heuristic['prodPropertyValue'] = Heuristic.hasHeuristicProductPropertyState
        data.append(tmp_heuristic)
    return data

def properties():
    data = []
    property_inst = onto.Property.instances()
    for property in property_inst:
        tmp_property = {}
        tmp_property['iri'] = property.iri
        tmp_property['name'] = property.name
        tmp_property['description'] = property.comment.en.first()
        tmp_property['substanceType'] = format(property.isPropertyOf.first())
        #tmp_property['values'] = 
        data.append(tmp_property)
    return data

def getProductPropOfHeuristic():
    data = []
    sparql = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?prop 
WHERE { ?heur cosme:hasHeuristicProdProp ?prop.
    }"""))
    
    #heuristics = onto.Heuristic.instances()
    for property in sparql:
        tmp_property = {}
        tmp_property['iri'] = property[0].iri
        tmp_property['name'] = property[0].name
        data.append(tmp_property)
    return data
    

def valueProdProperties(prod_prop_list):
    data = {}
    sparql = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?prop ?propState 
WHERE { ?heur cosme:hasHeuristicProdProp ?prop; cosme:hasHeuristicProductPropertyState ?propState.
    }"""))
    for prod_prop in prod_prop_list:
        temp = []
        for pairs in sparql:
            if pairs[0].iri == prod_prop['iri']:
                tmp_value = {}
                tmp_value['iri'] = pairs[1].iri
                tmp_value['name'] = pairs[1].name
                temp.append(tmp_value)
            data[prod_prop['iri']] = temp
    return data

def getHeuristic(propertyIRI, valueIRI = None):
    print(propertyIRI)
    data = []
    if valueIRI:
        sparql = list(default_world.sparql("""
        PREFIX cosme: <https://purl.org/ontocosmetic#> 
            SELECT DISTINCT ?heurDescription ?ingType ?ingProperty ?ingValue 
    WHERE { ?heur cosme:hasHeuristicProdProp """+propertyIRI+""" ;
        cosme:hasHeuristicDescription ?heurDescription.
        OPTIONAL { ?heur cosme:hasHeuristicProductPropertyState """+valueIRI+"""; cosme:hasHeuristicIngType ?ingType;
        cosme:hasHeuristicIngProp ?ingProperty;
        cosme:hasIngredientPropertyState ?ingValue. }
        }"""))
    else:
        sparql = list(default_world.sparql("""
        PREFIX cosme: <https://purl.org/ontocosmetic#> 
            SELECT DISTINCT ?heurDescription ?ingType ?ingProperty ?ingValue 
    WHERE { ?heur cosme:hasHeuristicProdProp """+propertyIRI+""" ;
        cosme:hasHeuristicDescription ?heurDescription.
        OPTIONAL { ?heur cosme:hasHeuristicIngType ?ingType;
        cosme:hasHeuristicIngProp ?ingProperty;
        cosme:hasIngredientPropertyState ?ingValue. }
        }"""))
    for resp in sparql:
        tmp_value = {}
        tmp_value['description'] = resp[0]
        tmp_value['ingType'] = resp[1]
        tmp_value['ingProperty'] = resp[2]
        tmp_value['ingValue'] = resp[0]
        data.append(tmp_value)
    return data

def completeWithWater(formulation):
    totalQuantity = 0.0
    completingWater = onto.Dosage(f"dosage_{uuid.uuid4()}")
    completingWater.isQuantifying = onto.water

    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if dosage.hasQuantity:
            totalQuantity += dosage.hasQuantity
        print(dosage.isQuantifying)
        if onto.water.iri == dosage.isQuantifying:
            #TODO verifier le comportement
            destroy_entity(completingWater)
            completingWater = dosage
    waterQte = 100.0 - totalQuantity
    completingWater.hasQuantity = float(waterQte)
    formulation.hasDosage.append(completingWater)  

def listerIngredientsPerType():
    data = {}
    Thickeners = onto.Thickener.instances()
    thickenersList = []
    for thickener in Thickeners:
        tmp_thickener = {}
        tmp_thickener['iri'] = thickener.iri
        if thickener.hasINCIcode:
            tmp_thickener['inci'] = thickener.hasINCIcode[0]
        thickenersList.append(tmp_thickener)
    thickenersList.sort(key=lambda d: d['inci'])
    data['thickeners'] = thickenersList

    Surfactants = onto.Surfactant.instances()
    surfactantsList = []
    for surfactant in Surfactants:
        tmp_surfactant = {}
        tmp_surfactant['iri'] = surfactant.iri
        if surfactant.hasINCIcode:
            tmp_surfactant['inci'] = surfactant.hasINCIcode[0]
        surfactantsList.append(tmp_surfactant)
    surfactantsList.sort(key=lambda d: d['inci'])
    data['surfactants'] = surfactantsList

    Emollients = onto.Emollient.instances()
    emollientsList = []
    for emollient in Emollients:
        tmp_emollient = {}
        tmp_emollient['iri'] = emollient.iri
        if emollient.hasINCIcode : 
            tmp_emollient['inci'] = emollient.hasINCIcode[0]
        emollientsList.append(tmp_emollient)
    emollientsList.sort(key=lambda d: d['inci'])
    data['emollients'] = emollientsList

    Actives = onto.Active.instances()
    activesList = []
    for active in Actives:
        tmp_active = {}
        tmp_active['iri'] = active.iri
        if active.hasINCIcode : 
            tmp_active['inci'] = active.hasINCIcode[0]
        activesList.append(tmp_active)
    activesList.sort(key=lambda d: d['inci'])
    data['active'] = activesList
    return data


def calculateOilyPhaseQuantity(formulation):
    oilyPhaseQte = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if len(dosage.hasPhase) and onto.oily_phase.iri in dosage.hasPhase[0].is_a:
            oilyPhaseQte += dosage.hasQuantity
    formulation.hasTotalOilyPhase.append(oilyPhaseQte)

def calculateThickenerQuantity(formulation):
    thickenerQte = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Thickener:
            thickenerQte += dosage.hasQuantity
    formulation.hasTotalThickenerQuantity = thickenerQte 

def calculateHLB(formulation):
    calculatedHLB = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Surfactant:
            Surfactant = dosage.isQuantifying
            calculatedHLB += dosage.hasQuantity * Surfactant.hasHLB
    formulation.hasCalculatedHLB = calculatedHLB

def calculateRHLB(formulation):
    calculatedRHLB = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Emollient:
            Emollient = dosage.isQuantifying
            thickenerQte += dosage.hasQuantity * Emollient.hasRequiredHLB
    formulation.hasCalculatedRHLB = calculatedRHLB

def calculateHLBoverRHLB(formulation):
    calculateHLB(formulation)
    calculateRHLB(formulation)
    hlb = formulation.hasCalculatedHLB
    rhlb = formulation.hasCalculatedRHLB
    ratio = hlb/rhlb
    formulation.hasHlbOverRhlbRatio = ratio

def countNbSurfactant(formulation):
    nbSurfactant = 0
    
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Surfactant:
            nbSurfactant +=1
    formulation.hasNbSurfactantIng = nbSurfactant

def calculateSurfactantQuantity(formulation):
    sufactVol = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Surfactant:
            sufactVol += dosage.hasQuantity
    formulation.hasTotalSurfactantQuantity = sufactVol

def calculatePrice(formulationIRI):
    listDosages = formulationIRI.hasDosage
    tempPrice = 0
    for dosage in listDosages:
        Ingredient = dosage.isQuantifying
        print(Ingredient)
        print(Ingredient.hasPricePerKilogram)
        tempPrice += float(Ingredient.hasPricePerKilogram if Ingredient.hasPricePerKilogram else 0) * float(dosage.hasQuantity if dosage.hasQuantity else 0 )
    formulationIRI.hasTotalPrice = tempPrice /100

def saveFomulation(ingredients_iri, ingredients_qte):
    if len(ingredients_iri) != len(ingredients_qte):
        raise Exception("IRI array has to have the same size than quantity array")
    else:
        formulationID = uuid.uuid4()
        onto_formulation = get_ontology("http://purl.org/ontocosmetic/temp%s#" % formulationID)
        onto_formulation.imported_ontologies.append(onto)

        with onto_formulation:
            new_formul = onto.Formulation(f"fomulation_{formulationID}")
            for i in range(len(ingredients_iri)):
                tmp_dosage = onto.Dosage(f"dosage_{uuid.uuid4()}")
                print(tmp_dosage)
                ing = IRIS[ingredients_iri[i]]
                print(ing)
                tmp_dosage.isQuantifying.append(ing)
                tmp_dosage.hasQuantity = float(ingredients_qte[i])
                new_formul.hasDosage.append(tmp_dosage)
            completeWithWater(new_formul)
            calculateThickenerQuantity(new_formul)
            calculateSurfactantQuantity(new_formul)
            countNbSurfactant(new_formul)
            #calculateOilyPhaseQuantity(new_formul)
            #sync_reasoner_pellet([onto, onto_formulation], infer_property_values = True, infer_data_property_values = True, debug=2)
            onto_formulation.save(file=f"./app/static/OntoCosmetic-formul_{formulationID}.owl", format = "rdfxml")

def actionOnFormulation(iri, ONTO_ID, action):
    onto_tmp = get_ontology("http://purl.org/ontocosmetic/temp%s#" % ONTO_ID)

    Formulation = IRIS[iri]

    
    if action == "water":
        completeWithWater(Formulation)
    elif action =="price":
        calculatePrice(Formulation)
    elif action =="HLB":
        calculateHLBoverRHLB(Formulation)
    elif action =="reasoning":
        with onto_tmp:
            sync_reasoner_pellet([onto, onto_tmp], infer_property_values = True, infer_data_property_values = True)
    elif action =="thickenerQte":
        with onto_tmp:
            calculateThickenerQuantity(Formulation)
    elif action =="surfactantQte":
        calculateSurfactantQuantity(Formulation)
    elif action =="surfactantNb":
        countNbSurfactant(Formulation)
    elif action =="save":
        with onto_tmp:
            onto_tmp.save(file="./app/static/OntoCosmetic-temp.owl", format = "rdfxml")
            onto.save(file="./app/static/OntoCosmetic-temp_1.owl", format = "rdfxml")
    else:
        pass
