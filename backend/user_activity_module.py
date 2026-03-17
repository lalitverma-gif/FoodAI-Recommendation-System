from backend.database import connect_db


def add_interaction(user_id, business_id, rating):

    conn = connect_db()
    cursor = conn.cursor()

    # check if user already rated this business
    check_query = """
    SELECT id FROM interactions
    WHERE user_id=%s AND business_id=%s
    """

    cursor.execute(check_query, (user_id, business_id))
    existing = cursor.fetchone()

    # update rating if already exists
    if existing:

        update_query = """
        UPDATE interactions
        SET rating=%s
        WHERE user_id=%s AND business_id=%s
        """

        cursor.execute(update_query, (rating, user_id, business_id))

        conn.commit()
        conn.close()

        return "Rating updated"

    # insert new rating
    insert_query = """
    INSERT INTO interactions (user_id, business_id, rating)
    VALUES (%s, %s, %s)
    """

    cursor.execute(insert_query, (user_id, business_id, rating))

    conn.commit()
    conn.close()

    return "Interaction saved"
