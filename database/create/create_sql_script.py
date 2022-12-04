import json
import os

DB_LOC = "./createdb.sql"
BLD_JSON = "../all_buildings.json"


def main():
    if os.path.exists(DB_LOC):
        os.remove(DB_LOC)

    with open(DB_LOC, mode="w") as sql_file:
        starting_info = """PRAGMA foreign_keys = ON;

    DROP TABLE IF EXISTS reviews;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS buildings;
    DROP TABLE IF EXISTS commentVotes;
    DROP TABLE IF EXISTS images;

    CREATE TABLE buildings(
        id INTEGER PRIMARY KEY AUTOINCREMENT, abbr TEXT NOT NULL, addr TEXT NOT NULL, descrip TEXT NOT NULL, building_prose TEXT NOT NULL, usage_descrip TEXT, site TEXT NOT NULL, longitude FLOAT, latitude FLOAT, total_rating INTEGER NOT NULL, n_ratings INTEGER NOT NULL);\n\n"""

        sql_file.write(starting_info)

        # with open(BLD_JSON, 'r') as bld_file:

        #     buildings_json = json.load(bld_file)
        #     buildings = buildings_json['ServiceResponse']['Buildings']
        #     for b in buildings:
        #         # just a way to format the json values into a statement for the .sql file
        #         stmt = (f"INSERT INTO buildings VALUES("
        #             f"{int(b.get('BUILDING'))}, "
        #             f"\"{b.get('BUILDING_ABBR')}\","
        #             f"\"{b.get('ADDR1_ALIAS')}, {b.get('ADDRESS_2')}, {b.get('ADDRESS_3')}\","
        #             f"\"{b.get('DESCRIPTION')}\", "
        #             f"\"{b.get('BUILDING_PROSE')}\", "
        #             f"\"{b.get('USAGE_DESCRIPTION')}\", "
        #             f"\"{b.get('SITE')}\", "
        #             f"\"{b.get('LONGITUDE')}\", "
        #             f"\"{b.get('LATITUDE')}\", "
        #             f"{float(b['TOTAL_RATING'] if b.get('TOTAL_RATING') else 0.0)}, " 
        #             f"{int(b['NUMBER_RATINGS'] if b.get('NUMBER_RATINGS') else 0)}"
        #             ");\n")
        #         sql_file.write(stmt)

        sql_file.write("\n")

        users_table = """
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password_hash TEXT NOT NULL, 
        first_name TEXT NOT NULL, last_name TEXT NOT NULL, college TEXT NOT NULL,
        year INT NOT NULL);\n\n"""

        sql_file.write(users_table)
        
        reviews_table = """
    CREATE TABLE reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT, building_id INTEGER NOT NULL, user_id INTEGER NOT NULL, rating INTEGER NOT NULL,
        comment TEXT NOT NULL, date_time DATETIME, up_votes INTEGER NOT NULL, down_votes INTEGER NOT NULL, image_id INTEGER,
        FOREIGN KEY(building_id) REFERENCES buildings(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
        FOREIGN KEY(image_id) REFERENCES images(id));\n\n"""
    
        sql_file.write(reviews_table)

        commentVotes_table = """
    CREATE TABLE commentVotes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, review_id INTEGER NOT NULL, voter_id INTEGER NOT NULL, up_vote INTEGER NOT NULL,
        FOREIGN KEY(review_id) REFERENCES reviews(id),
        FOREIGN KEY(voter_id) REFERENCES users(id));\n\n"""

        sql_file.write(commentVotes_table)

        images_table = """
    CREATE TABLE images(
        id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, filename TEXT
        );\n\n
    """

        sql_file.write(images_table)
    
    #     rooms_table = """
    # CREATE TABLE rooms(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT, building_id INTEGER NOT NULL, name TEXT NOT NULL,
    #     FOREIGN KEY(building_id) REFERENCES buildings(id));\n\n"""
    
    #     sql_file.write(rooms_table)
            

if __name__ == "__main__":
    main()
