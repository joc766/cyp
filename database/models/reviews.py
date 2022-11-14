from helpers import query, insert_query

class Review:
    def __init__(self, building_id, user_id, rating, date_time, comment, up_votes, down_votes, id = None):
        self.id = id
        self.building_id = building_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.date_time = date_time
        self.up_votes = up_votes
        self.down_votes = down_votes
    
    def insert_into_db(self):
        stmt = "INSERT INTO reviews (building_id, user_id, rating, date_time, comment, up_votes, down_votes) VALUES (:building_id, :user_id, :rating, :comment, :date_time, :up_votes, :down_votes)"
        self.id = insert_query(stmt, list(self.to_dict().values())[1:])

    def to_dict(self):
        d = {
            "id": self.id,
            "building": self.building_id,
            "user": self.user_id,
            "rating": self.rating,
            "date_time": self.date_time,
            "comment": self.comment,
            "up_votes": self.up_votes,
            "down_votes": self.down_votes
        }
        return d

