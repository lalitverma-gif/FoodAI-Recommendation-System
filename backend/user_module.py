from backend.database import connect_db


def register_user(name, email, password):

    conn = connect_db()
    cursor = conn.cursor()

    # check if user already exists
    cursor.execute(
        "SELECT id FROM users WHERE email=%s",
        (email,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"status": "error", "message": "User already exists"}

    query = """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, password))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "User registered successfully"}


def login_user(email, password):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT id, name, email
    FROM users
    WHERE email=%s AND password=%s
    """

    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "status": "success",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        }
    else:
        return {"status": "error", "message": "Invalid email or password"}
