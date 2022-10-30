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
