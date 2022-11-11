from flask import Flask, request, make_response, redirect, url_for, render_template
from flask import render_template
from helpers import get_buildings_by_name, update_rating, update_user_comments, get_user_reviews

#we are using jinja
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

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

    # user_id = request.args.get('user_id')
    # building_id = building.get_id()
    # reviews = get_user_reviews(building_id)
    reviews = None

    html = render_template('building.html', name=building_info[0], 
        address=building_info[1], rating=building_info[2], comments=reviews)
    response = make_response(html)
    return response

@app.route('/submitRating', methods=['POST'])
def vote():
    building_name = request.form.get('building')
    n_stars = int(request.form.get('n_stars'))

    new_rating= update_rating(building_name, n_stars)

    response = make_response('SUCCESS')
    response.headers["new_rating"] = new_rating
    return response

@app.route('/submitReview', methods=['Post'])
def comment():
    building_name = request.form.get('building')
    submitted_review = request.form.get('review')
    print("submitted_review: ", submitted_review)
    store_review = update_user_comments(submitted_review, building_name)
    response = make_response('SUCCESS')
    response.headers["review"] = store_review
    return response
    


    