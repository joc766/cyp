import sqlite3
from contextlib import closing
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import FileStorage
import io


from database.models.building import Building
from database.models.user import User
from database.models.comment import Comment
from database.models.reviews import Review


DB_FILE = "file:./database/buildings.sqlite?mode=rw"

# TODO write general query function

def query(stmt, values):
    result = []
    with sqlite3.connect(DB_FILE, uri=True) as conn:
        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:
            if values == None:
                cursor.execute(stmt)
            else:
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
    stmt = "SELECT id, password_hash FROM users  WHERE username = ?;"
    result = query(stmt, [username])
    if len(result) == 0:
        raise KeyError('username not found')
    pwd_hash = result[0][1]
    if not check_password_hash(pwd_hash, password):
        raise ValueError('incorrect password')

    return result[0][0] # returns id


def get_buildings_by_name(name):
    buildings = []

    stmt = "SELECT id, abbr, descrip, building_prose, addr, usage_descrip, site, longitude, latitude, total_rating, n_ratings, facilities FROM buildings WHERE \
            descrip LIKE :descrip;"
    values = {"descrip": '%' + name + '%'}
    
    results = query(stmt, values)
    
    for row in results:
        building = Building(row)
        buildings.append(building)
    
    return buildings

def get_building_by_id(building_id):
    stmt = "SELECT descrip FROM buildings WHERE id = ?"
    results = query(stmt, [building_id])
    return results[0][0]


def update_rating(building_id, n_stars):
    stmt1 = "SELECT total_rating, n_ratings, id FROM buildings WHERE id = ?"
    result = query(stmt1, [building_id])[0]
    total_rating = float(result[0])
    n_ratings = int(result[1])

    new_rating = float(((total_rating * n_ratings) + n_stars) / (n_ratings + 1))
    stmt2 = "UPDATE buildings SET total_rating = ?, n_ratings = ? WHERE id = ?"
    query(stmt2, [new_rating, n_ratings + 1, result[2]])
    return new_rating


def add_review(building_id, user_id, rating, date_time, comment, image):
    '''update user with submitted comment'''
    stmt = "INSERT INTO reviews (building_id, user_id, rating, date_time, comment, up_votes, down_votes, image_id) VALUES (?, ?, ?, ?, ?, 0, 0, ?)"
    review_id = insert_query(stmt, [building_id, user_id, rating, date_time, comment, image])
    new_rating = update_rating(building_id, rating)
    return {"review": review_id, "new_rating": new_rating}


def get_user_comments(building_id, curr_user):
    stmt = "SELECT r.id AS id, r.rating AS rating, r.user_id AS user_id, r.comment AS comment, r.date_time AS date_time,\
r.up_votes AS up_votes, r.down_votes AS down_votes, img.id AS image_id, img.filename AS filename \
FROM reviews AS r INNER JOIN images AS img ON r.image_id = img.id WHERE r.building_id = ? ORDER BY up_votes - down_votes DESC"
    result = query(stmt, [building_id])
    comments = []
    for x in result:
        new = Comment(x["id"], building_id, x["user_id"], x["comment"], x["date_time"], x["rating"], up_votes=x["up_votes"], down_votes=x["down_votes"], image_id=x["image_id"], img_name=f"imageServe/{ x['image_id'] } ", current_user=curr_user)
        comments.append(new)
    return comments

def get_building_reviews(building_id):
    stmt = "SELECT reviews.id, reviews.rating, reviews.user_id, reviews.comment, reviews.date_time, reviews.up_votes, reviews.down_votes, images.image FROM reviews NATURAL JOIN images WHERE reviews.building_id = ?"
    result = query(stmt, [building_id])
    return [Comment(x["id"], building_id, x["user_id"], x["comment"], x["date_time"], x["rating"], up_votes=x["up_votes"], down_votes=x["down_votes"]) for x in result]

def insert_into_db(username, pwd_hash, first_name, last_name, college, year):
    stmt = "INSERT INTO users (username, password_hash, first_name, last_name, college, year) VALUES (:username, :hash, :first, :last, :college, :year);"
    id = insert_query(stmt, [username, pwd_hash, first_name, last_name, college, year])
    

# def get_building_reviews(building_name):
#     stmt = "SELECT reviews.comment FROM reviews JOIN buildings WHERE buildings.descrip = ?"
#     return query(stmt, [building_name])
def get_user_reviews(user_id):
    stmt = "SELECT r.building_id AS building_id, r.id AS id, r.rating AS rating, r.user_id AS user_id, r.comment AS comment, r.date_time AS date_time,\
    r.up_votes AS up_votes, r.down_votes AS down_votes, img.id AS image_id, img.filename AS filename \
    FROM reviews AS r INNER JOIN images AS img ON r.image_id = img.id WHERE r.user_id = ? ORDER BY up_votes - down_votes DESC"
    result = query(stmt, [user_id])
    comments = []
    for x in result:
        new = Comment(x["id"], x["building_id"], x["user_id"], x["comment"], x["date_time"], x["rating"], up_votes=x["up_votes"], down_votes=x["down_votes"], image_id=x["image_id"], img_name=f"imageServe/{ x['image_id'] } ", current_user=user_id)
        comments.append(new)
    return comments

    # stmt = "SELECT id, rating, user_id, comment, date_time, up_votes, down_votes, building_id FROM reviews WHERE user_id = ?"
    # result = query(stmt, [user_id])
    # return [Comment(x["id"], x["building_id"], x["user_id"], x["comment"], x["date_time"], x["rating"], up_votes=x["up_votes"], down_votes=x["down_votes"]) for x in result]


def get_all_users():
    stmt = "SELECT id, password_hash, username, first_name, last_name, year, college FROM users"
    results = query(stmt, None)
    users = []
    for user_info in results:
        users.append(User(user_info))
    return users


def get_user(user_id):

    stmt = "SELECT id, password_hash, username, first_name, last_name, year, college FROM users WHERE id = ?"
    
    results= query(stmt, [user_id])
    user = User(results[0])
    return user


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


def get_reviews_keyword(building_id, keyword, curr_user):
    stmt = "SELECT r.building_id AS building_id, r.id AS id, r.rating AS rating, r.user_id AS user_id, r.comment AS comment, r.date_time AS date_time,\
r.up_votes AS up_votes, r.down_votes AS down_votes, img.id AS image_id, img.filename AS filename \
FROM reviews AS r INNER JOIN images AS img ON r.image_id = img.id WHERE r.building_id = ? AND r.comment LIKE ? ORDER BY up_votes - down_votes DESC"
    result = query(stmt, [building_id, '%' + keyword + '%'])
    comments = []
    for x in result:
        new = Comment(x["id"], x["building_id"], x["user_id"], x["comment"], x["date_time"], x["rating"], up_votes=x["up_votes"], down_votes=x["down_votes"], image_id=x["image_id"], img_name=f"imageServe/{ x['image_id'] } ", current_user=curr_user)
        comments.append(new)
    return comments


def vote_for_review(review_id, voter_id, is_upvote):
    if is_upvote:
        stmt = "UPDATE reviews SET up_votes = up_votes + 1 WHERE id = ?"
    else:
        stmt = "UPDATE reviews SET down_votes = down_votes + 1 WHERE id = ?"
    query(stmt, [review_id])
    stmt2 = "INSERT INTO commentVotes (review_id, voter_id, up_vote) VALUES (?, ?, ?)"
    query(stmt2, [review_id, voter_id, is_upvote])

    return 


def vote_for_review(review_id, voter_id, is_upvote):
    if is_upvote:
        stmt = "UPDATE reviews SET up_votes = up_votes + 1 WHERE id = ?"
    else:
        stmt = "UPDATE reviews SET down_votes = down_votes + 1 WHERE id = ?"
    query(stmt, [review_id])
    stmt2 = "INSERT INTO commentVotes (review_id, voter_id, up_vote) VALUES (?, ?, ?)"
    query(stmt2, [review_id, voter_id, is_upvote])

    return 


def get_buildings_by_tag(tag):
    buildings = []

    stmt = "SELECT id, abbr, descrip, building_prose, addr, usage_descrip, site, longitude, latitude, total_rating, n_ratings, facilities FROM buildings WHERE LOWER(site) = ? OR LOWER(usage_descrip) = ?;"
    
    results = query(stmt, [tag.lower(), tag.lower()])
    
    for row in results:
        building = Building(row)
        buildings.append(building)

    return buildings 

def get_votes(review_ids):
    stmt = "SELECT voter_id FROM commentVotes WHERE review_id IN ?"
    return query(stmt, [review_ids])


def upload_image_to_db(file: FileStorage):
    binary_data = file.stream.read()

    stmt = "INSERT INTO images (image) VALUES (?);"
    return insert_query(stmt, [binary_data])

def get_image(img_id):
    stmt = "SELECT image FROM images WHERE id = ?;"
    result = query(stmt, [img_id])
    img = result[0]["image"]
    print(type(img))
    return io.BytesIO(img)