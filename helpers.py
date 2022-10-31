import sqlite3
from contextlib import closing

from building import Building

db_file = "file:database/buildings.db?mode=rw"

# TODO write general query function
def get_buildings_by_name(name):
    buildings = []
    
    with sqlite3.connect(db_file, uri=True) as conn:

        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:

            stmt = "SELECT id, abbr, descrip, building_prose, address, total_rating, n_ratings FROM buildings WHERE \
descrip LIKE :descrip;"
            values = {"descrip": '%' + name + '%'}
            cursor.execute(stmt, values)

            row = cursor.fetchone()
            while row is not None:
                building = Building(row)
                buildings.append(building)
                row = cursor.fetchone()
    
    return buildings

def update_rating(building_name, n_stars):

    with sqlite3.connect(db_file, uri=True) as conn:

        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:

            stmt1 = "SELECT total_rating, n_ratings, id FROM buildings WHERE descrip = ?"
            cursor.execute(stmt1, [building_name])
            result = cursor.fetchone()
            total_rating = float(result[0])
            n_ratings = int(result[1])

            new_rating = float(((total_rating * n_ratings) + n_stars) / (n_ratings + 1))
            stmt2 = "UPDATE buildings SET total_rating = ?, n_ratings = ? WHERE id = ?"
            cursor.execute(stmt2, [new_rating, n_ratings + 1, result[2]])
            return new_rating