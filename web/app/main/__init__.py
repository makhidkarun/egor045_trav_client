'''main __init__'''

# pragma pylint: disable=C0103, C0413

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, t5_cargogen, t5_orbit, misc, ct_cargogen # noqa
from . import ct_lbb6
from . import api_doc     # noqa
