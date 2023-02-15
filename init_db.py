from app.database import cursor

with cursor() as cur:
    cur.execute('''
        CREATE TABLE players (
        name text UNIQUE NOT NULL,
        proffession text NOT NULL,
        hp INTEGER,
        attac_points INTEGER NOT NULL,
        status text NOT NULL DEFAULT "offline",
        kills INTEGER DEFAULT 0,
        deaths INTEGER DEFAULT 0,
        hashed_password text not NULL
         )
        '''
    )