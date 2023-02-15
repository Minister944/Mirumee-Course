from app.database import cursor

with cursor() as cur:
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points, hashed_password) VALUES('grzesiu', 'mag', 100, 15, 'test')")
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points, hashed_password) VALUES('pawel', 'tank', 100, 20, 'test')")
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points, hashed_password) VALUES('damian', 'mag', 100, 15, 'test')")
