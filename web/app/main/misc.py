'''misc.py'''
import logging
import requests
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import Required, ValidationError
from . import main
from flask import render_template

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


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
    base_api_url = 'https://api.trav.phraction.org/misc/angdia'
    data = {}
    form = AngDiaForm()
    if form.validate_on_submit():
        LOGGER.debug('form.diameter.data = %s', form.diameter.data)
        LOGGER.debug('form.distance.data = %s', form.distance.data)
        resp = requests.get(base_api_url + '?distance={}&diameter={}'.format(
            form.distance.data, form.diameter.data))
        if resp.status_code == 200:
                data = resp.json()
        else:
            LOGGER.debug(
                'received status %d from API endpoint',
                resp.status_code)
    return render_template('angdia.html', data=data, form=form)
