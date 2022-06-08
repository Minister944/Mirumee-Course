from database import cursor

class Player:
    def __init__(self, id, name, proffession, hp, attac_points, status, kills, deaths ) -> None:
        self.id = id
        self.name = name
        self.proffession = proffession
        self.hp = hp
        self.attac_points = attac_points
        self.status = status
        self.kills = kills
        self.deaths = deaths



def get_players(db):
    query = "SELECT rowid, name, proffession, hp, attac_points, status, kills, deaths FROM players ORDER BY rowid"
    players = []
    for player in db.execute(query):
        player_data = Player(*player)
        players.append(player_data)
        
    return players

