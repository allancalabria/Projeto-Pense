import hmac
from functools import wraps
from flask import request, session, g, flash, redirect, url_for


def valid_csrf_token():
    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("_csrf_token", "")
    return bool(session_token and hmac.compare_digest(submitted_token, session_token))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.current_user is None:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("usuarios.login"))
        return view(*args, **kwargs)
    return wrapped_view
