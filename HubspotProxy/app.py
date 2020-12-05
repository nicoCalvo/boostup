# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import request

from config.blueprints import register_blueprints



def create_app(configuration='Production'):
    from config.database import db  # Avoid circular imports

    settings = f'config.settings.{configuration}'

    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
   
    register_blueprints(app)

    return app


app = create_app(os.getenv('APP_CONFIGURATION', 'Production'))
