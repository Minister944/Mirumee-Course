from app.database import cursor

with cursor() as cur:
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points) VALUES('123', 'nie mag', 34, 44)")
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points) VALUES('asf', 'nie mag', 34, 44)")
    cur.execute("INSERT INTO players(name, proffession, hp, attac_points) VALUES('dfssdfsddfbgk', 'nie mag', 34, 44)")
