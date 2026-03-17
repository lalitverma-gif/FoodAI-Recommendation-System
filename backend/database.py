import mysql.connector

def connect_db():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lalit6265",
        database="ai_recommendation_system"
    )

    return conn

