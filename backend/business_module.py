from backend.database import connect_db


def add_business(name, category, location, rating):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    # check if business exists
    cursor.execute(
        "SELECT * FROM businesses WHERE name=%s AND location=%s",
        (name, location)
    )
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return "Business already exists"
    query = """
    INSERT INTO businesses(name, category, location, rating)
    VALUES (%s,%s,%s,%s)
    """
    cursor.execute(query,(name,category,location,rating))
    conn.commit()
    conn.close()
    return "Business added successfully"


def get_all_businesses():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM businesses"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def get_business_by_category(category):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM businesses WHERE category=%s"
    cursor.execute(query, (category,))
    result = cursor.fetchall()
    conn.close()
    return result


def search_businesses(search_query):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM businesses WHERE name LIKE %s OR category LIKE %s"
    like_pattern = '%' + search_query + '%'
    cursor.execute(query, (like_pattern, like_pattern))
    result = cursor.fetchall()
    conn.close()
    return result


def get_top_businesses(limit=5):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    # Order by rating descending and limit to top 5
    query = "SELECT * FROM businesses ORDER BY rating DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    conn.close()
    return result
