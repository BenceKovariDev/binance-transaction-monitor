import sqlite3
from datetime import datetime, timedelta

# ==============================================================================
# TUNED THRESHOLDS
# ==============================================================================
TIME_LIMIT_MINUTES = 30
MAX_ALLOWED_TX = 10
# ==============================================================================

def run_compliance_monitor():
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    # ADVANCED SQL JOIN: Összekötjük a tranzakciókat a felhasználó adataival
    cursor.execute("""
        SELECT 
            t.user_id, 
            t.tx_hash, 
            t.amount_usd, 
            t.timestamp,
            u.kyc_status,
            u.risk_score
        FROM transactions t
        INNER JOIN users u ON t.user_id = u.user_id
        ORDER BY t.user_id, t.timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    # Csoportosítás felhasználónként (kiegészítve a profil adatokkal)
    user_history = {}
    for user_id, tx_hash, amount, timestamp_str, kyc, risk in rows:
        if user_id not in user_history:
            user_history[user_id] = {
                "kyc_status": kyc,
                "risk_score": risk,
                "txs": []
            }
        
        time_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        user_history[user_id]["txs"].append({"tx_hash": tx_hash, "amount": amount, "time": time_obj})

    alert_triggered = False
    
    for user_id, profile in user_history.items():
        txs = profile["txs"]
        for i in range(len(txs)):
            if i + MAX_ALLOWED_TX - 1 < len(txs):
                first_tx = txs[i]
                fifth_tx = txs[i + MAX_ALLOWED_TX - 1]
                
                time_diff = fifth_tx["time"] - first_tx["time"]
                
                if time_diff <= timedelta(minutes=TIME_LIMIT_MINUTES):
                    print(f"🚨 STRATEGIC AML ALERT: Potential Structuring Detected!")
                    print(f"👤 Account ID: {user_id}")
                    # ITT JELENNEK MEG AZ SQL JOIN ÁLTAL LAKÉRT PROFIL ADATOK:
                    print(f"🔒 KYC Status: {profile['kyc_status']} | ⚠️ Risk Score: {profile['risk_score']}")
                    print(f"⏱️ Velocity: {MAX_ALLOWED_TX} transactions within {time_diff.seconds // 60} minutes.")
                    print(f"📌 First Tx: {first_tx['tx_hash']} | Last Tx: {fifth_tx['tx_hash']}\n")
                    alert_triggered = True
                    break

    if not alert_triggered:
        print("✅ No structuring patterns found. Platform status: CLEAN.")

if __name__ == "__main__":
    print("🔍 Starting Relational Transaction Monitoring Engine...")
    run_compliance_monitor()
