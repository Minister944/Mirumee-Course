from database import cursor
from dataclasses import dataclass
from dataclasses import asdict
from starlette.exceptions import HTTPException

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

@dataclass
class Player:
    id : int
    name : str
    proffession : str
    hp : int
    attac_points : int
    status : str
    kills : int
    deaths : int
    hashed_password: str

#ALL STATUS
#{"status":"player not found"}
#{"status":"arledy"}
#{"status":"ok"}

def get_players(db):
    query = "SELECT rowid, name, proffession, hp, attac_points, status, kills, deaths, hashed_password FROM players ORDER BY rowid"
    players = []
    for player in db.execute(query):
        player_data = Player(*player)
        players.append(asdict(player_data))
        
    return players

def get_player_by_ids(db, id):
    query = "SELECT rowid, name, proffession, hp, attac_points, status, kills, deaths, hashed_password FROM players WHERE rowid=:id"
    params = {'id': id}
    player = db.execute(query, params).fetchone()
    if not player:
        return None
    
    return asdict(Player(*player))


def get_players_name(db, name):
    query = "SELECT rowid, name, proffession, hp, attac_points, status, kills, deaths, hashed_password FROM players WHERE name=:name"
    params = {'name': name}

    player = db.execute(query, params).fetchone()

    if not player:
        raise HTTPException(status_code=404, detail="not found account")

          
    return player

def create_player(db, data):
    query = "INSERT INTO players(name, proffession, hp,attac_points,hashed_password) VALUES (:name, :proffession, :hp, :attack, :hashed_password)"
    player = db.execute(query, data)

    # player.lastrowid
    # get player by id
    # return player data as JSON(DICT)
    return player

def offline(db, id):
    with cursor() as cur:
        player = get_player_by_ids(cur,id)
    if player is None:
        return {"status":"player not found"}
    if player["status"] == "offline":
        return {"status":"arledy"}
    
    query = "UPDATE players SET status='offline' WHERE rowid=:id"
    params = {'id': id}
    player = db.execute(query, params)

    return {"status":"ok"}

def online(db, id):
    with cursor() as cur:
        player = get_player_by_ids(cur,id)
    if player is None:
        return {"status":"player not found"}
    print(player)
    if player["status"] == "online":
        return {"status":"arledy"}
    query = "UPDATE players SET status='online' WHERE rowid=:id"
    params = {'id': id}
    player = db.execute(query, params)

    return {"status":"ok"}


def dead(db, target_id, player_id):
    query = "UPDATE players SET hp=100 WHERE rowid=:id"
    params = {'id': target_id}
    target = db.execute(query, params)
    offline(db, target_id)
    query = "UPDATE players SET deaths=deaths+1 WHERE rowid=:id"
    params = {'id': target_id}
    target = db.execute(query, params)

    query = "UPDATE players SET kills=kills+1 WHERE rowid=:id"
    params = {'id': player_id}
    target = db.execute(query, params)

    return {"status" : "dead"}

def attack(db, target_id, player_id):
    
    with cursor() as cur:
        target = get_player_by_ids(cur,target_id)
        player = get_player_by_ids(cur,player_id)

    if player is None:
        return {"status":"player not found"}
    if target is None:
        return {"status":"target not found"}

    if target["status"] == "offline":
        return {"status":"user is offline"}

    new_hp = target["hp"] - player['attac_points']

    #dead
    if new_hp <= 0:
        with cursor() as cur:
            return dead(cur,target_id, player_id)
        
    with cursor() as cur:
        query = "UPDATE players SET hp=:new_hp WHERE rowid=:id"
        params = {'id': target_id, 'new_hp': new_hp}
        cur.execute(query, params)

        target = get_player_by_ids(cur, target_id)

    return target