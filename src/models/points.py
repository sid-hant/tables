from src.common.database import Database

class Points(object):
    def __init__(self, _id, ppw, ppd):
        self._id = _id
        self.ppw = ppw
        self.ppd = ppd

    def json(self):
        return {
            "_id": self._id,
            "ppw": self.ppw,
            "ppd": self.ppd
        }

    def return_json_id(self):
        return {
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='pointssetting', data=self.json())

    @classmethod
    def get_points(cls, room_id):
        data = Database.find_one("pointssetting", {"_id": room_id})
        if data is not None:
            return cls(**data)

    def update_mongo(self):
        Database.update(collection='pointssetting', data=self.json(), _id=self.return_json_id())