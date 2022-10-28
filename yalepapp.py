from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

#we are using jinja
#-----------------------------------------------------------------------

app = Flask(__name__)

#-----------------------------------------------------------------------
#initial page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response