# database.py
import sqlite3

def create_db():
    conn = sqlite3.connect('nvd_data.db')
    cursor = conn.cursor()

    # CVE 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cve_data (
            id TEXT PRIMARY KEY,
            publishedDate TEXT,
            description TEXT,
            severity TEXT,
            vulnerableProducts TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_db()
