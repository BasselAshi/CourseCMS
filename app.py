# required imports
# the sqlite library allows us to communicate with the sqlite database
import sqlite3
# we are adding the import 'g' which will be used for the database
from flask import Flask, render_template, request, g, session, redirect

DATABASE = './database.db'

# the function get_db is taken from here
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# the function query_db is taken from here
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# the function make_dicts is taken from here
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


app = Flask(__name__)
app.secret_key = 'CSCB20'

# the function close_connection is taken from here
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()


@app.route('/login')
def login():
    # Check if already logged in
    if session.get('user') != None:
        return redirect("/index")

    # Check if login unsuccessful
    invalid = request.args.get("invalid")
    if invalid == "true":
        return render_template('login.html', invalid=True)

    # db = get_db()
    # db.row_factory = make_dicts

    # employees = []
    # for employee in query_db('SELECT * FROM users'):
    #     employees.append(employee)

    # db.close()
    # return render_template('login.html', employee=employees)
    return render_template('login.html', invalid=False)


@app.route('/logout')
def logout():
    session['user'] = None
    return redirect("/login")


@app.route('/validation', methods=['POST'])
def validation():
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    db.row_factory = make_dicts
    user = query_db("SELECT username FROM users WHERE username = '" +
                    username + "' AND password = '" + password + "'", one=True)

    # If invalid username/password
    if user is None:
        return redirect("/login?invalid=true")

    session['user'] = user['username']
    return redirect("/index")


@app.route('/')
@app.route('/index')
def index():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('index.html', username=username)


@app.route('/calendar')
def calendar():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('calendar.html', username=username)


@app.route('/news')
def news():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('news.html', username=username)


@app.route('/lectures')
def lectures():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('lectures.html', username=username)


@app.route('/labs')
def labs():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('labs.html', username=username)


@app.route('/assignments')
def assignments():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('assignments.html', username=username)


@app.route('/tests')
def tests():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('tests.html', username=username)


@app.route('/resources')
def resources():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('resources.html', username=username)


@app.route('/feedback')
def feedback():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('feedback.html', username=username)
