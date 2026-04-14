import sqlite3

conn = sqlite3.connect("business.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    plan TEXT,
    execution TEXT,
    critique TEXT
)
""")

conn.commit()


def save_run(user_input, plan, execution, critique):
    cursor.execute(
        "INSERT INTO history (user_input, plan, execution, critique) VALUES (?, ?, ?, ?)",
        (user_input, plan, execution, critique)
    )
    conn.commit()


def get_history():
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    return cursor.fetchall()


# 🔥 ADD THIS
def get_run_by_id(run_id):
    cursor.execute("SELECT * FROM history WHERE id=?", (run_id,))
    return cursor.fetchone()