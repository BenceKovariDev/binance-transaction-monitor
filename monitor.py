import sqlite3
from datetime import datetime, timedelta

# ==============================================================================
# TUNED THRESHOLDS (Finomhangolt határértékek a hamis pozitívok csökkentésére)
# Combined rule designed by Bence: 10 transactions within 30 minutes.
# ==============================================================================
TIME_LIMIT_MINUTES = 30  # Expanded from 10 to 30 minutes
MAX_ALLOWED_TX = 10       # Raised from 5 to 10 transactions
# ==============================================================================

def run_compliance_monitor():
    # Connect to the local SQLite database
    conn = sqlite3.connect("binance_transactions.db")
    cursor = conn.cursor()

    # Fetch all transactions ordered by user and time
    cursor.execute("""
        SELECT user_id, tx_hash, amount_usd, timestamp 
        FROM transactions 
        ORDER BY user_id, timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    # Group transactions by user_id
    user_history = {}
    for user_id, tx_hash, amount, timestamp_str in rows:
        if user_id not in user_history:
            user_history[user_id] = []
        
        # Convert string timestamp to Python datetime object
        time_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        user_history[user_id].append({"tx_hash": tx_hash, "amount": amount, "time": time_obj})

    # Execute the Velocity Alert Engine (Velocity Check)
    alert_triggered = False
    
    for user_id, txs in user_history.items():
        for i in range(len(txs)):
            # Check if there are enough subsequent transactions to evaluate the rule
            if i + MAX_ALLOWED_TX - 1 < len(txs):
                first_tx = txs[i]
                fifth_tx = txs[i + MAX_ALLOWED_TX - 1]
                
                # Calculate time difference between the first and Nth transaction
                time_diff = fifth_tx["time"] - first_tx["time"]
                
                # If velocity violates the tuned threshold -> TRIGGER AML ALERT
                if time_diff <= timedelta(minutes=TIME_LIMIT_MINUTES):
                    print(f"🚨 STRATEGIC AML ALERT: Potential Structuring (Smurfing) Detected!")
                    print(f"👤 Account ID: {user_id}")
                    print(f"⏱️ Velocity: {MAX_ALLOWED_TX} transactions within {time_diff.seconds // 60} minutes.")
                    print(f"📌 First Tx: {first_tx['tx_hash']} | Last Tx: {fifth_tx['tx_hash']}\n")
                    alert_triggered = True
                    break # One alert per user block is sufficient

    if not alert_triggered:
        print("✅ No structuring patterns found. Platform status: CLEAN.")

if __name__ == "__main__":
    print("🔍 Starting Transaction Monitoring Engine (Tuned Version)...")
    run_compliance_monitor()
