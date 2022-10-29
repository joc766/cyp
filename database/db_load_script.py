import sqlite3
import json
from contextlib import closing

""" Script opens and sets up the database schema and reads in data from starting_buildings.json 

    Can be used to rebuild the database if something occurs where that is necessary like accidentally 
    emptying the whole db.
"""

def main():
    with open('starting_buildings.json', 'r') as f:
        start = json.load(f)
        buildings = start['ServiceResponse']['Buildings']
        with sqlite3.connect('file:buildings.db?mode=rw', uri=True) as conn:
            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cursor:
                # create the main table
                stmt = "CREATE TABLE buildings\
(id INTEGER PRIMARY KEY,\
abbr TEXT NOT NULL,\
address TEXT NOT NULL,\
descrip TEXT NOT NULL,\
building_prose TEXT NOT NULL,\
total_rating INTEGER NOT NULL,\
n_ratings INTEGER NOT NULL);\
"
                cursor.execute(stmt)
                # load the information into the table (primary keys are auto-generated)
                for b in buildings:
                    stmt = "INSERT INTO buildings (id, abbr, address, descrip, building_prose, total_rating, n_ratings)\
VALUES(:id, :abbr, :address, :descrip, :building_prose, :total_rating, :n_ratings);"
                    values = {
                        'id': b['ID'],
                        'abbr': b['BUILDING_ABBR'],
                        'address': f"{b['ADDR1_ALIAS']}, {b['ADDRESS_2']}, {b['ADDRESS_3']}",
                        'descrip': b['DESCRIPTION'], 
                        'building_prose': b['BUILDING_PROSE'],
                        'total_rating': b['TOTAL_RATING'],
                        'n_ratings': b['NUMBER_RATINGS']
                    }
                    cursor.execute(stmt, values)


            

if __name__ == '__main__':
    main()