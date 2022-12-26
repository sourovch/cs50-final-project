from flask import Flask, render_template, session, request, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_paginate import Pagination, get_page_args
from datetime import datetime

from helper import login_required, apology, no_login, get_notes

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///notes.db")


@app.route("/")
@login_required
def index():
    """Render index page"""

    userId = session['user_id']
    notes = db.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 6", userId)
    todos = db.execute(
        "SELECT * FROM todos WHERE user_id = ? ORDER BY id DESC LIMIT 5", userId)

    print(notes)

    return render_template('home.html', notes=notes, todos=todos)


@app.route("/login/", methods=["GET", "POST"])
@no_login
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        notes = db.execute("SELECT * FROM users WHERE username = ?",
                           request.form.get("username"))

        if len(notes) != 1 or not check_password_hash(notes[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = notes[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
@no_login
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not len(username) > 2:
            return apology("username is too small")

        if not (username and password and confirmation):
            return apology("must fill every feald")

        if not password == confirmation:
            return apology("passwords didn't not matched")

        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already exist")

        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
                   username, generate_password_hash(password))

        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?", username)[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/logout/")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route('/notes/')
@login_required
def notes():
    """Renders notes page"""

    user_id = session['user_id']
    date_filter = request.args.get('date')

    if date_filter:
        print(date_filter)
        notes = db.execute(
            "SELECT * FROM notes WHERE user_id = ? AND date = ? ORDER BY id DESC", user_id, date_filter)
    else:
        notes = db.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC", user_id)

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page', per_page=8)

    paginated_notes = get_notes(notes, offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=len(notes))

    dateToday = datetime.now().strftime('%Y-%m-%d')

    return render_template('notes.html', notes=paginated_notes, pagination=pagination, dateToday=dateToday)


@app.route('/notes/add/', methods=["GET", 'POST'])
@login_required
def addNotes():
    """Adds new note"""

    if request.method == 'POST':
        title = request.form.get('title')
        noteBody = request.form.get('note-body')
        if not title:
            return apology("You Must Give Your Note A Title")

        if not noteBody:
            return apology("Note Can't Be Empty")

        if len(title) > 120:
            return apology("Think Of A Smaller Title")

        if len(noteBody) > 1200:
            return apology("Note Can't Be That Big")

        dateTody = datetime.now().strftime("%Y-%m-%d")
        userId = session['user_id']

        db.execute('INSERT INTO notes(title, note, date, user_id) VALUES(?, ?, ?, ?)',
                   title, noteBody, dateTody, userId)

        return redirect('/notes')

    return render_template('add_note.html')


@app.route('/notes/note/<int:noteId>', methods=["GET"])
def readNote(noteId):
    """Provide a single post to user"""

    note = db.execute('SELECT * FROM notes WHERE id = ?', noteId)

    if not note:
        return apology('Note Does not exist')

    user = db.execute(
        'SELECT username FROM users WHERE id = ?', note[0]['user_id'])

    return render_template('note.html', note=note[0], user=user[0])


@app.route('/notes/delete/<int:noteId>', methods=['GET'])
@login_required
def delateNote(noteId):
    """Deletes a note"""

    userId = session['user_id']

    note = db.execute('SELECT * FROM notes WHERE id = ?', noteId)

    if not note:
        return apology("Note Don't Exist")

    if not userId == note[0]['user_id']:
        return apology("Unauthorized", 401)

    db.execute('DELETE FROM notes WHERE id = ?', noteId)

    return redirect('/notes')


@app.route('/notes/edit/<int:noteId>', methods=['GET', 'POST'])
@login_required
def editNote(noteId):
    """Edit a note"""

    userId = session['user_id']
    note = db.execute('SELECT * FROM notes WHERE id = ?', noteId)

    if not note:
        return apology("Note Don't Exist")

    if not userId == note[0]['user_id']:
        return apology("Unauthorized", 401)

    dateTody = datetime.now().strftime("%Y-%m-%d")

    if not note[0]['date'] == dateTody:
        return apology('You Can Only Edit Notes That Written Tody')

    if request.method == 'POST':
        title = request.form.get('title')
        noteBody = request.form.get('note-body')
        if not title:
            return apology("You Must Give Your Note A Title")

        if not noteBody:
            return apology("Note Can't Be Empty")

        if len(title) > 120:
            return apology("Think Of A Smaller Title")

        if len(noteBody) > 1200:
            return apology("Note Can't Be That Big")

        db.execute('UPDATE notes SET title = ?, note = ? WHERE id = ?',
                   title, noteBody, note[0]['id'])

        return redirect('/notes')

    return render_template('edit_note.html', note=note[0])


@app.route('/todos')
@login_required
def todos():
    """Render todo page"""

    userId = session['user_id']
    todos = db.execute(
        "SELECT * FROM todos WHERE user_id = ? ORDER BY id DESC", userId)
    return render_template('todos.html', todos=todos)


@app.route('/todos/add', methods=["GET", "POST"])
@login_required
def addTodos():
    """Adds a todo"""

    if request.method == 'POST':
        todo = request.form.get('todo')

        if not todo:
            return apology("Todo Can't Be Empty")

        if len(todo) > 30:
            return apology('Text is too big')

        db.execute('INSERT INTO todos(todo, user_id) VALUES(?, ?)',
                   todo, session['user_id'])

        return redirect('/todos')

    return render_template('add_todo.html')


@app.route('/todos/delete/<int:todoId>', methods=['GET'])
@login_required
def deleteTodo(todoId):
    """Delete a todo"""

    userId = session['user_id']

    todo = db.execute('SELECT * FROM todos WHERE id = ?', todoId)

    if not todo:
        return apology("Todo Don't Exist")

    if not userId == todo[0]['user_id']:
        return apology("Unauthorized", 401)

    db.execute('DELETE FROM todos WHERE id = ?', todoId)

    return redirect('/todos')


@app.route('/todos/change/<int:todoId>', methods=['GET'])
@login_required
def checkTodo(todoId):
    """Check or uncheck a todo"""

    userId = session['user_id']

    todo = db.execute('SELECT * FROM todos WHERE id = ?', todoId)

    if not todo:
        return apology("Todo Don't Exist")

    if not userId == todo[0]['user_id']:
        return apology("Unauthorized", 401)

    if todo[0]['is_checked'] == 1:
        db.execute('UPDATE todos SET is_checked = ? WHERE id = ?',
                   0, todo[0]['id'])
    else:
        db.execute('UPDATE todos SET is_checked = ? WHERE id = ?',
                   1, todo[0]['id'])

    return jsonify({"status": "ok", "code": "200"}), 200


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def error(e):
    return render_template('error.html', errorText='Page Is Not Available', errorCode=404), 404


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=3000)
