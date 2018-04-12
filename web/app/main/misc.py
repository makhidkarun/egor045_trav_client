'''misc.py'''

import requests
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField
from wtforms.validators import Required, Regexp, NumberRange
from flask import render_template, current_app
from . import main

NAVBAR_ITEMS = [
    {'label': 'Miscellaneous items', 'target': 'main.misc_index'}
]

STAR_REGEXP = r'^[OBAFGKM]([0-9] ?(Ia|Ib|II|III|IV|V|VI)|D)$'

class AngDiaForm(FlaskForm):
    '''Form for angular diameter'''
    diameter = FloatField(
        'Object diameter',
        [Required(), NumberRange(0.0000001, 9999999999.0)])
    distance = FloatField(
        'Distance to object',
        [Required(), NumberRange(0.0000001, 9999999999.0)])
    submit = SubmitField('Submit')


class StarColourForm(FlaskForm):
    '''Form for star colour'''
    classification = StringField(
        'Star classification',
        validators=[Regexp(STAR_REGEXP), Required()]
    )
    submit = SubmitField('Submit')


@main.route('/misc/angdia', methods=['GET', 'POST'])
def angdia():
    '''Return angular diameter of object diameter D, range R'''
    base_api_url = '{}/misc/angdia'.format(
        current_app.config['API_SERVER'])
    data = {}
    error_msg = None
    form = AngDiaForm()
    if form.validate_on_submit():
        current_app.logger.debug('form.diameter.data = %s', form.diameter.data)
        current_app.logger.debug('form.distance.data = %s', form.distance.data)

        try:
            resp = requests.get(
                base_api_url +
                '?distance={}&diameter={}'.format(
                    form.distance.data, form.diameter.data))
            if resp.status_code == 200:
                data = resp.json()
            else:
                error_msg = 'Received status {} from API endpoint'.format(
                    resp.status_code)
                current_app.logger.debug(error_msg)
        except requests.ConnectionError:
            current_app.logger.debug('Unable to connect to API endpoint')
            error_msg = 'Unable to connect to API server'

    return render_template(
        'angdia.html',
        data=data,
        form=form,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS)


@main.route('/misc/starcolour', methods=['GET', 'POST'])
@main.route('/misc/starcolor', methods=['GET', 'POST'])
def starcolor():
    '''Return RGB values for star'''

    base_api_url = '{}/misc/starcolor'.format(
        current_app.config['API_SERVER'])
    data = {}
    error_msg = None
    form = StarColourForm()

    if form.validate_on_submit():
        current_app.logger.debug(
            'Form data = %s',
            form.classification.data)
        current_app.logger.debug('Form errors = %s', form.errors)

        try:
            # Drop space from classification
            form.classification.data = form.classification.data.replace(' ', '')
            current_app.logger.debug(
                'form data now = %s',
                form.classification.data
            )
            resp = requests.get(
                base_api_url +
                '?code={}'.format(
                    form.classification.data))
            if resp.status_code == 200:
                data = resp.json()
            else:
                current_app.logger.debug(
                    'received %s from API server',
                    resp.json()
                )
                error_msg = 'Received status {} "{}" from API endpoint'.format(
                    resp.status_code, resp.json()['description'])
                current_app.logger.debug(error_msg)
        except requests.ConnectionError:
            current_app.logger.debug('Unable to connect to API endpoint')
            error_msg = 'Unable to connect to API server'

    return render_template(
        'starcolour.html',
        form=form,
        data=data,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS
    )
