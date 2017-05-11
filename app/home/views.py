from flask import render_template
from flask_login import login_required

from . import home

@home.route('/')
def homepage():
    """Renders homepage template"""
    return render_template('home/index.html', title='Ciao, mondo!')

@home.route('/dashboard')
@login_required
def dashboard():
    """Renders dashboard template if logged in"""
    return render_template('home/dashboard.html', title='Dashboard')
