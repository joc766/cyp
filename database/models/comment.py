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

    def __init__(self, id, building_id, user_id, comment, date_time, rating, current_user=None, up_votes=None, down_votes=None, tags=None, image=None):
        self.id = id
        self.rating = rating
        self.building_id=building_id
        self.user_id = user_id
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.comment = comment
        self.date_time = date_time
        self.tags = tags
        self.image = image

        self.username = self.get_username()
        self.add_comment_votes()
        self.curr_has_voted = False
        if current_user is not None:
            for v in self.votes:
                if v[0] == current_user:
                    self.curr_has_voted = True


    def add_comment_votes(self):
        stmt = "SELECT voter_id, up_vote FROM commentVotes WHERE review_id = ?"
        result = list(query(stmt, [self.id]))
        self.votes = result
        return self.votes


    def get_username(self):
        stmt = "SELECT username FROM users WHERE id = ?"
        result = query(stmt, [self.user_id])
        return result[0][0]

    def to_tuple(self):
        return (self.id, self.user_id, self.username, self.comment, self.date_time, self.rating, self.up_votes, self.down_votes, self.curr_has_voted, self.image)
