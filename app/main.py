from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from crud import *

async def homepage(request):
    with cursor() as cur:
        result = []
        for x in get_players(cur):
            result.append(x.__dict__) 

    return JSONResponse(result)


app = Starlette(debug=True, routes=[
    Route('/', homepage, methods=["GET"]),
])