import json
import os

DB_LOC = "./createdb.sql"
BLD_JSON = "./starting_buildings.json"


def main():
    if os.path.exists(DB_LOC):
        os.remove(DB_LOC)

    with open(DB_LOC, mode="w") as sql_file:
        starting_info = """PRAGMA foreign_keys = ON;

    DROP TABLE IF EXISTS buildings;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS reviews;
    DROP TABLE IF EXISTS rooms;

    CREATE TABLE buildings(
        id INTEGER, abbr TEXT NOT NULL, addr TEXT NOT NULL, descrip TEXT NOT NULL, building_prose TEXT NOT NULL, total_rating INTEGER NOT NULL, n_ratings INTEGER NOT NULL,
        PRIMARY KEY(id));\n\n"""

        sql_file.write(starting_info)

        with open(BLD_JSON, 'r') as bld_file:

            buildings_json = json.load(bld_file)
            buildings = buildings_json['ServiceResponse']['Buildings']
            for b in buildings:
                # just a way to format the json values into a statement for the .sql file
                stmt = (f"INSERT INTO buildings VALUES("
                    f"{int(b.get('BUILDING'))}, "
                    f"\"{b.get('BUILDING_ABBR')}\","
                    f"\"{b.get('ADDR1_ALIAS')}, {b.get('ADDRESS_2')}, {b.get('ADDRESS_3')}\","
                    f"\"{b.get('DESCRIPTION')}\", "
                    f"\"{b.get('BUILDING_PROSE')}\", "
                    f"{float(b['TOTAL_RATING'] if b.get('TOTAL_RATING') else 0.0)}, " 
                    f"{int(b['NUMBER_RATINGS'] if b.get('NUMBER_RATINGS') else 0)}"
                    ");\n")
                sql_file.write(stmt)

        sql_file.write("\n")

        users_table = """
    CREATE TABLE users(
        id INTEGER, netid TEXT NOT NULL, password TEXT NOT NULL, 
        first_name TEXT NOT NULL, last_name TEXT NOT NULL, college TEXT NOT NULL,
        year INT NOT NULL,
        PRIMARY KEY(id));\n\n"""

        sql_file.write(users_table)
        
        reviews_table = """
    CREATE TABLE reviews(
        id INTEGER, building_id INTEGER NOT NULL, user_id INTEGER NOT NULL, rating INTEGER NOT NULL,
        comment TEXT NOT NULL, date_time DATETIME, room_number INTEGER NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(building_id) REFERENCES buildings(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(room_number) REFERENCES room(id));\n\n"""
    
        sql_file.write(reviews_table)
    
        rooms_table = """
    CREATE TABLE rooms(
        id INTEGER, building_id INTEGER NOT NULL, name TEXT NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(building_id) REFERENCES buildings(id));\n\n"""
    
        sql_file.write(rooms_table)
            

if __name__ == "__main__":
    main()