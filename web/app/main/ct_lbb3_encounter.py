'''ct_lbb3_encounter.py'''

import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectMultipleField
from wtforms.validators import Regexp, Optional, Required
from flask import render_template, current_app
from . import main

UWP_REGEXP = r'^[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]$'

NAVBAR_ITEMS = [
    {'label': 'Classic Traveller', 'target': 'main.ct_index'},
    {'label': 'Classic Traveller LBB3 utilities', 'target': 'main.ct_lbb3_index'}
]

TERRAIN_TYPES_TABLE = [
    'Clear',
    'Prairie',
    'Rough',
    'Broken',
    'Mountain',
    'Forest',
    'Jungle',
    'River',
    'Swamp',
    'Marsh',
    'Desert',
    'Beach',
    'Surface',
    'Shallows',
    'Depths',
    'Bottom',
    'Sea Cave',
    'Sargasso',
    'Ruins',
    'Cave',
    'Chasm',
    'Crater'
]


class EnvironmentForm(FlaskForm):
    '''Form for encounter table generation'''
    uwp = StringField(
        'UWP',
        validators=[Optional(), Regexp(UWP_REGEXP)]
    )
    terrain = SelectMultipleField(
        'Terrain',
        choices=[
            ('Clear', 'Clear'),
            ('Prairie', 'Prairie'),
            ('Rough', 'Rough'),
            ('Broken', 'Broken'),
            ('Mountain', 'Mountain'),
            ('Forest', 'Forest'),
            ('Jungle', 'Jungle'),
            ('River', 'River'),
            ('Swamp', 'Swamp'),
            ('Marsh', 'Marsh'),
            ('Desert', 'Desert'),
            ('Beach', 'Beach'),
            ('Surface', 'Surface'),
            ('Shallows', 'Shallows'),
            ('Depths', 'Depths'),
            ('Bottom', 'Bottom'),
            ('Sea+Cave', 'Sea Cave'),
            ('Sargasso', 'Sargasso'),
            ('Ruins', 'Ruins'),
            ('Cave', 'Cave'),
            ('Chasm', 'Chasm'),
            ('Crater', 'Crater'),
        ],
        validators=[Required()]
    )
    table_size = RadioField(
        'Table size',
        choices=[
            ('1', '1D'),
            ('2', '2D')
        ],
        validators=[Required()]
    )
    submit = SubmitField('Submit')


@main.route('/ct/lbb3/encounter', methods=['GET', 'POST'])
def ct_lbb3_encounter():
    '''Encounter table'''
    tables = {}
    error_msg = None
    form = EnvironmentForm()
    base_api_url = '{}/ct/lbb3/encounter'.format(
        current_app.config['API_SERVER'])

    if form.validate_on_submit():
        current_app.logger.debug('form.uwp = %s', form.uwp.data)
        current_app.logger.debug('form.terrain = %s', form.terrain.data)
        current_app.logger.debug('form.table_size = %s', form.table_size.data)

        # Build request_uri
        request_uri_elements = ['size={}'.format(form.table_size.data)]
        if form.uwp.data != '':
            request_uri_elements.append('uwp={}'.format(form.uwp.data))

        # form.terrain.data is a list
        for terrain in form.terrain.data:
            request_uri_base = list(request_uri_elements)
            try:
                request_uri_base.append('terrain={}'.format(terrain))
                request_uri = '&'.join(request_uri_base)
                current_app.logger.debug(
                    'Calling API endpoint %s?%s',
                    base_api_url, request_uri
                )
                resp = requests.get(base_api_url + '?' + request_uri)
                if resp.status_code == 200:
                    current_app.logger.debug(
                        'API server returned %s', resp.json()
                    )
                    tables[terrain] = resp.json()
                else:
                    error_msg = 'Received status {} from API endpoint, message is {}'.format(
                        resp.status_code, resp.json['description']
                    )
                    current_app.logger.debug(error_msg)
            except requests.ConnectionError:
                current_app.logger.debug('Unable to connect to API endpoint')
                error_msg = 'Unable to connect to API server'

    current_app.logger.debug('tables = %s', tables)

    return render_template(
        'ct_lbb3_encounter.html',
        tables=tables,
        error_msg=error_msg,
        form=form,
        uwp=form.uwp.data,
        navbar_items=NAVBAR_ITEMS
    )
