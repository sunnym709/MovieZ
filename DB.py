from datetime import datetime
from pytz import timezone
import sqlite3


def generateHash():
    now = datetime.now(timezone("Asia/Kolkata"))
    hash_value = now.strftime("%Y%m%d%H%M%S%f")
    return hex(int(hash_value))[2:]


def connect():
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS MOVIES (id, title)")
    cur.execute("CREATE TABLE IF NOT EXISTS SERIES (id, title)")
    cur.execute("CREATE TABLE IF NOT EXISTS DRAMAS (id, title)")
    cur.execute("CREATE TABLE IF NOT EXISTS ANIME (id, title)")
    cur.execute("CREATE TABLE IF NOT EXISTS TMDB (id, title, genres, poster, date, cast, rating, type, overview)")
    conn.commit()
    conn.close()


def insertToTMDB(item):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    id = generateHash()
    cur.execute("INSERT INTO TMDB VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",[id, item.get("title"), item.get("genres"), item.get("poster"), str(item.get("date")), item.get("cast"), item.get("rating"), item.get("type"), item.get("overview")])
    conn.commit()
    conn.close()


def getIndex(limit=18, skip=0, search_term=None, order_by='Id', type=None):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    query = "SELECT id, title, type, poster FROM TMDB"
    params = []
    if search_term:
        search_terms = search_term.split()
        query += " WHERE " + " AND ".join(["title LIKE ?"] * len(search_terms))
        params.extend(['%' + term + '%' for term in search_terms])
    if type:
        if params:
            query += " AND"
        else:
            query += " WHERE"
        query += " type = ?"
        params.append(type)
    query += f" ORDER BY {order_by} DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    cur.execute(query, params)
    rows = cur.fetchall()
    result = [{'Id': i[0], 'title': i[1], 'type': i[2], 'poster': i[3]} for i in rows]
    cur.close()
    conn.close()
    return result


def getFomTMDBByID(Id):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM TMDB WHERE id='{Id}'")
    i = cur.fetchone()
    return {'title':i[1],'genres':i[2],'poster':i[3],'date':i[4],'cast':i[5],"rating":i[6],"overview":i[8]}


def getItems(table,search_term):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    query = f"SELECT id, title FROM {table.upper()}"
    channel = 1001672758629 if table == "movies" else 1001885286768 if table == "series" else 1001943439473 if table == "dramas" else 1001805372983
    params = []
    if search_term:
        search_terms = search_term.split()
        query += " WHERE " + " AND ".join(["title LIKE ?"] * len(search_terms))
        params.extend(['%' + term + '%' for term in search_terms])
    query += f" ORDER BY title"
    cur.execute(query, params)
    rows = cur.fetchall()
    result = [{'Id': i[0], 'title': i[1], 'channel':channel} for i in rows]
    cur.close()
    conn.close()
    return result

def addItems(table,id,title):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table.upper()} VALUES (?, ?)",[str(id), str(title)])
    conn.commit()
    conn.close()


def updateItems(table,id,title):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE {table.upper()} SET title='{title}' WHERE id='{id}'")
    conn.commit()
    conn.close()


def deleteItems(table,id):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table.upper()} WHERE id='{id}'")
    conn.commit()
    conn.close()


def updatePosts(id,title):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    print(f"UPDATE TMDB title='{title}' WHERE id='{id}'")
    cur.execute(f"UPDATE TMDB SET title='{title}' WHERE id='{id}'")
    conn.commit()
    conn.close()
