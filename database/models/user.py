from helpers import query, insert_query

class User:
    def __init__(self, password_hash, username, first_name, last_name, year, college, user_id=None):
        self.id = user_id
        self.password_hash = password_hash
        self.username = username
        self.first_name = first_name    
        self.last_name = last_name
        self.year = year
        self.college = college

    def insert_into_db(self):
        stmt = "INSERT INTO users (username, password_hash, first_name, last_name, college, year) VALUES (:username, :hash, :first, :last, :college, :year);"
        self.id = insert_query(stmt, self.to_dict())

    def to_dict(self):
        d = {
            "id": self.id,
            "username": self.username,
            "hash": self.password_hash,
            "first": self.first_name,
            "last": self.last_name,
            "year": self.year,
            "college": self.college
        }
        return d
