from src.common.database import Database


class Player_All(object):

    def __init__(self, name, games_played, wins, draw, loss, points, tourneys_won, room_id, _id):
        self._id = _id
        self.name = name
        self.wins = wins
        self.draw = draw
        self.games_played = games_played
        self.loss = loss
        self.tourneys_won = tourneys_won
        self.points = points
        self.room_id = room_id

    def save_to_mongo(self):
        Database.insert(collection='playersall', data=self.json())

    def update_mongo(self):
        Database.update(collection='playersall', data=self.json(), _id=self.return_json_name())

    def remove_from_mongo(self):
        Database.remove(collection='playersall', data=self.json())

    def return_json_name(self):
        return {
            "name": self.name}

    def json(self):
        return {
            "name": self.name,
            "wins": self.wins,
            "loss": self.loss,
            "draw": self.draw,
            "points": self.points,
            "tourneys_won": self.tourneys_won,
            "games_played": self.games_played,
            "room_id": self.room_id,
            "_id": self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        player_data = Database.find_one(collection="playersall", query={'_id': _id})
        return cls(**player_data)

    @classmethod
    def find_by_id(cls, _id):
        data = Database.find_one("playersall", {"_id": _id})
        if data is not None:
            return cls(**data)
        return None

    @classmethod
    def find_by_room_id(cls, _id):
        players_data = Database.sort("playersall", {"room_id": _id}, "points")
        if players_data is None:
            return None
        else:
            return [cls(**data) for data in players_data]

    @classmethod
    def find_by_name(cls, name):
        name = name.upper()
        data = Database.find_one("playersall", {"name": name})
        if data is not None:
            return cls(**data)
        return None




