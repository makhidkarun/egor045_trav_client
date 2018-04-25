'''ct-lbb6.py'''

import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Regexp, NumberRange
from flask import render_template, current_app
from . import main

UWP_REGEXP = r'^[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]$'
STAR_REGEXP = r'^([OBAFGKM]([0-9] ?(Ia|Ib|II|III|IV|V|VI)|D))$'

NAVBAR_ITEMS = [
    {'label': 'Classic Traveller', 'target': 'main.ct_index'},
]


class CTLBB6CombinedInputForm(FlaskForm):
    '''Input form for CT LBB6'''
    star = StringField(
        'Star',
        validators=[Regexp(STAR_REGEXP)]
    )
    orbit = IntegerField('Orbit')
    planet = StringField(
        'Planet',
        validators=[Regexp(UWP_REGEXP)]
    )
    submit = SubmitField('Submit')


@main.route('/ct/lbb6/combined', methods=['GET', 'POST'])
def ct_lbb6_combined():
    '''Handle combined/planet query'''
    planet = {}
    error_msg = None
    
    base_api_url = '{}/ct/lbb6/planet'.format(
        current_app.config['API_SERVER'])
    
    form = CTLBB6CombinedInputForm()
    if form.validate_on_submit():
        current_app.logger.debug('form.star.data = %s', form.star.data)
        current_app.logger.debug('form.orbit.data = %s', form.orbit.data)
        current_app.logger.debug('form.planet.data = %s', form.planet.data)

