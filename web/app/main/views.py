'''views.py'''

from . import main
from flask import render_template


@main.route('/')
@main.route('/index')
def index():
    '''Index'''
    intro_text = "This is a collection of utilities I've written to " + \
        "ease the burden of refereeing Traveller games."
    links = [
        {'text': 'Traveller 5 utilities', 'uri': '/t5/'},
        # {'text': 'Classic Traveller', 'uri': '/ct/'},
        {'text': 'Miscellaneous links', 'uri': '/misc/'}
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
    ]
    return render_template(
        'index.html',
        title='Home',
        header_text='egor045 Traveller Tools - T5',
        intro_text=intro_text,
        links=links)


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
