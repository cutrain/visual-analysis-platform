from flask import Blueprint

graph = Blueprint('graph',
                 __name__,
                 static_folder='static'
                )

from . import routes
