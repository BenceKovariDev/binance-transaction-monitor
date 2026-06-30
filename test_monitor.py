import os
from contract_monitor import analyze_onchain_transaction, generate_compliance_freeze_request, SUSPICIOUS_CONTRACT

def test_critical_scam_alert():
    # Szimuláljuk az egyik ismert csaló címet a BscScan listádról
    bad_tx = {
        "hash": "0x21809b1871...",
        "from_address": "0xFD5eEe381401Dd1fC7",
        "to_contract": SUSPICIOUS_CONTRACT
    }
    analysis = analyze_onchain_transaction(bad_tx)
    assert analysis["status"] == "ALERT_HIGH"
    assert "Known malicious actor" in analysis["reason"]

def test_medium_risk_alert():
    # Új, eddig ismeretlen gyanús cím lép kapcsolatba a csaló tokennel
    unknown_user_tx = {
        "hash": "0xabc123xyz...",
        "from_address": "0xNewPotentialVictimAddress",
        "to_contract": SUSPICIOUS_CONTRACT
    }
    analysis = analyze_onchain_transaction(unknown_user_tx)
    assert analysis["status"] == "ALERT_MEDIUM"

def test_clean_tx():
    # Egy teljesen legitim tranzakció egy másik, biztonságos címre
    safe_tx = {
        "hash": "0x77777777...",
        "from_address": "0xLegitTrader",
        "to_contract": "0x2170ed0880ac9a755fd29b2688956bd959f933f8"
    }
    analysis = analyze_onchain_transaction(safe_tx)
    assert analysis["status"] == "CLEAN"

def test_automated_freeze_request_generation():
    # Ellenőrizzük, hogy gyanús tranzakció esetén a zárolási kérvény sikeresen létrejön-e JSON-ben
    bad_tx = {
        "hash": "0x21809b1871...",
        "from_address": "0xFD5eEe381401Dd1fC7",
        "to_contract": SUSPICIOUS_CONTRACT
    }
    analysis = analyze_onchain_transaction(bad_tx)
    
    # Futtatjuk a zárolási funkciót
    action_result = generate_compliance_freeze_request(analysis)
    
    assert action_result["status"] == "SUCCESS"
    assert action_result["data"]["request_type"] == "EMERGENCY_ASSET_FREEZE_AND_REPORT"
    assert os.path.exists(action_result["saved_file"])
