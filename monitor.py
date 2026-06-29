import sqlite3
from datetime import datetime, timedelta

# A te általad meghatározott szabály határértékei (Thresholds)
TIME_LIMIT_MINUTES = 10
MAX_ALLOWED_TX = 5

def run_compliance_monitor():
    # Kapcsolódunk a meglévő adatbázishoz
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    # Lekérjük az összes tranzakciót időrendi sorrendben
    cursor.execute("""
        SELECT user_id, tx_hash, amount_usd, timestamp 
        FROM transactions 
        ORDER BY user_id, timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    # Csoportosítjuk a tranzakciókat a felhasználók szerint
    user_history = {}
    for user_id, tx_hash, amount, timestamp_str in rows:
        if user_id not in user_history:
            user_history[user_id] = []
        
        # Átalakítjuk a szöveges időbélyeget Python datetime objektummá
        time_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        user_history[user_id].append({"tx_hash": tx_hash, "amount": amount, "time": time_obj})

    # Élesítjük a sebesség alapú riasztási logikádat (Velocity Check)
    alert_triggered = False
    
    for user_id, txs in user_history.items():
        for i in range(len(txs)):
            # Megnézzük, van-e legalább 5 tranzakciója a listában ettől a ponttól
            if i + MAX_ALLOWED_TX - 1 < len(txs):
                first_tx = txs[i]
                fifth_tx = txs[i + MAX_ALLOWED_TX - 1]
                
                # Időkülönbség kiszámítása
                time_diff = fifth_tx["time"] - first_tx["time"]
                
                # Ha a különbség kisebb vagy egyenlő 10 percnél -> RIASZTÁS!
                if time_diff <= timedelta(minutes=TIME_LIMIT_MINUTES):
                    print(f"🚨 STRATEGIC AML ALERT: Potential Structuring (Smurfing) Detected!")
                    print(f"👤 Account ID: {user_id}")
                    print(f"⏱️ Velocity: {MAX_ALLOWED_TX} transactions within {time_diff.seconds // 60} minutes.")
                    print(f"📌 First Tx: {first_tx['tx_hash']} | Last Tx: {fifth_tx['tx_hash']}\n")
                    alert_triggered = True
                    break # Egy felhasználónál elég egy riasztás egyszerre

    if not alert_triggered:
        print("✅ No structuring patterns found. Platform status: CLEAN.")

if __name__ == "__main__":
    print("🔍 Starting Transaction Monitoring Engine...")
    run_compliance_monitor()
