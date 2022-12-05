
class Building:
    def __init__(self, sqlRow):
        self._id = sqlRow["id"]
        self._abbr = sqlRow["abbr"]
        self._address = sqlRow["addr"]
        self._descrip = sqlRow["descrip"]
        self._building_prose = sqlRow["building_prose"]
        self._usage = sqlRow["usage_descrip"]
        self._site = sqlRow["site"]
        self._longitude = sqlRow["longitude"]
        self._latitude = sqlRow["latitude"]
        self._total_rating = sqlRow["total_rating"]
        self._n_ratings = sqlRow["n_ratings"]
        self._facilities = sqlRow["facilities"]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._descrip
    
    def get_address(self):
        return self._address

    def get_details(self):
        return self._building_prose
    
    def get_usage(self):
        return self._usage

    def get_site(self):
        return self._site
    
    def get_lat_long(self):
        return [self._longitude, self._latitude]
    
    def get_rating(self):
        return self._total_rating
    
    def get_facilities(self):
        return self._facilities

    def to_tuple(self):
        # returns (id, name, address, details, ratings)
        return (self._id, self._descrip, self._address, self._building_prose, self._total_rating, self._latitude, self._longitude, self._site, self._usage, self._facilities)

    def to_xml(self):
        pass # TODO ?
        # pattern = '<book>'
        # pattern += '<author>%s</author>'
        # pattern += '<title>%s</title>'
        # pattern += '<price>%f</price>'
        # pattern += '</book>'
        # return pattern % (self._author, self._title, self._price)
