from flask import Blueprint

component = Blueprint('component',
                 __name__,
                 static_folder='static'
                )

from . import routes
