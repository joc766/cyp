import json
import sqlite3

from contextlib import closing

BUILDINGS_JSON = './all_buildings.json'
DB_FILE = "file:../buildings.sqlite?mode=rw"

def query(stmt, values):
    result = []
    with sqlite3.connect(DB_FILE, uri=True) as conn:
        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt, values)
            result = cursor.fetchall()
        
    return result

def load_all_buildings():
    with open(BUILDINGS_JSON, "r") as file:
        build_json = json.load(file)
        buildings = build_json["ServiceResponse"]["Buildings"]
        for b in buildings:
            values = []
            stmt = (f"INSERT INTO buildings (id, abbr, addr, descrip, building_prose, usage_descrip, site, longitude, latitude, total_rating, n_ratings, facilities) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);\n")
            values.append(int(b.get('BUILDING')))
            values.append(b.get('BUILDING_ABBR'))
            values.append(f"{b.get('ADDR1_ALIAS')}, {b.get('ADDRESS_2')}, {b.get('ADDRESS_3')}")
            values.append(b.get('DESCRIPTION'))
            values.append(b["BUILDING_PROSE"] if b.get('BUILDING_PROSE') else b["DESCRIPTION"])
            values.append(b["USAGE_DESCRIPTION"] if b.get('USAGE_DESCRIPTION') else b["DESCRIPTION"])
            values.append(b.get('SITE'))
            values.append(b.get('LONGITUDE'))
            values.append(b.get('LATITUDE'))
            values.append(float(b['TOTAL_RATING'] if b.get('TOTAL_RATING') else 0.0))
            values.append(int(b['NUMBER_RATINGS'] if b.get('NUMBER_RATINGS') else 0))
            values.append(b['FACILITIES'] if b.get('FACILITIES') else None)
            query(stmt, values)

if __name__ == "__main__":
    load_all_buildings()