import sqlite3 as sq


def db_start():
    global db, cur

    db = sq.connect('D:\PythonProjects\WeatherBot\database\cities.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS cities(user_id TEXT PRIMARY KEY, city TEXT)")
    db.commit()


def add_city(user_id, city):
    global cur
    user = cur.execute("SELECT 1 FROM cities WHERE user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO cities VALUES(?, ?)", (user_id, city))
        db.commit()


def get_city_from_db(user_id):
    city = cur.execute("SELECT city FROM cities WHERE user_id = ? ", (user_id,)).fetchone()
    return city[0]


def edit_city(user_id, city):
    cur.execute("UPDATE cities SET city = ? WHERE user_id = ?", (city, user_id))
    db.commit()


def check_user(user_id):
    query = cur.execute("SELECT 1 FROM cities WHERE user_id = ?", (user_id,)).fetchone()
    if query:
        return True
    else:
        return False
