from flask import render_template

from . import home


@home.route('/')
def homepage():
    """Renders homepage template"""
    return render_template('home/index.html', title='Ciao, mondo!')
