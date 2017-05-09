from flask import render_template
from flask_login import login_required

from . import home

@home.route('/')
def homepage():
    """
    Render homepage template on route /
    """
    return render_template('home/index.html', title='Ciao, mondo!')

@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')
