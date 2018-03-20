'''t5_orbit.py'''

import logging
# import re
import requests
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import NumberRange
from flask import render_template, current_app
from . import main

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


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
    base_api_url = 'https://{}/t5/orbit'.format(
        current_app.config['API_SERVER'])
    form = OrbitForm()
    if form.validate_on_submit():
        LOGGER.debug('Orbit number = %s', form.orbit_number.data)
        if form.orbit_number.data:
            request_url = '{}/{}'.format(
                base_api_url,
                form.orbit_number.data)
            LOGGER.debug('Calling API endpoint %s', request_url)
            resp = requests.get(request_url)
            if resp.status_code == 200:
                orbit = resp.json()
            else:
                LOGGER.debug(
                    'received status %d from API endpoint',
                    resp.status_code)
                return render_template(
                    'generic_api_response.html',
                    status_code=resp.status_code,
                    message=resp.description)
        LOGGER.debug('orbit = %s', orbit)
    return render_template(
        't5_orbit.html',
        orbit=orbit,
        form=form)
