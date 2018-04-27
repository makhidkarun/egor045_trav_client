'''views.py'''

from flask import render_template
from . import main  # noqa


@main.route('/')
@main.route('/index')
def index():
    '''Index'''
    intro_text = "This is a collection of utilities I've written to " + \
        "ease the burden of refereeing Traveller games."
    links = [
        {'text': 'Traveller 5 utilities', 'uri': '/t5/'},
        {'text': 'Classic Traveller utilities', 'uri': '/ct/'},
        {'text': 'Miscellaneous utilities', 'uri': '/misc/'}
    ]
    return render_template(
        'index.html',
        title='Home',
        intro_text=intro_text,
        links=links)


@main.route('/t5/')
@main.route('/t5/index')
def t5_index():
    '''T5 index'''
    intro_text = 'T5 utilities'
    links = [
        {
            'text': 'T5 cargogen',
            'uri': '/t5/cargogen',
            'api': '/api_doc?endpoint=/t5/cargogen'
        },
        {
            'text': 'T5 orbit details',
            'uri': '/t5/orbit',
            'api': '/api_doc?endpoint=/t5/orbit'
        }
    ]
    navbar_items = []
    return render_template(
        'index.html',
        title='Home',
        header_text='egor045 Traveller Tools - T5',
        intro_text=intro_text,
        links=links,
        navbar_items=navbar_items)


@main.route('/ct/')
@main.route('/ct/index')
def ct_index():
    '''CT index'''
    intro_text = 'Classic Traveller utilities'
    links = [
        {'text': 'LBB2 cargogen', 'uri': '/ct/lbb2/cargogen'},
        {'text': 'LBB6 utilities', 'uri': '/ct/lbb6'}
    ]
    navbar_items = []
    return render_template(
        'index.html',
        title='Home',
        header_text='egor045 Traveller Tools - Classic Traveller',
        intro_text=intro_text,
        links=links,
        navbar_items=navbar_items)


@main.route('/ct/lbb2/cargogen')
@main.route('/ct/lbb2/cargogen/index')
def ct_lbb2_cargogen():
    '''CT LBB2 cargogen index'''
    intro_text = 'Classic Traveller LBB2 cargo utilities'
    links = [
        {
            'text': 'LBB2 purchase cargo',
            'uri': '/ct/lbb2/cargogen/purchase',
            'api': '/api_doc?endpoint=/ct/lbb2/cargogen/purchase'
        },
        {
            'text': 'LBB2 sell cargo',
            'uri': '/ct/lbb2/cargogen/sale',
            'api': '/api_doc?endpoint=/ct/lbb2/cargogen/sale'
        },
        {
            'text': 'LBB2 purchase/sell cargo',
            'uri': '/ct/lbb2/cargogen/purchase_sale'
        }
    ]
    navbar_items = [
        {'label': 'Classic Traveller', 'target': 'main.ct_index'}
    ]
    return render_template(
        'index.html',
        title='Home',
        header_text='egor045 Traveller Tools - Classic Traveller',
        intro_text=intro_text,
        links=links,
        navbar_items=navbar_items)


@main.route('/misc/')
def misc_index():
    '''Misc utilities'''
    intro_text = 'Miscellaneous utilities'
    navbar_items = []
    links = [
        {
            'text': 'Angular diameter',
            'uri': '/misc/angdia',
            'api': '/api_doc?endpoint=/misc/angdia'}
    ]
    return render_template(
        'index.html',
        title='Home',
        intro_text=intro_text,
        header_text='egor045 Traveller Tools - Miscellaneous',
        links=links,
        navbar_items=navbar_items)


@main.route('/ct/lbb6')
@main.route('/ct/lbb6/index')
def ct_lbb6_index():
    '''CT LBB6 index'''
    intro_text = 'CT LBB6 tools'
    links = [
        {
            'text': 'LBB6 planet details',
            'uri': '/ct/lbb6/planet',
            'api': '/api_doc?endpoint=/ct/lbb6/planet'
        },
        {
            'text': 'LBB6 star details',
            'uri': '/ct/lbb6/star',
            'api': '/api_doc?endpoint=/ct/lbb6/star'
        },
        {
            'text': 'LBB6 orbit details',
            'uri': '/ct/lbb6/orbit',
            'api': '/api_doc?endpoint=/ct/lbb6/orbit'
        }
    ]
    navbar_items = [
        {'label': 'Classic Traveller', 'target': 'main.ct_index'}
    ]
    return render_template(
        'index.html',
        title='Home',
        intro_text=intro_text,
        header_text='egor045 Traveller Tools - CT LBB6',
        links=links,
        navbar_items=navbar_items)
