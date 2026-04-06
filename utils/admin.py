from datetime import datetime, timezone

from flask import flash

from utils.storage import get_users, save_users, get_posts


def get_dashboard_stats():
    """Aggregate dashboard statistics for the admin panel.

    Returns:
        dict with keys: total_users, total_posts, admin_count, viewer_count.
    """
    users = get_users()
    posts = get_posts()

    admin_count = sum(1 for u in users if u.get("role") == "admin")
    viewer_count = sum(1 for u in users if u.get("role") == "viewer")

    return {
        "total_users": len(users),
        "total_posts": len(posts),
        "admin_count": admin_count,
        "viewer_count": viewer_count,
    }


def list_users():
    """Return all users.

    Returns:
        list of user dicts.
    """
    return get_users()


def create_user(display_name, username, password, role):
    """Create a new user with validation and role selection.

    Args:
        display_name: Display name string.
        username: Username string.
        password: Password string.
        role: Role string ('admin' or 'viewer').

    Returns:
        dict with user info on success, None on failure.
    """
    if not display_name or not username or not password or not role:
        flash("All fields are required.", "error")
        return None

    if role not in ("admin", "viewer"):
        flash("Role must be 'admin' or 'viewer'.", "error")
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
        "role": role,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    users.append(new_user)
    save_users(users)

    return new_user


def delete_user(user_id, current_user_id):
    """Delete a user with constraints.

    Cannot delete the default admin (id=1) or the currently logged-in user.

    Args:
        user_id: The ID of the user to delete.
        current_user_id: The ID of the currently logged-in admin user.

    Returns:
        True on success, False on failure.
    """
    if user_id == 1:
        flash("Cannot delete the default admin user.", "error")
        return False

    if user_id == current_user_id:
        flash("Cannot delete your own account.", "error")
        return False

    users = get_users()
    updated_users = [u for u in users if u["id"] != user_id]

    if len(updated_users) == len(users):
        flash("User not found.", "error")
        return False

    save_users(updated_users)
    return True