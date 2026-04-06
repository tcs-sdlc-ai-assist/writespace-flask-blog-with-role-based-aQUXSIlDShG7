def get_avatar(role):
    """Return avatar dict with emoji and color accent based on user role.

    Args:
        role: User role string (e.g., 'admin', 'viewer').

    Returns:
        dict with 'emoji' (str) and 'color' (str) keys.
    """
    role_lower = (role or "").lower()

    avatars = {
        "admin": {"emoji": "👑", "color": "indigo"},
        "viewer": {"emoji": "📖", "color": "teal"},
    }

    return avatars.get(role_lower, {"emoji": "📖", "color": "teal"})