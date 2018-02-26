'''routes.py'''

from . import main
from flask import render_template


@main.route('/')
@main.route('/index')
def index():
    '''Index'''
    intro_text = 'This is home page'
    links = [
        {'text': 'Traveller 5 utilities', 'uri': '/t5/'},
        # {'text': 'Classic Traveller', 'uri': '/ct/'},
        # {'text': 'Miscellaneous links', 'uri': '/misc/'}
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
    intro_text = 'This is T5 page'
    links = [
        {'text': 'T5 cargogen', 'uri': '/t5/cargogen'},
    ]
    return render_template(
        'index.html',
        title='Home',
        intro_text=intro_text,
        links=links)


# @main.route('/misc/')
# def misc_index():
#    '''Misc utilities'''
#    intro_text = 'Miscellaneous utilities'
#    links = [
#        {'text': 'Angular diameter', 'uri': '/misc/angdia'}
#    ]
#    return render_template(
#        'index.html',
#        title='Home',
#        intro_text=intro_text,
#        links=links)
