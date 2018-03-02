'''main __init__'''

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, t5_cargogen, misc     # noqa
