import sqlite3
from contextlib import closing

DB_FILE = "file:./database/buildings.sqlite?mode=rw"

def query(stmt, values):
    result = []
    with sqlite3.connect(DB_FILE, uri=True) as conn:
        conn.row_factory = sqlite3.Row

        with closing(conn.cursor()) as cursor:
            cursor.execute(stmt, values)
            result = cursor.fetchall()
        
    return result

class Comment:

    def __init__(self, building_id, user_id, comment, date_time, upvotes=None, downvotes=None, tags=None, room_number=None, id=None):
        self.id = id
        self.building_id=building_id
        self.user_id = user_id
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.comment = comment
        self.date_time = date_time
        self.tags = tags
        self.room_number = room_number

        self.username = self.get_username()

    def get_username(self):
        stmt = "SELECT username FROM users WHERE id = ?"
        result = query(stmt, [self.user_id])
        return result[0][0]

    def to_tuple(self):
        return (self.id, self.user_id, self.username, self.comment, self.date_time)