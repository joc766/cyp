from flask import Flask, request, make_response, redirect, url_for, render_template, session, jsonify
from flask import render_template
from helpers import get_buildings_by_name, update_rating, get_building_reviews, get_comments_keyword, add_review, vote_for_review, get_user, get_user_reviews
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException, NotFound

from helpers import get_buildings_by_name, update_rating, verify_login, insert_into_db
from decorators import login_required
from database.models.user import User
from datetime import datetime
from flask_session import Session
from tempfile import mkdtemp

#we are using jinja
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = mkdtemp()
Session(app)

#-----------------------------------------------------------------------
#initial page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html') # TODO write login html

    elif request.method == 'POST':
        username = request.form.get('username')
        if not username:
            raise KeyError('no username given') # TODO write an error page
        password = request.form.get('password')
        if not password:
            raise KeyError('no password given')
        
        try:
            user_id = verify_login(username, password)
        except KeyError as e:
            # username invalid
            data = {
                'status': 'FAILURE',
                'message': 'Invalid username'
            }
            return make_response(jsonify(data), 200)
        except ValueError as e:
            # password invalid 
            data = {
                'status': 'FAILURE',
                'message': 'Invalid password'
            }
            return make_response(jsonify(data), 200)
        
        session['user_id'] = user_id
        data = {'status': 'SUCCESS'}
        return make_response(jsonify(data), 200)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        year = request.form.get('year')
        college = request.form.get('college')
        pwd_hash = generate_password_hash(password)

        # new_user = User(pwd_hash, username, first_name, last_name, year, college)

        try:
            user = insert_into_db(username, pwd_hash, first_name, last_name, college, year)

        except Exception as e:
            raise(e)
    
    return redirect('/login')

@app.route('/error', methods=['GET'])
def error():
    error_msg = request.args.get('error_msg')
    return render_template('error.html', error_msg=error_msg)


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
@login_required
def building_details():
    name = request.args.get('name')
    building = get_buildings_by_name(name)[0]
    building_info = building.to_tuple()

    building_id = building_info[0]
    name = building_info[1]
    address = building_info[2]
    details = building_info[3]
    rating = building_info[4]
    latitude = building_info[5]
    longitude = building_info[6]

    # room_num = 1
    comments = get_building_reviews(building_id)
    user_has_commented = False
    for c in comments:
        if c.user_id == session['user_id']:
            user_has_commented = True
    print(user_has_commented)

    html = render_template('building.html', building_id=building_id, name=name, 
        address=address, details=details, rating=rating, latitude=latitude, longitude=longitude, comments=comments, user_has_commented=user_has_commented)
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

@app.route('/submitReview', methods=['POST'])
def submit_comment():
    building_id = int(request.form.get('building_id'))
    # user_id = session['user_id'] if session['user_id'] else int(1)
    user_id = session["user_id"]
    rating = int(request.form.get('rating'))
    comment = str(request.form.get('commentText'))
    date_time = datetime.now()
    # room_num = int(request.form.get('room_num'))

    res = add_review(building_id, user_id, rating, date_time, comment)
    data = {
        "review": res["review"],
        "new_rating": res["new_rating"]
    }
    response = make_response(data)
    return response
    
@app.route('/loadComments', methods=['GET'])
def load_comments():
    building_id = request.args.get('building_id')

    comments = [x.to_tuple() for x in get_building_reviews(building_id)]
    return comments

@app.route('/searchComments', methods=['GET'])
def get_comments():
    building_id = request.args.get('building_id')
    keyword = request.args.get('keyword')
    if (keyword is None) or (keyword.strip() == ''):
        response = make_response('')
        return response

    matches = get_comments_keyword(building_id, keyword)

    html = ''
    pattern = '<button onclick="location.href=\'/info?name=%s\';">%s</button>'
    for building in matches:
        html += pattern % (building.get_name(), building.get_name())
    
    response = make_response(html)
    return response


@app.route("/commentVote", methods=['POST'])
def commentVote():
    print(dict(request.form))
    data = request.form
    
    vote_for_review(data["reviewId"], session["user_id"], 1 if data["value"] == "1" else 0)

    return make_response("SUCCESS")

@app.route('/profile', methods=['GET'])
@login_required
def user_profile():
    #do this but for username
    #building_id = request.args.get('building_id')
    # username = 'hi'
    user = get_user(session["user_id"])
    user_info = user.to_dict()
    c = [x.to_tuple() for x in get_user_reviews(session["user_id"])]
    comments = ""
    pattern = "<div class='col mb-2'>"
    pattern += "<p class='mb-0'>" + "<strong>%s: %s </strong>" + "<br>%s</p>"
    pattern  += "%s<button reviewId='%s' value='1' class='voteBtn btn btn-success' type='button'> <img src='static/images/hand-thumbs-up.svg'/></button>%s<button reviewId='%s' value='-1' class='voteBtn btn btn-danger' type='button'><img src='static/images/hand-thumbs-down.svg'/></button><br><br>"
    pattern  += "</div>"
    for comment in c:
        stars = ""
        for x in range(0, int(comment[5])):
            stars += '★'
        comments += pattern % (comment[2], stars, comment[3], str(comment[6]), str(comment[0]), str(comment[7]), str(comment[0]) )

    html = render_template('profile.html', user=user_info["username"], college=user_info["college"], year=user_info["year"], comments=comments)
    response = make_response(html)
    return response
    

    