import sqlite3

def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect("golfers.db")

# Initialize DB (create table if it doesn't exist)
def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS golfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            handicap REAL,
            driving_distance REAL,
            putts_per_hole REAL,
            gir REAL,
            approach_accuracy REAL
        )
    ''')
    conn.commit()
    conn.close()

# Add Golfer
def add_golfer(name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO golfers (name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy))
    conn.commit()
    conn.close()

# Get All Golfers
def get_all_golfers():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers")
    rows = c.fetchall()
    conn.close()
    golfers = []
    for row in rows:
        golfers.append({
            "id": row[0],
            "name": row[1],
            "handicap": row[2],
            "driving_distance": row[3],
            "putts_per_hole": row[4],
            "gir": row[5],
            "approach_accuracy": row[6]
        })
    return golfers

# Get Golfer By Name
def get_golfer_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "handicap": row[2],
            "driving_distance": row[3],
            "putts_per_hole": row[4],
            "gir": row[5],
            "approach_accuracy": row[6]
        }
    return None

#Initialize DB on import
create_table()
