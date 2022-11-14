import sqlite3
from contextlib import closing
from werkzeug.security import generate_password_hash, check_password_hash


from database.models.building import Building
from database.models.reviews import Review


DB_FILE = "file:./database/buildings.sqlite?mode=rw"

# TODO write general query function

def query(stmt, values):
    result = []
    with sqlite3.connect(DB_FILE, uri=True) as conn:
        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt, values)
            result = cursor.fetchall()
        
    return result

def insert_query(stmt, values):
    with sqlite3.connect(DB_FILE, uri=True) as conn:

        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt, values)
            row_id = cursor.lastrowid
        
    return row_id

def verify_login(username, password):
    stmt = "SELECT id, password_hash FROM users WHERE username = ?;"
    result = query(stmt, [username])
    if len(result) == 0:
        raise KeyError('username not found')
    pwd_hash = result[0][1]
    if not check_password_hash(pwd_hash, password):
        raise ValueError('incorrect password')

    return result[0][0] # returns id


def get_buildings_by_name(name):
    buildings = []

    stmt = "SELECT id, abbr, descrip, building_prose, addr, total_rating, n_ratings FROM buildings WHERE \
            descrip LIKE :descrip;"
    values = {"descrip": '%' + name + '%'}
    
    results = query(stmt, values)
    
    for row in results:
        building = Building(row)
        buildings.append(building)
    
    return buildings


def update_rating(building_name, n_stars):
    stmt1 = "SELECT total_rating, n_ratings, id FROM buildings WHERE descrip = ?"
    result = query(stmt1, [building_name])[0]
    total_rating = float(result[0])
    n_ratings = int(result[1])

    new_rating = float(((total_rating * n_ratings) + n_stars) / (n_ratings + 1))
    stmt2 = "UPDATE buildings SET total_rating = ?, n_ratings = ? WHERE id = ?"
    query(stmt2, [new_rating, n_ratings + 1, result[2]])
    return new_rating


def add_comment(building_id, user_id, rating, date_time, comment):
    '''update user with submitted comment'''
    stmt = "INSERT INTO reviews (building_id, user_id, rating, date_time, comment, up_votes, down_votes) VALUES (?, ?, ?, ?, ?, 0, 0)"
    result = query(stmt, [building_id, user_id, rating, date_time, comment])
    return result

def get_reviews(building_id):
    reviews = []
    stmt = "SELECT comment, date_time, up_votes, down_votes FROM reviews WHERE building_id = ?"
    #stmt = "SELECT id, building_id, user_id, rating, comment, date_time, up_votes, down_votes FROM reviews WHERE building_id = ?"
    results = query(stmt, [building_id])
    for row in results:
        review = Review(row)
        reviews.append(review)
    return reviews

def get_building_reviews(building_name):
    stmt = "SELECT reviews.comment FROM reviews JOIN buildings WHERE buildings.descrip = ?"
    return query(stmt, [building_name])

def update_comment_voting(is_upvote, review_id):
    stmt1 = "SELECT up_votes, down_votes FROM reviews WHERE id = ?"
    result = query(stmt1, [review_id])[0]
    up_votes = int(result[0])
    down_votes = int(result[1])
    if is_upvote:
        stmt2 = "UPDATE reviews SET up_votes = ? WHERE id = ?"
        up_votes += 1
        query(stmt2, [up_votes, review_id])
    else:
        stmt2 = "UPDATE reviews SET up_votes = ? WHERE id = ?"
        down_votes += 1
        query(stmt2, [down_votes, review_id])
    return [up_votes, down_votes]

def get_reviews_keyword(building_id, keyword):
    reviews = []
    stmt = "SELECT comment, date_time, up_votes, down_votes FROM reviews WHERE building_id = ? AND comment LIKE ?"
    results = query(stmt, [building_id, '%'+keyword+'%'])
    for row in results:
        review = Review(row)
        reviews.append(review)
    return reviews
