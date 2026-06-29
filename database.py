import sqlite3

def create_and_populate_db():
    # Kapcsolódás az adatbázishoz
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    # TÁBLA ÚJRAALAPOZÁSA (Töröljük a régit, hogy tiszta lappal induljunk)
    cursor.execute("DROP TABLE IF EXISTS transactions")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tx_hash TEXT PRIMARY KEY,
        user_id TEXT,
        amount_usd REAL,
        timestamp TEXT
    )
    """)

    test_data = [
        # 1. NORMÁL FELHASZNÁLÓ (Szórványos tranzakciók)
        ("0x1a2b3c", "USER_NORMAL_1", 900.0, "2026-06-29 11:00:00"),
        ("0x2b3c4d", "USER_NORMAL_1", 950.0, "2026-06-29 11:30:00"),
        
        # 2. AZ ÚJ NAGYPÁLYÁS CSALÓ (USER_WHALE_X)
        # 11 darab utalást indít el összesen 15 percen belül, mindet a limit alatt!
        ("0xhash_1", "USER_WHALE_X", 990.0, "2026-06-29 12:00:00"),
        ("0xhash_2", "USER_WHALE_X", 985.0, "2026-06-29 12:01:00"),
        ("0xhash_3", "USER_WHALE_X", 992.0, "2026-06-29 12:02:00"),
        ("0xhash_4", "USER_WHALE_X", 980.0, "2026-06-29 12:03:00"),
        ("0xhash_5", "USER_WHALE_X", 975.0, "2026-06-29 12:05:00"),
        ("0xhash_6", "USER_WHALE_X", 991.0, "2026-06-29 12:06:00"),
        ("0xhash_7", "USER_WHALE_X", 965.0, "2026-06-29 12:08:00"),
        ("0xhash_8", "USER_WHALE_X", 988.0, "2026-06-29 12:10:00"),
        ("0xhash_9", "USER_WHALE_X", 970.0, "2026-06-29 12:12:00"),
        ("0xhash_10", "USER_WHALE_X", 994.0, "2026-06-29 12:13:00"),
        ("0xhash_11", "USER_WHALE_X", 982.0, "2026-06-29 12:15:00"),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO transactions (tx_hash, user_id, amount_usd, timestamp)
    VALUES (?, ?, ?, ?)
    """, test_data)

    conn.commit()
    conn.close()
    print("✅ Adatbázis sikeresen frissítve az új nagypályás mintákkal!")

if __name__ == "__main__":
    create_and_populate_db()
