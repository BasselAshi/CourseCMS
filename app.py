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
    user = query_db("SELECT username FROM users WHERE username = ? AND password = ?", [
                    username, password], one=True)

    # If invalid username/password
    if user is None:
        return redirect("/login?invalid=true")

    session['user'] = user['username']
    return redirect("/index")


@app.route('/register')
def register():

    # User is already logged in
    if session.get('user') != None:
        return redirect("/index")

    invalid = request.args.get("invalid")
    # Invalid inputs
    if invalid == "true":
        return render_template('register.html', invalid=True)

    return render_template('/register.html', invalid=False)


@app.route('/register_validation', methods=['POST'])
def register_validation():

    username = request.form.get('username')
    password = request.form.get('password')
    role_id = request.form.get('role_id')

    db = get_db()
    db.row_factory = make_dicts

    # Check invalid username/password
    user = query_db("SELECT username FROM users WHERE username = ?", [
                    username], one=True)
    if ((not user is None) or (password == "") or (username == "")):
        return redirect("/register?invalid=true")

    # Insert User and log them in
    query_db("INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)", [
             username, password, role_id])
    get_db().commit()

    session['user'] = username
    return redirect("/index")


@app.route('/')
@app.route('/index')
def index():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('index.html', username=username, roleid=getRank(username))


@app.route('/calendar')
def calendar():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('calendar.html', username=username, roleid=getRank(username))


@app.route('/news')
def news():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('news.html', username=username, roleid=getRank(username))


@app.route('/lectures')
def lectures():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('lectures.html', username=username, roleid=getRank(username))


@app.route('/labs')
def labs():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('labs.html', username=username, roleid=getRank(username))


@app.route('/assignments')
def assignments():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('assignments.html', username=username, roleid=getRank(username))


@app.route('/tests')
def tests():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('tests.html', username=username, roleid=getRank(username))


@app.route('/resources')
def resources():
    username = session.get('user')
    if username is None:
        return redirect('login')
    return render_template('resources.html', username=username, roleid=getRank(username))


@app.route('/feedback')
def feedback():
    username = session.get('user')
    if username is None:
        return redirect('login')

    # Only allow students
    roleid = getRank(username)
    if roleid != '2':
        return redirect('index')

    # Populate instructors
    instructors = getInstructors()

    return render_template('feedback.html', username=username, roleid=roleid, instructors=instructors, submitted=False)


@app.route('/mymarks')
def mymarks():
    username = session.get('user')
    if username is None:
        return redirect('login')

    # Only allow students
    roleid = getRank(username)
    if roleid != '2':
        return redirect('index')

    # Populate marks
    userId = getUserId(username)
    marks = getMarks(userId)

    return render_template('mymarks.html', username=username, roleid=getRank(username), marks=marks)


@app.route('/studentmarks')
def studentmarks():
    username = session.get('user')
    if username is None:
        return redirect('login')

    # Only allow instructors
    roleid = getRank(username)
    if roleid != '1':
        return redirect('index')

    assessments = getAssessments()
    session['assessment_id'] = None

    return render_template('studentmarks.html', username=username, title=None, roleid=getRank(username), assessments=assessments)


@app.route('/selectassessment', methods=['POST'])
def selectassessment():
    username = session.get('user')
    if username is None:
        return redirect('login')

    db = get_db()
    db.row_factory = make_dicts

    # Request assessmentId
    assessmentId = request.form.get("assessmentselect")
    session['assessment_id'] = assessmentId

    # Get the title of the assessment with id = assessmentId
    title = getAsesssmentName(assessmentId)

    # Get marks dictionary
    marks = getMarksByAssessmentId(assessmentId)

    return render_template('studentmarks.html', username=username, title=title, roleid=getRank(username), assessmentId=assessmentId, marks=marks, assessments=getAssessments())


def getAsesssmentName(assessmentId):
    titleDict = query_db("SELECT title FROM assessments WHERE id = ?", [
                         assessmentId], one=True)
    title = str(titleDict['title'])

    return title


@app.route('/studentfeedback')
def studentfeedback():
    username = session.get('user')
    if username is None:
        return redirect('login')

    # Only allow instructors
    roleid = getRank(username)
    if roleid != '1':
        return redirect('index')

    # Populate feedbacks for current instructor
    userId = getUserId(username)
    feedbacks = getFeedbacks(userId)

    return render_template('studentfeedback.html', username=username, roleid=getRank(username), feedbackId=None, feedbacks=feedbacks)


@app.route('/selectfeedback', methods=['POST'])
def selectfeedback():
    username = session.get('user')
    if username is None:
        return redirect('login')

    db = get_db()
    db.row_factory = make_dicts

    feedbackId = request.form.get("feedbackSelect")
    
    # No feedbacks exist
    if feedbackId == None:
        return render_template('studentfeedback.html', feedbackId=feedbackId, exist=False, username=username, roleid=getRank(username), feedbacks=getFeedbacks(getUserId(username)))

    feedback = query_db(
        "SELECT * FROM feedback WHERE id = ?", [feedbackId], one=True)
    q1 = feedback['q1']
    q2 = feedback['q2']
    q3 = feedback['q3']
    q4 = feedback['q4']

    return render_template('studentfeedback.html', username=username, roleid=getRank(username), feedbackId=feedbackId, feedbacks=getFeedbacks(getUserId(username)), q1=q1, q2=q2, q3=q3, q4=q4)


@app.route('/deletefeedback', methods=['POST'])
def deletefeedback():
    username = session.get('user')
    if username is None:
        return redirect('login')

    feedbackId = request.form.get("delete")

    query_db(
        "DELETE FROM feedback WHERE id = " + feedbackId)
    get_db().commit()

    return render_template('studentfeedback.html', username=username, roleid=getRank(username), feedbackId=None, feedbacks=getFeedbacks(getUserId(username)), deleted=True)


def getRank(username):
    db = get_db()
    db.row_factory = make_dicts

    user = query_db(
        "SELECT role_id FROM users WHERE username = ?", [username], one=True)
    return str(user['role_id'])


def getUserId(username):
    db = get_db()
    db.row_factory = make_dicts

    user = query_db(
        "SELECT id FROM users WHERE username = ?", [username], one=True)
    return str(user['id'])


def getInstructors():
    db = get_db()
    db.row_factory = make_dicts

    instructors = query_db(
        "SELECT id, username FROM users WHERE role_id = 1", one=False)

    return instructors


def getFeedbacks(instructorId):
    db = get_db()
    db.row_factory = make_dicts

    feedbacks = query_db(
        "SELECT id FROM feedback WHERE instructor_id = ?", [instructorId], one=False)

    return feedbacks


def getAssessments():
    db = get_db()
    db.row_factory = make_dicts

    assessments = query_db(
        "SELECT id, title FROM assessments", one=False)

    return assessments


def getMarks(user_id):
    db = get_db()
    db.row_factory = make_dicts

    marks = query_db(
        "SELECT m.id as mark_id, m.user_id, m.assessment_id, m.percentage, a.title, r.done FROM marks m LEFT JOIN assessments a on a.id = m.assessment_id LEFT JOIN remarks r on m.id = r.mark_id WHERE m.user_id = ?", [user_id], one=False)

    if len(marks) == 0:
        return None

    return marks


def getMarksByAssessmentId(assessment_id):
    db = get_db()
    db.row_factory = make_dicts
    marks = query_db(
        "SELECT r.id As rId, u.username, m.percentage, r.done, r.reason, m.id  FROM marks m LEFT JOIN users u on u.id = m.user_id LEFT JOIN remarks r on m.id = r.mark_id WHERE m.assessment_id = ?", [assessment_id], one=False)

    if len(marks) == 0:
        return None

    return marks


@app.route('/submitfeedback', methods=['POST'])
def submitfeedback():
    username = session.get('user')
    instructorId = request.form.get('instruc')
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')

    # Insert User and log them in
    query_db("INSERT INTO feedback (instructor_id, q1, q2, q3, q4) VALUES (?, ?, ?, ?, ?)",
             [instructorId, q1, q2, q3, q4])
    get_db().commit()

    return render_template('feedback.html', username=username, roleid=getRank(username), submitted=True)


@app.route('/submitremark', methods=['POST'])
def submitremark():
    markId = request.form.get("submit")
    reason = request.form.get("reason" + markId)

    # Insert assessment remark
    query_db("INSERT INTO remarks (mark_id, done, reason) VALUES (?, 0, ?)", [
             markId, reason])
    get_db().commit()

    return redirect("mymarks")


@app.route('/studentremark', methods=['POST'])
def studentremark():

    username = session.get('user')
    if username is None:
        return redirect('login')

    # Only allow instructors
    roleid = getRank(username)
    if roleid != '1':
        return redirect('index')

    assessments = getAssessments()

    remarkId = request.form.get("resolve")

    if(remarkId != None):
        # Resolve
        query_db("UPDATE remarks SET done = 1 WHERE id = ?", [remarkId])
        get_db().commit()

    else:
        markId = request.form.get("submit")
        newMark = request.form.get("input")

        # Update assessment mark
        query_db("UPDATE marks SET percentage = ? WHERE id = ?",
                 [newMark, markId])
        get_db().commit()

    assessmentId = session.get('assessment_id')
    title = getAsesssmentName(assessmentId)
    marks = getMarksByAssessmentId(assessmentId)

    return render_template('studentmarks.html', username=username, title=title, roleid=getRank(username), marks=marks, assessments=assessments)


if __name__ == '__main__':
    app.run(debug=True)
