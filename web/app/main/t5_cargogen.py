'''T5_cargogen views.py'''

import logging
# import re
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp, Optional
from . import main
from flask import render_template, current_app

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

UWP_REGEXP = r'^[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]$'
# UWPS_REGEXP = r'\b[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]\b'


class SourceWorldForm(FlaskForm):
    '''Source world'''
    source_uwp = StringField(
        'Source world UWP',
        validators=[Regexp(UWP_REGEXP)])
    market_uwp = StringField(
        'Market world UWP (optional)',
        validators=[Regexp(UWP_REGEXP), Optional()])
    submit = SubmitField('Submit')


@main.route('/t5/cargogen', methods=['GET', 'POST'])
def t5_cargogen():
    '''Generate cargo'''
    cargo = {}
    base_api_url = 'https://{}/t5/cargogen'.format(
        current_app.config['API_SERVER'])
    form = SourceWorldForm()
    # source_world_uwp = ''
    # source_world_tcs = ''
    if form.validate_on_submit():
        LOGGER.debug('form.source_uwp.data = %s', form.source_uwp.data)
        LOGGER.debug('form.market_uwp.data = %s', form.market_uwp.data)
        # form.uwp.data is unicode, convert
        if form.source_uwp.data:
            request_url = '{}/source/{}'.format(
                base_api_url,
                form.source_uwp.data)
            if form.market_uwp.data:
                request_url = '{}/market/{}'.format(
                    request_url,
                    form.market_uwp.data)
            LOGGER.debug('Calling API endpoint %s', request_url)
            resp = requests.get(request_url)
            if resp.status_code == 200:
                cargo = resp.json()
            else:
                LOGGER.debug(
                    'received status %d from API endpoint',
                    resp.status_code)
        LOGGER.debug('cargo = %s', cargo)
    return render_template(
        't5_cargogen.html',
        cargo=cargo,
        form=form)
