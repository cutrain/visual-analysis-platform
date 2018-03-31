from flask import Blueprint

main = Blueprint('index',
                 __name__,
                 static_folder='static',
                )

from . import routes
