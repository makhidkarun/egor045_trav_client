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
        {'text': 'T5 cargogen', 'uri': '/t5/cargogen'},
        {'text': 'T5 orbit details', 'uri': '/t5/orbit'}
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
        {'text': 'LBB2 cargogen', 'uri': '/ct/lbb2/cargogen'}
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
        {'text': 'LBB2 purchase cargo', 'uri': '/ct/lbb2/cargogen/purchase'},
        {'text': 'LBB2 sell cargo', 'uri': '/ct/lbb2/cargogen/sale'}
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
    links = [
        {'text': 'Angular diameter', 'uri': '/misc/angdia'}
    ]
    return render_template(
        'index.html',
        title='Home',
        intro_text=intro_text,
        links=links)
