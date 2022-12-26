from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(msg, code=400):
    return render_template('error.html', errorCode=code, errorText=msg), code


def no_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id"):
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


def get_notes(notes, offset=0, per_page=10):
    return notes[offset: offset + per_page]
