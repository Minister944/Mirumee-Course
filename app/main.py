from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from crud import *

async def homepage(request):
    with cursor() as cur:
        result = get_players(cur)

    return JSONResponse(result)


app = Starlette(debug=True, routes=[
    Route('/', homepage, methods=["GET"]),
])