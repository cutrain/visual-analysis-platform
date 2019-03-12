from flask import Blueprint

data = Blueprint('data',
                 __name__,
                 static_folder='static',
                )

from . import routes
