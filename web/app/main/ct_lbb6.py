'''ct_lbb6.py'''

import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Regexp, NumberRange, Optional, Required
from flask import render_template, current_app
from . import main

UWP_REGEXP = r'^[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]$'
STAR_REGEXP = r'^([OBAFGKM]([0-9] ?(Ia|Ib|II|III|IV|V|VI)|D))$'

NAVBAR_ITEMS = [
    {'label': 'Classic Traveller', 'target': 'main.ct_index'},
]


class CTLBB6PlanetInputForm(FlaskForm):
    '''Input form for CT LBB6 planet'''
    planet = StringField(
        'Planet',
        validators=[Required(), Regexp(UWP_REGEXP)]
    )
    star = StringField(
        'Star',
        validators=[Optional(), Regexp(STAR_REGEXP)]
    )
    orbit = IntegerField(
        'Orbit',
        validators=[Optional(), NumberRange(0, 19)]
    )
    submit = SubmitField('Submit')


class CTLBB6StarInputForm(FlaskForm):
    '''Input form for CT LBB6 star'''
    star = StringField(
        'Star',
        validators=[Required(), Regexp(STAR_REGEXP)]
    )
    submit = SubmitField('Submit')


class CTLBB6OrbitInputForm(FlaskForm):
    '''Input form for CT LBB6 orbit'''
    orbit = IntegerField(
        'Orbit',
        validators=[Required(), NumberRange(0, 19)]
    )
    star = StringField(
        'Star',
        validators=[Optional(), Regexp(STAR_REGEXP)]
    )
    submit = SubmitField('Submit')



@main.route('/ct/lbb6/planet', methods=['GET', 'POST'])
def ct_lbb6_planet():
    '''Handle planet query'''
    data = {}
    error_msg = None

    base_api_url = '{}/ct/lbb6/planet'.format(
        current_app.config['API_SERVER'])

    form = CTLBB6PlanetInputForm()
    if form.validate_on_submit():
        current_app.logger.debug('form.star.data = %s', form.star.data)
        current_app.logger.debug('form.orbit.data = %s', form.orbit.data)
        current_app.logger.debug('form.planet.data = %s', form.planet.data)

        current_app.logger.debug('form.star.data = %s', form.star.data)
        current_app.logger.debug('form.orbit.data = %s', form.orbit.data)
        current_app.logger.debug('form.planet.data = %s', form.planet.data)

        request_uri_elements = []
        if form.star.data != '':
            request_uri_elements.append('star={}'.format(form.star.data))
        if form.orbit.data is not None:
            request_uri_elements.append('orbit_no={}'.format(form.orbit.data))
        if form.planet.data is not '':
            request_uri_elements.append('uwp={}'.format(form.planet.data))
        if request_uri_elements != []:
            request_uri = '?' + '&'.join(request_uri_elements)
        else:
            request_uri = ''
        current_app.logger.debug('request_uri = %s', request_uri)

        if request_uri != '':
            try:
                current_app.logger.debug(
                    'Calling API endpoint %s%s',
                    base_api_url, request_uri
                )
                resp = requests.get(
                    base_api_url + request_uri
                )
                if resp.status_code == 200:
                    current_app.logger.debug(
                        'API server returned %s', resp.json()
                    )
                    data['planet'] = resp.json()
                else:
                    error_msg = 'Received status {} from API endpoint, message is {}'.format(
                        resp.status_code, resp.json['description'])
                    current_app.logger.debug(error_msg)
            except requests.ConnectionError:
                current_app.logger.debug('Unable to connect to API endpoint')
                error_msg = 'Unable to connect to API server'
        current_app.logger.debug('data = %s', data)

    return render_template(
        'ct_lbb6.html',
        form=form,
        data=data,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS
    )


@main.route('/ct/lbb6/star', methods=['GET', 'POST'])
def ct_lbb6_star():
    '''Handle star query'''
    data = {}
    error_msg = None

    base_api_url = '{}/ct/lbb6/star'.format(
        current_app.config['API_SERVER'])

    form = CTLBB6StarInputForm()
    if form.validate_on_submit():
        current_app.logger.debug('form.star.data = %s', form.star.data)

        current_app.logger.debug('form.star.data = %s', form.star.data)

        request_uri_elements = []
        if form.star.data != '':
            request_uri_elements.append('code={}'.format(form.star.data))
        if request_uri_elements != []:
            request_uri = '?' + '&'.join(request_uri_elements)
        else:
            request_uri = ''
        current_app.logger.debug('request_uri = %s', request_uri)

        if request_uri != '':
            try:
                current_app.logger.debug(
                    'Calling API endpoint %s%s',
                    base_api_url, request_uri
                )
                resp = requests.get(
                    base_api_url + request_uri
                )
                if resp.status_code == 200:
                    current_app.logger.debug(
                        'API server returned %s', resp.json()
                    )
                    data['star'] = resp.json()
                else:
                    error_msg = 'Received status {} from API endpoint, message is {}'.format(
                        resp.status_code, resp.json['description'])
                    current_app.logger.debug(error_msg)
            except requests.ConnectionError:
                current_app.logger.debug('Unable to connect to API endpoint')
                error_msg = 'Unable to connect to API server'
        current_app.logger.debug('data = %s', data)

    return render_template(
        'ct_lbb6.html',
        form=form,
        data=data,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS
    )

@main.route('/ct/lbb6/orbit', methods=['GET', 'POST'])
def ct_lbb6_orbit():
    '''Handle orbit query'''
    data = {}
    error_msg = None

    base_api_url = '{}/ct/lbb6/orbit'.format(
        current_app.config['API_SERVER'])

    form = CTLBB6OrbitInputForm()
    if form.validate_on_submit():
        current_app.logger.debug('form.star.data = %s', form.orbit.data)
        current_app.logger.debug('form.star.data = %s', form.star.data)

        request_uri_elements = []
        if form.orbit.data is not None:
            request_uri_elements.append('orbit_no={}'.format(form.orbit.data))
        if form.star.data != '':
            request_uri_elements.append('star={}'.format(form.star.data))
        if request_uri_elements != []:
            request_uri = '?' + '&'.join(request_uri_elements)
        else:
            request_uri = ''
        current_app.logger.debug('request_uri = %s', request_uri)

        if request_uri != '':
            try:
                current_app.logger.debug(
                    'Calling API endpoint %s%s',
                    base_api_url, request_uri
                )
                resp = requests.get(
                    base_api_url + request_uri
                )
                if resp.status_code == 200:
                    current_app.logger.debug(
                        'API server returned %s', resp.json()
                    )
                    data['orbit'] = resp.json()
                else:
                    error_msg = 'Received status {} from API endpoint, message is {}'.format(
                        resp.status_code, resp.json['description'])
                    current_app.logger.debug(error_msg)
            except requests.ConnectionError:
                current_app.logger.debug('Unable to connect to API endpoint')
                error_msg = 'Unable to connect to API server'
        current_app.logger.debug('data = %s', data)

    return render_template(
        'ct_lbb6.html',
        form=form,
        data=data,
        error_msg=error_msg,
        navbar_items=NAVBAR_ITEMS
    )
