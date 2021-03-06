"""
Routes and views for the flask application.
"""

import os
from datetime import datetime
from flask import render_template, jsonify
from blackboard import app
from blackboard.model import Model
from jinja2 import Environment

from functools import wraps
from flask import redirect, request, current_app

def support_jsonp(func): # see https://gist.github.com/aisipos/1094140
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            resp = func(*args, **kwargs)
            resp.set_data('{}({})'.format(
                str(callback),
                resp.get_data(as_text=True)
            ))
            resp.mimetype = 'application/javascript'
            return resp
        else:
            return func(*args, **kwargs)
    return decorated_function

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)

Model()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        dev_name=os.environ['DEV_NAME'],
        year=datetime.now().year,
        metrics=sorted(Model().output),
        groups=sorted(Model().output['Test 1']),
        json_data=Model().json_output,
        json_info=Model().json_info,
        timestamp=datetimeformat(Model().timestamp)
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        dev_name=os.environ['DEV_NAME'],
        dev_email=os.environ['DEV_EMAIL'],
        year=datetime.now().year,
    )

@app.route('/source')
def source():
    """Renders the source page."""
    return render_template(
        'source.html',
        github_url='https://github.com/yumichael/MAT194-gradeview',
        dev_name=os.environ['DEV_NAME'],
        year=datetime.now().year,
    )

@app.route('/ping')
@support_jsonp
def pong():
    return jsonify(pong=1)