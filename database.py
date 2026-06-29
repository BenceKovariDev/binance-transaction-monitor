import sqlite3

def create_and_populate_db():
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tx_hash TEXT PRIMARY KEY,
        user_id TEXT,
        amount_usd REAL,
        timestamp TEXT
    )
    """)

    test_data = [
        ("0x1a2b3c", "USER_NORMAL_1", 900.0, "2026-06-29 11:00:00"),
        ("0x2b3c4d", "USER_NORMAL_1", 950.0, "2026-06-29 11:30:00"),
        
        # A te 5 utalás / 10 perc szabályod teszteléséhez a CSALÓ:
        ("0xaa1111", "USER_LOGIC_2", 980.0, "2026-06-29 11:10:00"),
        ("0xbb2222", "USER_LOGIC_2", 975.0, "2026-06-29 11:12:00"),
        ("0xcc3333", "USER_LOGIC_2", 990.0, "2026-06-29 11:13:00"),
        ("0xdd4444", "USER_LOGIC_2", 960.0, "2026-06-29 11:15:00"),
        ("0xee5555", "USER_LOGIC_2", 985.0, "2026-06-29 11:16:00"),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO transactions (tx_hash, user_id, amount_usd, timestamp)
    VALUES (?, ?, ?, ?)
    """, test_data)

    conn.commit()
    conn.close()
    print("✅ Adatbázis sikeresen létrehozva és feltöltve tesztadatokkal!")

if __name__ == "__main__":
    create_and_populate_db()
