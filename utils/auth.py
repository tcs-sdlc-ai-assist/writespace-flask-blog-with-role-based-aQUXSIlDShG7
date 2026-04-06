from datetime import datetime, timezone
from functools import wraps

from flask import flash, redirect, session, url_for

from utils.storage import get_users, save_users


def login(username, password):
    """Validate credentials and set session state.

    Args:
        username: The username string.
        password: The password string.

    Returns:
        dict with user info on success, None on failure.
    """
    if not username or not password:
        return None

    users = get_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            session["user"] = {
                "user_id": user["id"],
                "username": user["username"],
                "display_name": user["display_name"],
                "role": user["role"],
            }
            return user

    return None


def register(display_name, username, password, confirm_password):
    """Register a new viewer account with validation.

    Args:
        display_name: Display name string.
        username: Username string.
        password: Password string.
        confirm_password: Password confirmation string.

    Returns:
        dict with user info on success, None on failure.
    """
    if not display_name or not username or not password or not confirm_password:
        flash("All fields are required.", "error")
        return None

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return None

    users = get_users()
    for user in users:
        if user["username"] == username:
            flash("Username already exists.", "error")
            return None

    max_id = max((u["id"] for u in users), default=0)
    new_user = {
        "id": max_id + 1,
        "display_name": display_name,
        "username": username,
        "password": password,
        "role": "viewer",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    users.append(new_user)
    save_users(users)

    session["user"] = {
        "user_id": new_user["id"],
        "username": new_user["username"],
        "display_name": new_user["display_name"],
        "role": new_user["role"],
    }

    return new_user


def logout():
    """Clear the current user session."""
    session.pop("user", None)


def get_current_user():
    """Retrieve the current user from session.

    Returns:
        dict with user session info, or None if not logged in.
    """
    return session.get("user", None)


def login_required(f):
    """Decorator that redirects unauthenticated users to the login page."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_current_user() is None:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator that restricts access to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if current_user is None:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        if current_user.get("role") != "admin":
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function