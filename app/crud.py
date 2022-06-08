from database import cursor




def get_players(db):
    query = "SELECT rowid, name, proffession, hp, attac_points, status, kills, deaths FROM players ORDER BY rowid"
    players = []
    for player in db.execute(query):
        player_data = player
        print(player)
        players.append(player_data) 
    return players

