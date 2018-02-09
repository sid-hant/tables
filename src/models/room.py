import uuid
from flask import session
from src.common.database import Database
from src.models.match import Match
from src.models.player import Player
from src.models.points import Points
from src.models.player_all import Player_All

class Room(object):

    def __init__(self, password, name, _id=None):
        self._id = self._id = uuid.uuid4().hex if _id is None else _id
        self.password = password
        self.name = name

    def save_to_mongo(self):
        Database.insert('rooms', self.json())

    def json(self):
        return {
            "password": self.password,
            "_id": self._id,
            "name": self.name
        }

    @classmethod
    def from_mongo(cls, _id):
        room_data = Database.find_one(collection="rooms", query={'_id': _id})
        return cls(**room_data)

    @classmethod
    def find_by_id(cls, _id):
        data = Database.find_one("rooms", {"_id": _id})
        if data is not None:
            return cls(**data)
        return None

    @staticmethod
    def login_valid(room_id, password):
        room = Room.find_by_id(room_id)
        if room is not None:
            return room.password == password
        return False

    @staticmethod
    def login(room_id):
        session['_id'] = room_id

    @staticmethod
    def new_player(name, room_id):
        name = name.upper()
        player = Player(name,0,0,0,0,0,0,room_id)
        player_all = Player_All(name,0,0,0,0,0,0,room_id,player._id)
        player.save_to_mongo()
        player_all.save_to_mongo()

    @staticmethod
    def new_match(p1,p2,p1score,p2score,room_id):
        match = Match(p1,p2,p1score,p2score,room_id)
        match.save_to_mongo()

    @staticmethod
    def remove_player(name):
        name = name.upper()
        find_player = Player.find_by_name(name)
        if find_player is not None:
            find_player.remove_from_mongo()
            pAll = Player_All.find_by_name(name)
            pAll.remove_from_mongo()
        else:
            return None

    def remove_room(self):
        _id = self._id
        Database.remove('pointssetting', {'_id':_id})
        Database.remove('players', {'room_id':_id})
        Database.remove('matches', {'room_id': _id})
        Database.remove('playersall', {'room_id': _id})
        Database.remove(collection='rooms', data=self.json())
        session['_id'] = 67207220660863

    @staticmethod
    def update_table(p1, p2, p1score, p2score):
        p1 = p1.upper()
        p2 = p2.upper()
        room_id = session['_id']
        points = Points.get_points(room_id)
        player1_data = Database.find_one("players", {"name": p1})
        player2_data = Database.find_one("players", {"name": p2})

        if player1_data and player2_data is not None:
            if p1score > p2score:
                winner = Player.find_by_name(p1)
                winner.wins = winner.wins + 1
                winner.games_played = winner.games_played + 1
                winner.points = winner.points + int(points.ppw)
                loser = Player.find_by_name(p2)
                loser.loss = loser.loss + 1
                loser.games_played = loser.games_played + 1

                winnertot = Player_All.find_by_name(p1)
                winnertot.wins = winner.wins + 1
                winnertot.games_played = winnertot.games_played + 1
                winnertot.points = winnertot.points + int(points.ppw)
                losertot = Player_All.find_by_name(p2)
                losertot.loss = losertot.loss + 1
                losertot.games_played = losertot.games_played + 1

                winner.update_mongo()
                loser.update_mongo()
                winnertot.update_mongo()
                losertot.update_mongo()

            elif p2score > p1score:
                winner = Player.find_by_name(p2)
                winner.wins = winner.wins + 1
                winner.games_played = winner.games_played + 1
                winner.points = winner.points + int(points.ppw)
                loser = Player.find_by_name(p1)
                loser.loss = loser.loss + 1
                loser.games_played = loser.games_played + 1

                winnertot = Player_All.find_by_name(p2)
                winnertot.wins = winnertot.wins + 1
                winnertot.games_played = winnertot.games_played + 1
                winnertot.points = winnertot.points + int(points.ppw)
                losertot = Player_All.find_by_name(p1)
                losertot.loss = losertot.loss + 1
                losertot.games_played = losertot.games_played + 1

                winner.update_mongo()
                loser.update_mongo()
                winnertot.update_mongo()
                losertot.update_mongo()

            else:
                p1 = Player.find_by_name(p1)
                p2 = Player.find_by_name(p2)
                p1.draw = p1.draw + int(points.ppd)
                p2.draw = p2.draw + int(points.ppd)
                p1.points = p1.points + 1
                p2.points = p2.points + 1

                p1tot = Player_All.find_by_name(p1)
                p2tot = Player_All.find_by_name(p2)
                p1tot.draw = p1tot.draw + int(points.ppd)
                p2tot.draw = p2tot.draw + int(points.ppd)
                p1tot.points = p1tot.points + 1
                p2tot.points = p2tot.points + 1

                p1.update_mongo()
                p2.update_mongo()
                p1tot.update_mongo()
                p2tot.update_mongo()
        else:
            return None

    def get_players(self):
        return Player.find_by_room_id(self._id)

    def get_matches(self):
        return Match.find_by_room_id(self._id)

    def end_season(self):
        players = self.get_players()
        current_winner = None
        current_winner_points = 0
        for player in players:
            if current_winner == None:
                current_winner = player._id
                current_winner_points = player.points
            elif player.points > current_winner_points:
                current_winner = player._id
                current_winner_points = player.points
            player.wins = 0
            player.draw = 0
            player.games_played = 0
            player.loss = 0
            player.points = 0
            player.update_mongo()
        winner = Player.find_by_id(current_winner)
        winner.tourneys_won += 1
        winner.update_mongo()



