# -*- encoding: utf-8 -*-

import os
from flask import Flask
from flask_bootstrap import Bootstrap5, SwitchField

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

bootstrap = Bootstrap5(app)

from app import routes, models