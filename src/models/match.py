import uuid
from src.common.database import Database
import datetime
from src.models.player import Player

class Match(object):
    def __init__(self, p1, p2, p1score, p2score, room_id, date=None, _id=None):
        self._id = self._id = uuid.uuid4().hex if _id is None else _id
        self.p1 = p1
        self.date = datetime.datetime.utcnow()
        self.p1score = p1score
        self.p2 = p2
        self.p2score = p2score
        self.room_id = room_id

    def save_to_mongo(self):
        Database.insert(collection='matches', data=self.json())

    def json(self):
        return {
            "p1":self.p1,
            "p2":self.p2,
            "p1score":self.p1score,
            "p2score":self.p2score,
            "date": self.date,
            "room_id":self.room_id,
            "_id":self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        match_data = Database.find_one(collection="matches", query={'_id': _id})
        return cls(**match_data)


    @classmethod
    def find_by_room_id(cls, _id):
        match_data = Database.sort("matches", {"room_id": _id}, 'date')
        if match_data is None:
            return None
        else:
            return [cls(**data) for data in match_data]

