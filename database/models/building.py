
class Building:
    def __init__(self, sqlRow):
        self._id = sqlRow["id"]
        self._abbr = sqlRow["abbr"]
        self._address = sqlRow["addr"]
        self._descrip = sqlRow["descrip"]
        self._building_prose = sqlRow["building_prose"]
        self._total_rating = sqlRow["total_rating"]
        self._n_ratings = sqlRow["n_ratings"]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._descrip
    
    def get_address(self):
        return self._address

    def get_details(self):
        return self._building_prose
    
    def get_rating(self):
        return self._total_rating

    def to_tuple(self):
        # returns (id, name, address, details, ratings)
        return (self._id, self._descrip, self._address, self._building_prose, self._total_rating)

    def to_xml(self):
        pass # TODO ?
        # pattern = '<book>'
        # pattern += '<author>%s</author>'
        # pattern += '<title>%s</title>'
        # pattern += '<price>%f</price>'
        # pattern += '</book>'
        # return pattern % (self._author, self._title, self._price)
