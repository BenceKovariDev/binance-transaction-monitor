import logging
import json

# Professzionális logolás beállítása
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# A BscScan felületen szereplő valódi, jelentett csaló USDT okosszerződés címe (Suspicious_Token23659)
SUSPICIOUS_CONTRACT = "0xc82b74532f417cc47fb14f0894d1b216d72f8888"

# Valódi gyanús küldő címek a BscScan listádról, amelyek interakcióba léptek a csaló szerződéssel
KNOWN_SUSPICIOUS_SENDERS = [
    "0x8d4c1bc92652c7b46".lower(),
    "0xfd5eee381401dd1fc7".lower(),
    "0x4d494197c624a8c9a".lower()
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
            if suspicious_sender in sender_address or sender_address in suspicious_sender:
                logging.warning(f"[ALERT - CRITICAL RISK] Blacklisted/Suspicious sender {sender_address} interacted with scam contract!")
                return {"status": "ALERT_HIGH", "reason": "Known malicious actor interacting with scam contract", "tx_hash": tx_hash}
        
        # Ha nem ismert gyanús cím, de a csaló szerződéssel interaktál (Medium Risk)
        logging.info(f"[ALERT - MEDIUM RISK] General user interaction detected on impersonating contract from {sender_address}")
        return {"status": "ALERT_MEDIUM", "reason": "Interaction with flagged impersonating contract", "tx_hash": tx_hash}
        
    # Teljesen tiszta tranzakció
    return {"status": "CLEAN", "reason": "No suspicious on-chain activity detected", "tx_hash": tx_hash}

def generate_compliance_freeze_request(analysis_result):
    """
    Hivatalos zárolási és intézkedési kérvény (Incident Response Freeze Request) generálása.
    Ha a monitor kritikus kockázatot észlel, ez a modul automatikusan elkészíti a jelentést
    a Binance belső kockázatkezelési és jogi osztálya számára.
    """
    if analysis_result.get("status") != "ALERT_HIGH":
        return {"status": "SKIPPED", "message": "No critical risk detected. Action not required."}
    
    # A Binance Compliance formátumnak megfelelő hivatalos adatstruktúra a tőzsdei zároláshoz
    freeze_request = {
        "request_type": "EMERGENCY_ASSET_FREEZE_AND_REPORT",
        "target_contract": SUSPICIOUS_CONTRACT,
        "evidence_tx_hash": analysis_result.get("tx_hash"),
        "reason_category": "IMPERSONATION_AND_PHISHING_SCAM",
        "detailed_reason": analysis_result.get("reason"),
        "action_required": [
            "BLOCK_ALL_DEPOSITS_FROM_THIS_CONTRACT_ON_BINANCE",
            "BLOCK_ALL_WITHDRAWALS_TO_THIS_CONTRACT_ON_BINANCE",
            "SUBMIT_OFFICIAL_REPORT_TO_BSCSCAN_FOR_PUBLIC_FLAGGING"
        ],
        "investigator": "Bence Kővári (Compliance Tech Specialist)"
    }
    
    # Elmentjük a hivatalos jelentést egy JSON fájlba (szimulált adatbázis küldés)
    filename = "compliance_freeze_request.json"
    with open(filename, "w") as f:
        json.dump(freeze_request, f, indent=4)
        
    logging.critical(f"[COMPLIANCE ACTION] Official Asset Freeze Request successfully generated and saved to {filename}!")
    return {"status": "SUCCESS", "saved_file": filename, "data": freeze_request}

if __name__ == "__main__":
    print("\n--- Running On-Chain Smart Contract Monitor Simulation ---")
    # Valós, 3 órával ezelőtti csaló tranzakció adatai a BscScan képedről
    sample_tx = {
        "hash": "0x942aa69db7...",
        "from_address": "0x8D4C1BC92652c7B46",
        "to_contract": "0xc82b74532f417cc47fb14f0894d1b216d72f8888"
    }
    
    # 1. Tranzakció elemzése
    analysis = analyze_onchain_transaction(sample_tx)
    print(f"Analysis Output: {analysis}\n")
    
    # 2. Zárolási folyamat automatikus indítása a csaló ellen
    print("--- Triggering Automated Compliance Enforcement Action ---")
    action = generate_compliance_freeze_request(analysis)
    print(f"Enforcement Output Status: {action['status']}\n")
