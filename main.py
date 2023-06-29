from flask import Flask,request
from flask import render_template
from db import searchDb,updateDb, deleteDb, addDb, indexDb, postDb
from tmdbv3api import TMDb
from tmdbv3api import Movie,TV
from datetime import datetime
from pytz import timezone


def generateHash():
    now = datetime.now(timezone("Asia/Kolkata"))
    hash_value = now.strftime("%Y%m%d%H%M%S%f")
    final_hash = hex(int(hash_value))[2:]
    return final_hash


app = Flask(__name__)
tmdb = TMDb()
tmdb.api_key = 'fe1a9cba269660db6066f930313e264b'
app.secret_key = 'many random bytes'


@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 18))
    search_term = request.args.get('search', '')
    pattern = '.*' + '.*'.join(search_term.strip().split(" ")) + '.*'
    query = {"$and": [{"title": {"$regex": pattern, "$options": "i"}}]} if search_term != '' else {}
    skip = (page - 1) * per_page
    data = indexDb(filter=query, skip=skip, limit=per_page)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 18 else page + 1
    return render_template('index.html', data=data, perv=perv, next=next)


@app.route('/post/<cat>/<id>')
def post(cat,id):
    post = postDb(id)
    search = post.get('search')
    search = ''.join(e for e in search if e.isalnum() or  e==" ")
    pattern = '.*' + '.*'.join(search.strip().split(" ")) + '.*'
    query = {"$and": [{"title": {"$regex": pattern, "$options": "i"}}]}
    data = searchDb(cat, sort={'title':1}, filter=query)
    return render_template('post.html',post=post,data=data)


@app.route('/<cat>/')
def movies(cat):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 20))
    search_term = request.args.get('search', '')
    pattern = '.*' + '.*'.join(search_term.strip().split(" ")) + '.*'
    query = {"$and": [{"title": {"$regex": pattern, "$options": "i"}}]} if search_term != '' else {}
    skip = (page - 1) * per_page
    sort = -1 if cat == "movies" else 1
    data = searchDb(cat,sort={"Id":sort}, filter=query, skip=skip, limit=per_page)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 20 else page + 1
    channel = "1001672758629" if cat == "movies" else "1001885286768" if cat == "series" else "1001943439473"
    return render_template('view.html', data=data, perv=perv, next=next,channel=channel)


@app.route('/admin/<cat>/')
def adminc(cat):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 40))
    search_term = request.args.get('search', '')
    sort = int(request.args.get('sort', 1))
    sort = -1 if cat == "movies" else 1
    pattern = '.*' + '.*'.join(search_term.strip().split(" ")) + '.*'
    query = {"$and": [{"title": {"$regex": pattern, "$options": "i"}}]} if search_term != '' else {}
    skip = (page - 1) * per_page
    data = searchDb(cat, sort={'Id':sort}, filter=query, skip=skip, limit=per_page)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 40 else page + 1
    return render_template('manage.html', data=data, perv=perv, next=next,channel=cat)


@app.route("/update/<channel>/<id>",methods=['POST'])
def update(channel,id):
    title = request.json.get('title')
    updateDb(channel,int(id),title)
    return {'title':title,'id':'b'+id}


@app.route("/delete/<channel>/<id>",methods=['POST'])
def delete(channel,id):
    deleteDb(channel,int(id))
    return "ok"


@app.route("/add/movie",methods=['POST'])
def addMovie():
    tmdb = request.form.get('tmdb')
    tmdb = tmdb[tmdb.rindex("/")+1:].split("-")[0]
    movie = Movie()
    Id = generateHash()
    try:
        res = movie.details(int(tmdb))
        overview = res.overview
        title = res.title + " ("+res.release_date[:4]+")"
        search = title.replace('(','').replace(')','')
        poster = "https://image.tmdb.org/t/p/w500"+res.poster_path
        document = {'Id':Id,'title':title,'search':search,'type':'movies','overview':overview,'poster':poster}
        addDb(document)
    except:
        pass
    return render_template('admin.html')


@app.route("/add/series",methods=['POST'])
def addSeries():
    tmdb = request.form.get('tmdb')
    tmdb = tmdb[tmdb.rindex("/")+1:].split("-")[0]
    tv = TV()
    Id = generateHash()
    try:
        res = tv.details(int(tmdb))
        overview = res.overview
        title = res.name + " ("+res.first_air_date[:4]+")"
        search = res.name
        poster = "https://image.tmdb.org/t/p/w500"+res.poster_path
        document = {'Id':Id,'title':title,'search':search,'type':'series','overview':overview,'poster':poster}
        addDb(document)
    except:
        pass
    return render_template('admin.html')

@app.route("/add/drama",methods=['POST'])
def addDramas():
    tmdb = request.form.get('tmdb')
    tmdb = tmdb[tmdb.rindex("/")+1:].split("-")[0]
    tv = TV()
    Id = generateHash()
    try:
        res = tv.details(int(tmdb))
        overview = res.overview
        title = res.name + " ("+res.first_air_date[:4]+")"
        search = res.name
        poster = "https://image.tmdb.org/t/p/w500"+res.poster_path
        document = {'Id':Id,'title':title,'search':search,'type':'dramas','overview':overview,'poster':poster}
        addDb(document)
    except:
        pass
    return render_template('admin.html')


@app.route("/add/anime",methods=['POST'])
def addAnime():
    tmdb = request.form.get('tmdb')
    tmdb = tmdb[tmdb.rindex("/")+1:].split("-")[0]
    tv = TV()
    Id = generateHash()
    try:
        res = tv.details(int(tmdb))
        overview = res.overview
        title = res.name + " ("+res.first_air_date[:4]+")"
        search = res.name
        poster = "https://image.tmdb.org/t/p/w500"+res.poster_path
        document = {'Id':Id,'title':title,'search':search,'type':'anime','overview':overview,'poster':poster}
        addDb(document)
    except:
        pass
    return render_template('admin.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
