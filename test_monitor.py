from contract_monitor import analyze_onchain_transaction, SUSPICIOUS_CONTRACT

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
        "to_contract": "0x2170ed0880ac9a755fd29b2688956bd959f933f8" # Legit ETH/BSC cím példa
    }
    analysis = analyze_onchain_transaction(safe_tx)
    assert analysis["status"] == "CLEAN"
