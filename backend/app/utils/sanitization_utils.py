def escape_like(s: str) -> str:
    """
    Escape special characters in a string for use in SQL LIKE/ILIKE queries.
    """
    if not isinstance(s, str):
        return s
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
