from flask import Blueprint

project = Blueprint('project',
                 __name__,
                 static_folder='static',
                )

from . import routes
