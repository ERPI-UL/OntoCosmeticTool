import os
from typing import List
import uuid
from owlready2 import *
onto = get_ontology("./app/static/OntoCosmetic-40-all.owl").load()

def format(value):
    if value:
        if type(value) is owlready2.prop.IndividualValueList or type(value) is List:
            return ", ".join(value)
        else:
            return value
    else:
        return "-"

def getLabels(IRIs):
    if IRIs:
        if type(IRIs) is owlready2.prop.IndividualValueList or type(IRIs) is list:
            iri_label = ""
            for iri in IRIs:
                if iri.label.en.first():
                    if len(IRIs)>1:
                        iri_label += f"{iri.label.en.first()}, "
                    else:
                        iri_label = iri.label.en.first()
                elif iri.name:
                    if len(IRIs)>1:
                        iri_label += f"{iri.name}, "
                    else:
                        iri_label = iri.name
                elif iri.iri:
                    if len(IRIs)>1:
                        iri_label += f"{iri.iri}, "
                    else:
                        iri_label = iri.iri
                else:
                    if len(IRIs)>1:
                        iri_label += f"{iri}, "
                    else:
                        iri_label = iri
            return iri_label
        else:
            try: 
                if IRIs.label:
                    return IRIs.label.en.first()
                else:
                    return IRIs.name
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
        tmp_formulation['price'] = formul.hasTotalPrice
        tmp_formulation['ratio'] = formul.hasHlbOverRhlbRatio
        tmp_formulation['highEmolQte'] = formul.hasHighAbsEmolQte
        tmp_formulation['medEmolQte'] = formul.hasMedAbsEmolQte
        tmp_formulation['lowEmolQte'] = formul.hasLowAbsEmolQte
        data.append(tmp_formulation)
    return data

def getFormulationProp():
    data = []
    formulations = onto.Formulation.instances()
    for formul in formulations:
        tmp_formulation = {}
        tmp_formulation['iri'] = formul.iri
        tmp_formulation['name'] = formul.name
        tmp_formulation['stability'] = getLabels(formul.hasProductStability)
        tmp_formulation['oiliness'] = getLabels(formul.hasProductOiliness)
        tmp_formulation['viscosity'] = getLabels(formul.hasProductViscosity)
        tmp_formulation['absorption'] = getLabels(formul.hasProductAbsorptionRate)
        tmp_formulation['sensorialProfile'] = getLabels(formul.hasSensorialProfile)
        data.append(tmp_formulation)
    return data

def getHeurValidatedByFormulation():
    data = []
    heuristics = onto.Heuristic.instances()
    formulations = onto.Formulation.instances()
    for formul in formulations:
        validatedHeur = formul.isValidatedBy
        formul_valid_temp = {}
        formul_valid_temp['name'] = formul.name
        for heur in heuristics:
            if heur in validatedHeur:
                formul_valid_temp[heur.name] = "✔"
            else:
                formul_valid_temp[heur.name] = "-"
        data.append(formul_valid_temp)
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
    data['stability'] = getLabels(Formulation.hasProductStability)
    data['oiliness'] = getLabels(Formulation.hasProductOiliness)
    data['viscosity'] = getLabels(Formulation.hasProductViscosity)
    data['price'] = Formulation.hasTotalPrice
    data['HLB'] = Formulation.hasCalculatedHLB
    data['RHLB'] = Formulation.hasCalculatedRHLB
    data['ratio'] = Formulation.hasHlbOverRhlbRatio
    for Dosage in dosages:
        tmp_dosage = {}
        tmp_dosage['ing'] = Dosage.isQuantifying.name
        tmp_dosage['qte'] = Dosage.hasQuantity
        dos.append(tmp_dosage)
    data['dosages'] = dos
    return data

def getDosages(formulIRI):
    Formulation = IRIS[formulIRI]
    dosages = Formulation.hasDosage
    data = []
    for dosage in dosages:
        temp = {}
        temp['iri'] = dosage.isQuantifying.iri
        temp['qte'] = dosage.hasQuantity
        data.append(temp)
    return data


def heuristicsValidatedByFormulation(iri):
    Formulation = IRIS[iri]
    heuristics = Formulation.isValidatedBy
    heurs = []
    for Heuristic in heuristics:
        tmp_heur = {}
        tmp_heur['id'] = Heuristic.name
        tmp_heur['description'] = format(Heuristic.hasHeuristicDescription)
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
        data.append(tmp_property)
    return data

def getRecommendedIngredients(heuristics):
    data = {}
    for heuristic in heuristics:
        heurName = heuristic['name'].name
        resp = []              
        if heurName == "C8":
            resp = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?ing 
WHERE { ?ing cosme:hasLongChainsAndNoDoubleBonds ?val.
    }"""))
        elif heurName == "C7": 
            resp = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?ing 
WHERE { ?ing cosme:hasLaurylOleylGroup ?val.
    }"""))
        elif heurName == "C6":
            resp = [['Octyldodecanol']]
        elif heurName == "C5":
            resp = [['cetearyl'],['stearyl'],['cetyl ']]
        elif heurName == "C21":
            resp = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?ing 
WHERE { ?ing cosme:hasSpreading cosme:high_spreading.
    }"""))
        elif heurName == "C22":
            resp = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?ing 
WHERE { ?ing cosme:hasSpreading cosme:medium_spreading.
    }"""))
        elif heurName == "C23":
            resp = list(default_world.sparql("""
    PREFIX cosme: <https://purl.org/ontocosmetic#> 
           SELECT DISTINCT ?ing 
WHERE { ?ing cosme:hasSpreading cosme:low_spreading.
    }"""))
        ingList= []
        if resp:
            for property in resp:
                try:
                    ingList.append(property[0].name)
                except:
                    ingList.append(property[0])
            data[heuristic['name']]=ingList
        else:
            data[heuristic['name']]=[]
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
    allValueList = []
    for prod_prop in prod_prop_list:
        temp = []
        for pairs in sparql:
            if pairs[0].iri == prod_prop['iri']:
                
                tmp_value = {}
                tmp_value['iri'] = pairs[1].iri
                tmp_value['name'] = pairs[1].name
                allValueList.append(tmp_value)
                temp.append(tmp_value)
            data[prod_prop['iri']] = temp
    data['all']= allValueList
    return data

def getHeuristic(propertyIRI, valueIRI = None):
    print(propertyIRI)
    property = propertyIRI.split("#")
    if valueIRI:
        state = valueIRI.split("#")
    data = []
    if valueIRI:
        sparql = list(default_world.sparql("""
        PREFIX cosme: <https://purl.org/ontocosmetic#> 
            SELECT DISTINCT ?heurDescription ?ingType ?ingProperty ?ingValue ?heur
    WHERE { ?heur cosme:hasHeuristicProdProp cosme:"""+property[1]+""" ;
        cosme:hasHeuristicProductPropertyState cosme:"""+state[1]+""";
        cosme:hasHeuristicDescription ?heurDescription.
        OPTIONAL { ?heur cosme:hasHeuristicIngType ?ingType.}
        OPTIONAL { ?heur cosme:hasHeuristicIngProp ?ingProperty.}
        OPTIONAL { ?heur cosme:hasIngredientPropertyState ?ingValue. }
        }"""))
    else:
        sparql = list(default_world.sparql("""
        PREFIX cosme: <https://purl.org/ontocosmetic#> 
            SELECT DISTINCT ?heurDescription ?ingType ?ingProperty ?ingValue ?heur
    WHERE { ?heur cosme:hasHeuristicProdProp cosme:"""+property[1]+""" ;
        cosme:hasHeuristicDescription ?heurDescription.
        OPTIONAL { ?heur cosme:hasHeuristicIngType ?ingType.}
        OPTIONAL {?heur cosme:hasHeuristicIngProp ?ingProperty.}
        OPTIONAL {?heur cosme:hasIngredientPropertyState ?ingValue. }
        }"""))
    for resp in sparql:
        tmp_value = {}
        tmp_value['description'] = resp[0]
        tmp_value['ingType'] = resp[1]
        tmp_value['ingProperty'] = resp[2]
        tmp_value['ingValue'] = resp[3]
        tmp_value['name'] = resp[4]
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

def listIngredientsPerType():
    data = {}
    Thickeners = onto.Thickener.instances()
    thickenersList = []
    for thickener in Thickeners:
        tmp_thickener = {}
        tmp_thickener['iri'] = thickener.iri
        if thickener.hasINCIcode:
            tmp_thickener['inci'] = thickener.hasINCIcode[0]
        else: 
            tmp_thickener['inci'] = thickener.name
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
        else: 
            tmp_surfactant['inci'] = surfactant.name
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
        else: 
            tmp_emollient['inci'] = emollient.name
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
        else: 
            tmp_active['inci'] = active.name
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
    formulation.hasTotalOilyPhase = float(oilyPhaseQte)

def calculteEmolSpreading(formulation):
    lowSpreadinQte = 0.0
    medSpreadingQte = 0.0
    highSpreadingQte = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        ing = dosage.isQuantifying
        if onto.low_spreading in ing.hasSpreading:
            lowSpreadinQte += dosage.hasQuantity
        elif onto.medium_to_low_spreading in ing.hasSpreading:
            lowSpreadinQte += dosage.hasQuantity
        elif onto.medium_spreading in ing.hasSpreading:
            medSpreadingQte += dosage.hasQuantity
        elif onto.medium_to_high_spreading in ing.hasSpreading:
            highSpreadingQte += dosage.hasQuantity
        elif onto.high_spreading in ing.hasSpreading:
            highSpreadingQte += dosage.hasQuantity
    formulation.hasHighAbsEmolQte = lowSpreadinQte
    formulation.hasMedAbsEmolQte = medSpreadingQte
    formulation.hasLowAbsEmolQte = highSpreadingQte


def calculateThickenerQuantity(formulation):
    thickenerQte = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Thickener:
            thickenerQte += dosage.hasQuantity
    formulation.hasTotalThickenerQuantity = thickenerQte 

def calculateHLB(formulation):
    qteSurfactant = 0.0
    calculatedHLB = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Surfactant:
            Surfactant = dosage.isQuantifying
            qteSurfactant += dosage.hasQuantity
            calculatedHLB += dosage.hasQuantity * Surfactant.hasHLB
    formulation.hasCalculatedHLB = calculatedHLB /qteSurfactant

def calculateRHLB(formulation):
    qteEmollient = 0.0
    calculatedRHLB = 0.0
    listDosages = formulation.hasDosage
    for dosage in listDosages:
        if type(dosage.isQuantifying) is onto.Emollient:
            Emollient = dosage.isQuantifying
            qteEmollient += dosage.hasQuantity
            calculatedRHLB += dosage.hasQuantity * Emollient.hasRequiredHLB
    formulation.hasCalculatedRHLB = calculatedRHLB / qteEmollient

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
                ing = IRIS[ingredients_iri[i]]
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
    elif action =="oiliness":
        calculateOilyPhaseQuantity(Formulation)
    elif action =="emolAbs":
        calculteEmolSpreading(Formulation)
    elif action =="all":
        completeWithWater(Formulation)
        calculatePrice(Formulation)
        calculateHLBoverRHLB(Formulation)
        calculateOilyPhaseQuantity(Formulation)
        calculteEmolSpreading(Formulation)
        calculateThickenerQuantity(Formulation)
        calculateSurfactantQuantity(Formulation)
        countNbSurfactant(Formulation)
    elif action =="reasoning":
        with onto:
            sync_reasoner_pellet([onto], infer_property_values = True, infer_data_property_values = True)
    elif action =="thickenerQte":
        with onto:
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
