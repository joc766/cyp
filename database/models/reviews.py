

class Review:
    def __init__(self, sqlRow):
        # self.id = sqlRow['id']
        # self.building_id = sqlRow['building_id']
        # self.user_id = sqlRow['user_id']
        # self.rating = sqlRow['rating']
        self.comment = sqlRow['comment']
        self.date_time = sqlRow['date_time']
        self.up_votes = sqlRow['up_votes']
        self.down_votes = sqlRow['down_votes']
    
    def get_comment(self):
        return self.comment
    
    def to_list(self):
        print([self.comment, self.date_time, self.up_votes, self.down_votes], 'the list')
        return [self.comment, self.date_time, self.up_votes, self.down_votes]
    
    def insert_into_db(self):
        stmt = "INSERT INTO reviews (building_id, user_id, rating, date_time, comment, up_votes, down_votes) VALUES (:building_id, :user_id, :rating, :comment, :date_time, :up_votes, :down_votes)"
        #self.id = insert_query(stmt, list(self.to_dict().values())[1:])

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

