# OntoCosmetic Tool

OntoCosmetic tool is a web service that permits to formulate cosmetic product and verify design rules against this formulation. 
This web service is a prototype designed to validate the feasbility of using ontology to assit the formulation process of cosmetic product.

This software was developed by Alex Gabriel (Université de Lorraine - ERPI) in collaboration with Juliana Serna (Université de Lorraine - LRGP).

This work is based on OntoCosmetic ontologies however the ontology was instanciated with additional information which is not available by default.

# Main features


# Commands 
In order to start the application, there is two alternatives : using Docker or python venv. 

## Docker
Here are the main commmands to start the app using docker. It requires to install Docker on the host machine.
```sh
# create the container
docker build . -t ontocosmtool

# start the container
docker run -d -p 5000:5000 --name=OntoCosmTool ontocosmtool

# stop the container
docker stop OntoCosmTool
```

## Venv
To use this alternive, it requires Python and Pip on the host system. As the reasoner (Pellet) requires Java, you may have installed Java on the host machine.

```sh
# create the virtual environment
python3 -m venv .

# activate the virtual environment (Windows)
Scripts\activate 

# install required dependencies (do it once, the first time)
pip install -r requirements.txt

# start the web service 
python3 run.py

# stop the virtual environment
docker stop OntoCosmTool
```

## Resources
[Jinja2 HTML Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
[bootstrap flask](https://bootstrap-flask.readthedocs.io/en/stable/)
[OWLREADY2 doc](https://owlready2.readthedocs.io/en/latest/index.html)


## SHACL
[SHACL resources list](https://incf.github.io/neuroshapes/docs/shacl-tutorial/overview/index.html)
[Validating RDF data- SHACL book](http://book.validatingrdf.com/)