import sqlite3
import os
from flask import Flask, render_template, request, g, url_for, flash
from DataBase import FDataBase
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aasdaaf234fafd34f'

@app.route('/')
def index():
    print(url_for('index'))
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu() ,posts=dbase.getPostsAnonce(),title='Literature__leisure')

@app.route('/about')
def about():
    db = get_db()
    dbase = FDataBase(db)
    print(url_for('about'))
    return render_template('about.html', title='Literature__leisure', menu=dbase.getMenu(),posts=dbase.getPostsAnonce())

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        res = dbase.addContact(request.form['username'], request.form['email'],request.form['message'])
        if len(request.form['username']) > 4 and '@' in (request.form['email']):
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        print(request.form)
    return render_template('contacts.html', title='Контакты', menu=dbase.getMenu() ,posts=dbase.getPostsAnonce())

@app.errorhandler(404)

def Pagenotfound(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu())

def connect_db():
    conn = sqlite3.connect(r'main.db', uri =True)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/add_post', methods=['POST', "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'],request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

if __name__ == '__main__':
    app.run(debug=True)
