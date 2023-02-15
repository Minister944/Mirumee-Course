from http.client import HTTPException
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from crud import *
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

######## JWT ########
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username, password):
    user = get_players_name(db, username)
    print(user)
    if not verify_password(password, user[-1]):
        return False
    return True

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=360)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

######## ROUTERS ########

async def homepage(request):

    with cursor() as cur:
        result = []
        for x in get_players(cur):
            data = {"name":x["name"], "id":x["id"], "password":x["hashed_password"] }
            jwt_token = create_access_token(data)
            x.update({"token":str(jwt_token)})
            result.append(x)

    return JSONResponse(result)

async def get_name(request):
    try:
        name = request.query_params["name"]
    except KeyError:
        raise HTTPException(status_code=404, detail="not found account")

    with cursor() as cur:
        name = get_players_name(cur, name)
    return JSONResponse(name)


PROFESSION = {
    'mag': {"hp":50,"attack":15},
    'tank': {"hp":100,"attack":10}
}

async def get_player_by_id(request):
    # breakpoint()
    try:
        data = await request.json()
        token = data["token"]

        print(token)
    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return JSONResponse({"status":"unautorization"})

    with cursor() as cur:
        player = get_player_by_ids(cur, payload['id'])
    
    if payload['name'] != player['name'] or payload['password'] != player['hashed_password']:
        return JSONResponse({"status":"unautorization"})

    try:
        id = request.query_params["id"]
    except KeyError:
        raise HTTPException(status_code=404, detail="not found account")

    with cursor() as cur:
        player = get_player_by_ids(cur, id)
    return JSONResponse(player)

async def player_create(request):
    data = await request.json()
    profession = data.get('proffession')
    password = data.get('password')


    profession_data = PROFESSION.get(profession)
    print(profession_data)
    data['hp'] = profession_data['hp']
    data['attack'] = profession_data['attack']
    data['hashed_password'] = get_password_hash(password)
    
    with cursor() as cur:
        player = create_player(cur, data)
        player = get_player_by_ids(cur, player.lastrowid)

    result = player
    return JSONResponse(result)

async def change_offline(request):
    id = int(request.path_params['user_id'])
    with cursor() as cur:
        player = offline(cur, id)
    return JSONResponse(player)

async def change_online(request):
    id = int(request.path_params['user_id'])
    with cursor() as cur:
        player = online(cur, id)
    return JSONResponse(player)

    
async def player_attack(request):
    target_id = int(request.path_params['user_id'])
    data = await request.json()

    player_id = data["player_id"] 

    print(player_id)
    with cursor() as cur:
        player = attack(cur, target_id, player_id)
    return JSONResponse(player)

async def authenticate(request):
    data = await request.json()

    password = data["password"] 
    username = data["username"] 

    print(password)
    with cursor() as cur:
        player = authenticate_user(cur, username, password)
    return JSONResponse(player)
app = Starlette(debug=True, routes=[
    Route('/', homepage, methods=["GET"]),
    Route('/get_name', get_name, methods=["GET"]),
    Route("/create_player", player_create, methods=["POST"]),
    Route("/get_player_by_id", get_player_by_id, methods=["GET"]),
    Route("/player/{user_id}/offline", change_offline, methods=["GET"]),
    Route("/player/{user_id}/online", change_online, methods=["GET"]),
    Route("/player/{user_id}/attack", player_attack, methods=["GET"]),
    Route("/player/authenticate", authenticate, methods=["POST"]),
    
])