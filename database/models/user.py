

class User:
    def __init__(self, sqlRow):
        self.id = sqlRow["id"]
        self.password_hash = sqlRow["password_hash"]
        self.username = sqlRow["username"]
        self.first_name = sqlRow["first_name"]  
        self.last_name = sqlRow["last_name"]
        self.year = sqlRow["year"]
        self.college = sqlRow["college"]

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
