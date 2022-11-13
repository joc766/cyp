from flask import Flask, request, make_response, redirect, url_for, render_template, session
from flask import render_template
from helpers import get_buildings_by_name, update_rating, add_comment, get_user_comments
from werkzeug.security import generate_password_hash

from helpers import get_buildings_by_name, update_rating, verify_login
from decorators import login_required
from database.models.user import User

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
            raise(e)
        except ValueError as e:
            # password invalid 
            raise(e)
        
        session['user_id'] = user_id
        return redirect('/')


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

        new_user = User(pwd_hash, username, first_name, last_name, year, college)

        try:
            new_user.insert_into_db()

        except Exception as e:
            raise(e)
    
    return redirect('/login')


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

    building_id = building_info[0]
    name = building_info[1]
    address = building_info[2]
    details = building_info[3]
    rating = building_info[4]

    room_num = 1
    comments = get_user_comments(building_id)

    html = render_template('building.html', building_id=building_id, name=name, 
        address=address, details=details, rating=rating, comments=comments, room_num=room_num)
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

@app.route('/submitComment', methods=['POST'])
def submit_comment():
    building_id = int(request.form.get('building_id'))
    # user_id = session['user_id'] if session['user_id'] else int(1)
    user_id = int(1)
    rating = int(request.form.get('rating'))
    comment = str(request.form.get('commentText'))
    date_time = request.form.get('date_time')
    room_num = int(request.form.get('room_num'))

    store_review = add_comment(building_id, user_id, rating, comment, date_time, room_num)
    response = make_response('SUCCESS')
    response.headers["review"] = store_review
    return response
    
@app.route('/loadComments', methods=['GET'])
def load_comments():
    building_id = request.args.get('building_id')

    comments = get_user_comments(building_id)
    comments = [c['comment'] for c in comments]
    return comments

    