'''main __init__'''

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, t5_cargogen, t5_orbit, misc, ct_cargogen, ct_lbb6 # noqa
from . import api_doc     # noqa
