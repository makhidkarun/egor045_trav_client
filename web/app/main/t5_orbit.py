'''t5_orbit.py'''

# import re
import requests
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import NumberRange
from flask import render_template, current_app
from . import main

NAVBAR_ITEMS = [
    {'label': 'T5', 'target': 'main.t5_index'}
]


class OrbitForm(FlaskForm):
    '''Orbit form'''
    orbit_number = DecimalField(
        'Orbit number',
        description='Enter a number between 0.0 and 19.0 (decimals allowed)',
        validators=[NumberRange(0.0, 19.0)])
    submit = SubmitField('Submit')


@main.route('/t5/orbit', methods=['GET', 'POST'])
def t5_orbit():
    '''Orbit processor'''
    orbit = {}
    error_msg = None
    base_api_url = '{}/t5/orbit'.format(
        current_app.config['API_SERVER'])
    form = OrbitForm()
    if form.validate_on_submit():
        current_app.logger.debug('Orbit number = %s', form.orbit_number.data)
        if form.orbit_number.data:
            request_url = '{}/{}'.format(
                base_api_url,
                form.orbit_number.data)
            current_app.logger.debug('Calling API endpoint %s', request_url)

            try:
                resp = requests.get(request_url)
                if resp.status_code == 200:
                    orbit = resp.json()
                else:
                    error_msg = 'Received status {} from API endpoint'.format(
                        resp.status_code)
                    current_app.logger.debug(error_msg)
            except requests.ConnectionError:
                current_app.logger.debug('Unable to connect to API endpoint')
                error_msg = 'Unable to connect to API server'

        current_app.logger.debug('orbit = %s', orbit)
    return render_template(
        't5_orbit.html',
        orbit=orbit,
        form=form,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS)
