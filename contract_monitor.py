import logging

# Professzionális logolás beállítása
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# A BscScan képernyőképen szereplő valódi, jelentett csaló USDT okosszerződés (Suspicious_Token23659)
SUSPICIOUS_CONTRACT = "0xc82b74532f417cc47fb14f0894d1b216d72f8888"

# Valódi gyanús küldő címek (From), amik interakcióba léptek a csaló szerződéssel
KNOWN_SUSPICIOUS_SENDERS = [
    "0x8D4C1BC92652c7B46".lower(),
    "0xFD5eEe381401Dd1fC7".lower(),
    "0x4D494197c624A8C9a".lower()
]

def analyze_onchain_transaction(tx):
    """
    Binance Compliance (Megfelelőségi) elvárásoknak megfelelő on-chain tranzakció-elemző logika.
    Kiszűri az impersonating/scam okosszerződésekkel való interakciókat.
    """
    contract_address = tx.get("to_contract", "").lower().strip()
    sender_address = tx.get("from_address", "").lower().strip()
    tx_hash = tx.get("hash", "UNKNOWN")
    
    # Kritérium 1: A tranzakció a vizsgált csaló okosszerződésre irányul?
    if contract_address == SUSPICIOUS_CONTRACT.lower():
        
        # Kritérium 2: A küldő címe szerepel a korábban azonosított gyanús címek listáján?
        for suspicious_sender in KNOWN_SUSPICIOUS_SENDERS:
            # Részleges egyezést is nézünk, ha a cím le van vágva a felületen (...)
            if suspicious_sender in sender_address or sender_address in suspicious_sender:
                logging.warning(f"[ALERT - CRITICAL RISK] Blacklisted/Suspicious sender {sender_address} interacted with scam contract!")
                return {"status": "ALERT_HIGH", "reason": "Known malicious actor interacting with scam contract", "tx_hash": tx_hash}
        
        # Ha nem ismert gyanús cím, de a csaló szerződéssel interaktál (Medium Risk)
        logging.info(f"[ALERT - MEDIUM RISK] General user interaction detected on impersonating contract from {sender_address}")
        return {"status": "ALERT_MEDIUM", "reason": "Interaction with flagged impersonating contract", "tx_hash": tx_hash}
        
    # Teljesen tiszta, más szerződésre irányuló tranzakció
    return {"status": "CLEAN", "reason": "No suspicious on-chain activity detected", "tx_hash": tx_hash}

if __name__ == "__main__":
    print("\n--- Running On-Chain Smart Contract Monitor Simulation ---")
    # Teszteljük le egy valós adattal a képről (3 órával ezelőtti tranzakció a listádról)
    sample_tx = {
        "hash": "0x942aa69db7...",
        "from_address": "0x8D4C1BC92652c7B46",
        "to_contract": "0xc82b74532f417cc47fb14f0894d1b216d72f8888"
    }
    result = analyze_onchain_transaction(sample_tx)
    print(f"Analysis Output: {result}\n")
