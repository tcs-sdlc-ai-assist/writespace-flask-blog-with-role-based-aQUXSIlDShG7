from datetime import datetime, timezone

from flask import Flask, flash, redirect, render_template, request, session, url_for

from config import Config
from utils.auth import (
    admin_required,
    get_current_user,
    login,
    login_required,
    logout,
    register,
)
from utils.admin import create_user, delete_user, get_dashboard_stats, list_users
from utils.avatar import get_avatar
from utils.storage import ensure_data_files, get_posts, save_posts

app = Flask(__name__)
app.config.from_object(Config)

ensure_data_files()


@app.context_processor
def inject_globals():
    return {
        "get_avatar": get_avatar,
        "current_user": get_current_user(),
    }


# ===== Error Handlers =====

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# ===== Landing Page =====

@app.route("/")
def home():
    posts = get_posts()
    posts_sorted = sorted(posts, key=lambda p: p.get("created_at", ""), reverse=True)
    recent_posts = posts_sorted[:6]
    return render_template("index.html", recent_posts=recent_posts)


# ===== Auth Routes =====

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if get_current_user():
        return redirect(url_for("blogs"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = login(username, password)
        if user:
            flash("Welcome back, {}!".format(user["display_name"]), "success")
            return redirect(url_for("blogs"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register_route():
    if get_current_user():
        return redirect(url_for("blogs"))

    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        user = register(display_name, username, password, confirm_password)
        if user:
            flash("Account created successfully! Welcome, {}!".format(user["display_name"]), "success")
            return redirect(url_for("blogs"))

    return render_template("register.html")


@app.route("/logout")
def logout_route():
    logout()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# ===== Blog Routes =====

@app.route("/blogs")
@login_required
def blogs():
    posts = get_posts()
    posts_sorted = sorted(posts, key=lambda p: p.get("created_at", ""), reverse=True)
    return render_template("blogs.html", posts=posts_sorted)


@app.route("/blogs/write", methods=["GET", "POST"])
@login_required
def write_blog():
    current_user = get_current_user()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template("write_blog.html", post=None)

        posts = get_posts()
        max_id = max((p["id"] for p in posts), default=0)

        new_post = {
            "id": max_id + 1,
            "title": title,
            "content": content,
            "author_id": current_user["user_id"],
            "author_name": current_user["display_name"],
            "author_role": current_user["role"],
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        posts.append(new_post)
        save_posts(posts)

        flash("Post published successfully!", "success")
        return redirect(url_for("read_blog", post_id=new_post["id"]))

    return render_template("write_blog.html", post=None)


@app.route("/blogs/<int:post_id>")
@login_required
def read_blog(post_id):
    posts = get_posts()
    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("blogs"))

    return render_template("read_blog.html", post=post)


@app.route("/blogs/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog(post_id):
    current_user = get_current_user()
    posts = get_posts()
    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("blogs"))

    if current_user["role"] != "admin" and current_user["user_id"] != post["author_id"]:
        flash("You do not have permission to edit this post.", "error")
        return redirect(url_for("read_blog", post_id=post_id))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template("write_blog.html", post=post)

        post["title"] = title
        post["content"] = content
        save_posts(posts)

        flash("Post updated successfully!", "success")
        return redirect(url_for("read_blog", post_id=post_id))

    return render_template("write_blog.html", post=post)


@app.route("/blogs/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_blog(post_id):
    current_user = get_current_user()
    posts = get_posts()
    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("blogs"))

    if current_user["role"] != "admin" and current_user["user_id"] != post["author_id"]:
        flash("You do not have permission to delete this post.", "error")
        return redirect(url_for("read_blog", post_id=post_id))

    updated_posts = [p for p in posts if p["id"] != post_id]
    save_posts(updated_posts)

    flash("Post deleted successfully!", "success")
    return redirect(url_for("blogs"))


# ===== Admin Routes =====

@app.route("/admin")
@admin_required
def admin_dashboard():
    stats = get_dashboard_stats()
    posts = get_posts()
    posts_sorted = sorted(posts, key=lambda p: p.get("created_at", ""), reverse=True)
    recent_posts = posts_sorted[:10]
    return render_template("admin_dashboard.html", stats=stats, recent_posts=recent_posts)


@app.route("/admin/users", methods=["GET", "POST"])
@admin_required
def admin_users():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "viewer")

        user = create_user(display_name, username, password, role)
        if user:
            flash("User '{}' created successfully!".format(user["display_name"]), "success")
            return redirect(url_for("admin_users"))

    users = list_users()
    return render_template("user_management.html", users=users)


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    current_user = get_current_user()
    success = delete_user(user_id, current_user["user_id"])
    if success:
        flash("User deleted successfully!", "success")
    return redirect(url_for("admin_users"))


# ===== URL Rule Aliases for templates =====

app.add_url_rule("/login", endpoint="login", view_func=login_route)
app.add_url_rule("/register", endpoint="register", view_func=register_route)
app.add_url_rule("/logout", endpoint="logout", view_func=logout_route)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])