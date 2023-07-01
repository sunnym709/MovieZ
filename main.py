from flask import Flask,request
from flask import render_template
from DB import connect, getIndex, getFomTMDBByID, insertToTMDB, getItems, updateItems, deleteItems, addItems,updatePosts
from tmdb import tmdb


app = Flask(__name__)
app.secret_key = 'fe1a9cba269660db6066f930313e264b'
connect()


@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 18))
    search_term = request.args.get('search', None)
    skip = (page - 1) * per_page
    data = getIndex(skip=skip,search_term=search_term)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 18 else page + 1
    return render_template('index.html', data=data, perv=perv, next=next)


@app.route('/post/<cat>/<id>')
def post(cat,id):
    post = getFomTMDBByID(id)
    title = post.get("title")
    date = post.get("date")
    search = title + " " + date[:4] if cat == "movies" else title
    search = ''.join(e for e in search if e.isalnum() or e == " ")
    data = getItems(cat, search)
    return render_template('post.html',post=post,data=data)


@app.route('/<cat>/')
def movies(cat):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 18))
    search_term = request.args.get('search', None)
    skip = (page - 1) * per_page
    data = getIndex(skip=skip,search_term=search_term,type=cat)
    perv = None if page == 1 else page - 1
    next = None if len(data) != 18 else page + 1
    return render_template('index.html', data=data, perv=perv, next=next)


@app.route("/posts/add/<cat>/<id>",methods=['GET'])
def pAdd(cat,id):
    item = tmdb(id,cat)
    insertToTMDB(item)
    return "Success"


@app.route("/posts/update/<id>/<title>",methods=['GET'])
def pUpdate(id,title):
    updatePosts(id,title)
    return "Success"


@app.route("/update/<cat>/<id>/<title>",methods=['GET'])
def update(cat,id,title):
    updateItems(cat,id,title)
    return "Success"


@app.route("/add/<cat>/<id>/<title>",methods=['GET'])
def add(cat,id,title):
    print(cat,id,title)
    addItems(cat,id,title)
    return "Success"


@app.route("/delete/<cat>/<id>",methods=['GET'])
def delete(cat,id):
    deleteItems(cat,id)
    return "Success"


if __name__ == '__main__':
    app.debug = True
    app.run()
