from flask import Flask, jsonify
import os
import pymysql
import time

app = Flask(__name__)

# the info is collected from the env file present, gitignore env file
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "exampledb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def get_connection(retries=5, delay=2):
    """Try to connect to the MySQL DB with retries."""
    for i in range(retries):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                port=DB_PORT,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return conn
        except Exception as e:
            print(f"DB connection failed: {e}, retrying...")
            time.sleep(delay)
    raise RuntimeError("Could not connect to DB")

@app.route("/")
def index():
    return jsonify({
        "status": "running",
        "database_host": DB_HOST
    })

@app.route("/users")
def users():
    """Creates a 'users' table if not exists and returns user list."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100)
            );
        """)
        cur.execute("SELECT COUNT(*) AS count FROM users;")
        count = cur.fetchone()['count']
        if count == 0:
            cur.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob');")
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
