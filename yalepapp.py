from flask import Flask, request, make_response, redirect, url_for, render_template
from flask import render_template
from helpers import get_buildings_by_name

#we are using jinja
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------
#initial page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response


@app.route('/search', methods=['GET'])
def get_buildings():

    building_name = request.args.get('building')
    if (building_name is None) or (building_name.strip() == ''):
        response = make_response('')
        return response

    matches = get_buildings_by_name(building_name)

    html = ''
    pattern = '<button onclick="location.href=\'/info?name=%s\';">%s</button>'
    for building in matches:
        html += pattern % (building.get_name(), building.get_name())
    
    response = make_response(html)
    return response

@app.route('/info', methods=['GET'])
def building_details():
    name = request.args.get('name')
    building = get_buildings_by_name(name)[0]
    building_info = building.to_tuple()

    html = ''
    pattern = '<h5>%s</h5><strong>%s</strong>'
    html += pattern % ('Name', building_info[0])
    html += pattern % ('Address', building_info[1])
    html += pattern % ('Rating', building_info[2])

    #5 star system
    html += '<h6>Rate this Building</h6>'
    star_pattern = '<button onclick="changeRating(%s)">%s</button>'
    for i in range(0,5):
        html += star_pattern % (i+1, i+1)

    response = make_response(html)
    return response


    