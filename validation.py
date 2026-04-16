def is_duplicate(cursor, email):
    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    return cursor.fetchone() is not None
