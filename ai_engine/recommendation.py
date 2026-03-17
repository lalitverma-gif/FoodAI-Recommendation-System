import pandas as pd
from backend.database import connect_db
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(user_id):

    conn = connect_db()

    # Fixed: Changed from 'ratings' to 'interactions' to match user_activity_module.py
    interactions_query = """
    SELECT user_id, business_id, rating
    FROM interactions
    """

    interactions = pd.read_sql(interactions_query, conn)

    # Fixed: Included 'rating' in the SELECT statement as the template depends on it
    business_query = """
    SELECT business_id, name, category, rating
    FROM businesses
    """

    businesses = pd.read_sql(business_query, conn)

    conn.close()

    if interactions.empty:
        return []

    # user-business matrix
    matrix = interactions.pivot_table(
        index="user_id",
        columns="business_id",
        values="rating",
        fill_value=0
    )

    if user_id not in matrix.index:
        return []

    # similarity
    similarity = cosine_similarity(matrix)

    similarity_df = pd.DataFrame(
        similarity,
        index=matrix.index,
        columns=matrix.index
    )

    # top similar users
    similar_users = similarity_df[user_id].sort_values(ascending=False)

    similar_users = similar_users.iloc[1:6].index

    recommended_businesses = []

    for sim_user in similar_users:

        businesses_rated = interactions[
            interactions["user_id"] == sim_user
        ]["business_id"].tolist()

        recommended_businesses.extend(businesses_rated)

    # remove duplicates
    recommended_businesses = list(set(recommended_businesses))

    # remove already rated businesses
    user_rated = interactions[
        interactions["user_id"] == user_id
    ]["business_id"].tolist()

    recommended_businesses = [
        b for b in recommended_businesses if b not in user_rated
    ]

    result = businesses[
        businesses["business_id"].isin(recommended_businesses)
    ]

    # Fixed: Included 'rating' in the returned dictionary items
    return result[["name", "category", "rating"]].to_dict(orient="records")

