import sqlite3
from contextlib import closing

from database.models.building import Building

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


def add_comment(building_id, user_id, rating, comment, date_time, room_number):
    '''update user with submitted comment'''
    stmt = "INSERT INTO reviews (building_id, user_id, rating, comment, room_number) VALUES (?, ?, ?, ?, ?, ?)"
    result = query(stmt, [building_id, user_id, rating, comment, room_number])
    return result

def get_user_comments(building_id):
    stmt = "SELECT comment FROM reviews WHERE building_id = ?"
    result = query(stmt, [building_id])
    return result

# def get_user_reviews(user_id):
#     stmt = "SELECT comment FROM reviews WHERE user_id = ?"
#     result = query(stmt, [user_id])
#     return result


def get_building_reviews(building_name):
    stmt = "SELECT reviews.comment FROM reviews JOIN buildings WHERE buildings.descrip = ?"
    return query(stmt, [building_name])