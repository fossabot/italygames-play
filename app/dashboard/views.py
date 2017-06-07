from flask import render_template
from flask_login import login_required

from . import dashboard

@dashboard.route('/')
@login_required
def homepage():
    """Renders dashboard template if logged in"""
    return render_template('dashboard/index.html', title='Dashboard')
