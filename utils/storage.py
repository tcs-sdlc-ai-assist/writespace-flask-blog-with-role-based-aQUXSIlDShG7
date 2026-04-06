import json
import os
import tempfile

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
POSTS_FILE = os.path.join(DATA_DIR, "posts.json")

DEFAULT_USERS = [
    {
        "id": 1,
        "display_name": "Admin",
        "username": "admin",
        "password": "adminpass",
        "role": "admin",
        "created_at": "2024-06-01T12:00:00Z",
    }
]

DEFAULT_POSTS = []


def ensure_data_files():
    """Auto-create data/ directory and JSON files if missing."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        _atomic_write(USERS_FILE, DEFAULT_USERS)

    if not os.path.exists(POSTS_FILE):
        _atomic_write(POSTS_FILE, DEFAULT_POSTS)


def get_users():
    """Load and return all users from users.json."""
    ensure_data_files()
    return _read_json(USERS_FILE)


def save_users(users):
    """Save the full users list to users.json atomically."""
    ensure_data_files()
    _atomic_write(USERS_FILE, users)


def get_posts():
    """Load and return all posts from posts.json."""
    ensure_data_files()
    return _read_json(POSTS_FILE)


def save_posts(posts):
    """Save the full posts list to posts.json atomically."""
    ensure_data_files()
    _atomic_write(POSTS_FILE, posts)


def _read_json(filepath):
    """Read and parse a JSON file, returning the parsed data."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, IOError):
        return []


def _atomic_write(filepath, data):
    """Write data to a JSON file atomically using a temp file and rename."""
    dir_name = os.path.dirname(filepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
            json.dump(data, tmp_file, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise