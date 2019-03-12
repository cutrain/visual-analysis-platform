from flask import Blueprint

graph = Blueprint('graphx',
                 __name__,
                 static_folder='static'
                )

from . import routes
