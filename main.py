from flask import Flask,request
from flask import render_template
from DB import searchDb,updateDb, deleteDb, addDb, indexDb, postDb
from tmdb import tmdb
from datetime import datetime
from pytz import timezone
import sqlite3


def generateHash():
    now = datetime.now(timezone("Asia/Kolkata"))
    hash_value = now.strftime("%Y%m%d%H%M%S%f")
    final_hash = hex(int(hash_value))[2:]
    return final_hash


app = Flask(__name__)
app.secret_key = 'fe1a9cba269660db6066f930313e264b'


def connect():
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TMDB (id, title, genres, poster, date, cast, rating, type, overview)")
    conn.commit()
    conn.close()
connect()


def insert(item):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    id = generateHash()
    cur.execute("INSERT INTO TMDB VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",[id, item.get("title"), item.get("genres"), item.get("poster"), str(item.get("date")), item.get("cast"), item.get("rating"), item.get("type"), item.get("overview")])
    conn.commit()
    conn.close()


def getHome(limit=18, skip=0, search_term=None, order_by='Id', type=None):
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


def getByTmdbID(Id):
    conn = sqlite3.connect('api.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tmdb WHERE id='{Id}'")
    i = cur.fetchone()
    return {'title':i[1],'genres':i[2],'poster':i[3],'date':i[4],'cast':i[5],"rating":i[6],"overview":i[8]}


@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 18))
    search_term = request.args.get('search', None)
    skip = (page - 1) * per_page
    data = getHome(skip=skip,search_term=search_term)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 18 else page + 1
    return render_template('index.html', data=data, perv=perv, next=next)


@app.route('/post/<cat>/<id>')
def post(cat,id):
    post = getByTmdbID(id)
    title = post.get("title")
    date = post.get("date")
    search = title + " " + date[:4] if cat == "movies" else title
    search = ''.join(e for e in search if e.isalnum() or e == " ")
    pattern = '.*' + '.*'.join(search.strip().split(" ")) + '.*'
    query = {"$and": [{"title": {"$regex": pattern, "$options": "i"}}]}
    data = searchDb(cat, sort={'title': 1}, filter=query)
    return render_template('post.html',post=post,data=data)


@app.route('/<cat>/')
def movies(cat):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 18))
    search_term = request.args.get('search', None)
    skip = (page - 1) * per_page
    data = getHome(skip=skip,search_term=search_term,type=cat)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 18 else page + 1
    return render_template('index.html', data=data, perv=perv, next=next)


@app.route("/add/movie",methods=['POST'])
def addMovie():
    Id = request.form.get('tmdb')
    Id = Id[Id.rindex("/")+1:].split("-")[0]
    item = tmdb(Id)
    insert(item)
    return render_template('admin.html')


@app.route("/add/series",methods=['POST'])
def addSeries():
    Id = request.form.get('tmdb')
    Id = Id[Id.rindex("/") + 1:].split("-")[0]
    item = tmdb(Id,"series")
    insert(item)
    return render_template('admin.html')


@app.route("/add/drama",methods=['POST'])
def addDramas():
    Id = request.form.get('tmdb')
    Id = Id[Id.rindex("/") + 1:].split("-")[0]
    item = tmdb(Id,"dramas")
    insert(item)
    return render_template('admin.html')


@app.route("/add/anime",methods=['POST'])
def addAnime():
    Id = request.form.get('tmdb')
    Id = Id[Id.rindex("/") + 1:].split("-")[0]
    item = tmdb(Id,"anime")
    insert(item)
    return render_template('admin.html')






if __name__ == '__main__':
    app.debug = True
    app.run()
