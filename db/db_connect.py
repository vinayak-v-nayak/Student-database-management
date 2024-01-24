import mysql.connector

def get_db():
    config = {
        "host":"localhost",
        "user":"root",
        "password":"",
        "database":"student_database"  
    }
    return mysql.connector.connect(**config)
