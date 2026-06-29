import sqlite3

def create_and_populate_db():
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    # TÁBLÁK ÚJRAALAPOZÁSA (Töröljük a régieket a friss struktúráért)
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # 1. USERS TÁBLA (Felhasználó ID, KYC státusz, Kockázati szint)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        kyc_status TEXT,
        risk_score TEXT
    )
    """)

    # 2. TRANSACTIONS TÁBLA
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tx_hash TEXT PRIMARY KEY,
        user_id TEXT,
        amount_usd REAL,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # FELHASZNÁLÓI MINTA ADATOK
    user_data = [
        ("USER_NORMAL_1", "VERIFIED", "LOW"),
        ("USER_WHALE_X", "UNVERIFIED", "HIGH")  # Ő a mi névtelen, magas kockázatú bálnánk!
    ]

    # TRANSAKCIÓS MINTA ADATOK (A te 10 utalásos szabályodhoz)
    tx_data = [
        ("0x1a2b3c", "USER_NORMAL_1", 900.0, "2026-06-29 11:00:00"),
        ("0x2b3c4d", "USER_NORMAL_1", 950.0, "2026-06-29 11:30:00"),
        
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

    # Beszúrások végrehajtása
    cursor.executemany("INSERT INTO users (user_id, kyc_status, risk_score) VALUES (?, ?, ?)", user_data)
    cursor.executemany("INSERT INTO transactions (tx_hash, user_id, amount_usd, timestamp) VALUES (?, ?, ?, ?)", tx_data)

    conn.commit()
    conn.close()
    print("✅ Két-táblás (Users + Transactions) relációs adatbázis sikeresen felépítve!")

if __name__ == "__main__":
    create_and_populate_db()
