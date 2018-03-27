'''ct_cargogen.py'''

# import logging
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Regexp, NumberRange
from flask import render_template, current_app
from . import main


# current_app.logger = logging.getLogger(__name__)
# current_app.logger.setLevel(logging.ERROR)

UWP_REGEXP = r'^[A-HYX][0-9A-HJ-NP-Z]{6}\-[0-9A-HJ-NP-Z]$'


class CTPurchaseInputForm(FlaskForm):
    '''Input form for CE cargogen'''
    source_uwp = StringField(
        'Source world UWP',
        validators=[Regexp(UWP_REGEXP)])
    submit = SubmitField('Submit')


class CTSaleInputForm(FlaskForm):
    '''Input form for CT cargogen - sell cargo'''
    skill_levels = [
        ('0', 'Skill level 0'),
        ('1', 'Skill level 1'),
        ('2', 'Skill level 2'),
        ('3', 'Skill level 3'),
        ('4', 'Skill level 4'),
        ('5', 'Skill level 5')
    ]
    market_uwp = StringField(
        'Market world UWP',
        validators=[Regexp(UWP_REGEXP)])
    cargo_type = SelectField(
        'Cargo',
        choices=[
            ('Textiles', 'Textiles (Cr3000/ton, 3Dx5 tons)'),
            ('Polymers', 'Polymers (Cr7000/ton, 4Dx5 tons)'),
            ('Liquor', 'Liquor (Cr10000/ton, 1Dx5 tons)'),
            ('Wood', 'Wood (Cr1000/ton, 2Dx10 tons)'),
            ('Crystals', 'Crystals (Cr20000/ton, 1D tons)'),
            ('Radioactives', 'Radioactives (Cr1000000/ton, 1D tons)'),
            ('Steel', 'Steel (Cr500/ton, 4Dx10 tons)'),
            ('Copper', 'Copper (Cr2000/ton, 2Dx10 tons)'),
            ('Aluminum', 'Aluminum (Cr1000/ton, 5Dx10 tons)'),
            ('Tin', 'Tin (Cr9000/ton, 3Dx10 tons)'),
            ('Silver', 'Silver (Cr70000/ton, 1Dx5 tons)'),
            ('Special+Alloys', 'Special Alloys (Cr200000/ton, 1D tons)'),
            ('Petrochemicals', 'Petrochemicals (Cr10000/ton, 1D tons)'),
            ('Grain', 'Grain (Cr300/ton, 8Dx5 tons)'),
            ('Meat', 'Meat (Cr1500/ton, 4Dx5 tons)'),
            ('Spices', 'Spices (Cr6000/ton, 1Dx5 tons)'),
            ('Fruit', 'Fruit (Cr1000/ton, 2Dx5 tons)'),
            ('Pharmaceuticals', 'Pharmaceuticals (Cr100000/ton, 1D tons)'),
            ('Gems', 'Gems (Cr1000000/ton, 2D tons)'),
            ('Firearms', 'Firearms (Cr30000/ton, 2D tons)'),
            ('Ammunition', 'Ammunition (Cr30000/ton, 2D tons)'),
            ('Blades', 'Blades (Cr10000/ton, 2D tons)'),
            ('Tools', 'Tools (Cr10000/ton, 2D tons)'),
            ('Body+Armor', 'Body Armor (Cr50000/ton, 2D tons)'),
            ('Aircraft', 'Aircraft (Cr1000000/unit, 1D units)'),
            ('Air/raft', 'Air/raft (Cr6000000/unit, 1D units)'),
            ('Computers', 'Computers (Cr10000000/unit, 1D units)'),
            ('All+Terrain+Vehicles',
             'All Terrain Vehicles (Cr3000000/unit, 1D units)'),
            ('Armored+Vehicles',
             'Armored Vehicles (Cr7000000/unit, 1D units)'),
            ('Farm+Machinery',
             'Farm Machinery (Cr150000/unit, 1D units)'),
            ('Electronics+Parts',
             'Electronics Parts (Cr100000/ton, 1Dx5 tons)'),
            ('Mechanical+Parts', 'Mechanical Parts (Cr70000/ton, 1Dx5 tons)'),
            ('Cybernetic+Parts', 'Cybernetic Parts (Cr250000/ton, 1Dx5 tons)'),
            ('Computer+Parts', 'Computer Parts (Cr150000/ton, 1Dx5 tons)'),
            ('Machine+Tools', 'Machine Tools (Cr750000/ton, 1Dx5 tons)'),
            ('Vacc+Suits', 'Vacc Suits (Cr400000/ton, 1Dx5 tons)')
        ])
    quantity = IntegerField(
        'Quantity',
        default=1,
        validators=[NumberRange(0, 10000)])
    admin_skill = SelectField(
        'Admin skill',
        choices=skill_levels)
    bribery_skill = SelectField(
        'Bribery skill',
        choices=skill_levels)
    broker_skill = SelectField(
        'Broker skill',
        choices=skill_levels[:5])
    submit = SubmitField('Submit')


@main.route('/ct/lbb2/cargogen/purchase', methods=['GET', 'POST'])
def ct_cargogen_purchase():
    '''Purchase cargo'''
    cargo = {}
    source = None
    base_api_url = '{}/ct/lbb2/cargogen/purchase'.format(
        current_app.config['API_SERVER'])
    form = CTPurchaseInputForm()
    if form.validate_on_submit():
        current_app.logger.debug(
            'form.source_uwp.data = %s', form.source_uwp.data)
        if form.source_uwp.data:
            source = form.source_uwp.data
            request_url = '{}?source_uwp={}'.format(
                base_api_url,
                form.source_uwp.data)
            current_app.logger.debug('Calling API endpoint %s', request_url)
            resp = requests.get(request_url)
            if resp.status_code == 200:
                cargo = resp.json()
                current_app.logger.debug('befor cargo: %s', cargo)
                for modifier in cargo['purchase_dms']:
                    cargo['purchase_dms'][modifier] = \
                        '{:+d}'.format(cargo['purchase_dms'][modifier])
                for modifier in cargo['resale_dms']:
                    cargo['resale_dms'][modifier] = \
                        '{:+d}'.format(cargo['resale_dms'][modifier])
                current_app.logger.debug('after cargo: %s', cargo)
            else:
                current_app.logger.debug(
                    'received status %d from API endpoint',
                    resp.status_code)
        current_app.logger.debug('cargo = %s', cargo)
    return render_template(
        'ct_cargogen_purchase.html',
        source=source,
        cargo=cargo,
        form=form)


@main.route('/ct/lbb2/cargogen/sale', methods=['GET', 'POST'])
def ct_cargogen_sale():
    '''
    Sell cargo
    Specify
    - market UWP
    - cargo
    - quantity
    - broker, admin, bribery skills
    '''
    cargo = None
    market = None
    base_api_url = '{}/ct/lbb2/cargogen/sale'.format(
        current_app.config['API_SERVER'])
    form = CTSaleInputForm()
    if form.validate_on_submit():
        if form.cargo_type.data:
            request_url = '{}?market_uwp={}&cargo={}'.format(
                base_api_url,
                form.market_uwp.data,
                form.cargo_type.data,)
            request_url += '&admin={}&bribery={}&broker={}&quantity={}'.format(
                form.admin_skill.data,
                form.bribery_skill.data,
                form.broker_skill.data,
                form.quantity.data)
            current_app.logger.debug('Calling API endpoint %s', request_url)
            resp = requests.get(request_url)
            if resp.status_code == 200:
                cargo = resp.json()
                market = form.market_uwp.data
            else:
                current_app.logger.debug(
                    'received status %d from API endpoint',
                    resp.status_code)
        current_app.logger.debug('cargo = %s', cargo)
    return render_template(
        'ct_cargogen_sale.html',
        market=market,
        cargo=cargo,
        form=form)
