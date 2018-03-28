'''misc.py'''
import logging
import requests
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import Required, ValidationError
from flask import render_template, current_app
from . import main

NAVBAR_ITEMS = [
    {'label': 'Miscellaneous items', 'target': 'main.misc_index'}
]


class AngDiaForm(FlaskForm):
    '''Form for angular diameter'''
    diameter = FloatField('Object diameter', [Required()])
    distance = FloatField('Distance to object', [Required()])
    submit = SubmitField('Submit')

    def validate_distance(form, field):
        '''Custom validator = value > 0'''
        if float(field.data) is 0.0:
            raise ValidationError('Distance must not be 0')


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
