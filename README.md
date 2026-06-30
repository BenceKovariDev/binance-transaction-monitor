# Binance On-Chain Transaction Monitor & Compliance Simulation

An automated backend utility designed to monitor smart contract interactions on the BNB Smart Chain (BSC), filter suspicious activities, detect high-risk malicious actors, and trigger automated compliance enforcement mechanisms.

## 🚀 Key Features

- **On-Chain Risk Analysis:** Real-time checking of transactions against known fraudulent smart contract addresses (e.g., impersonating tokens/phishing architectures).
- **Blacklist & Pattern Matching:** Sophisticated lookup logic verifying if interactions originate from previously flagged or blacklisted malicious wallets.
- **Automated Incident Response:** Automatically generates standardized Compliance Asset Freeze Requests (`compliance_freeze_request.json`) to simulate exchange-level account isolation, blocking deposits/withdrawals immediately upon high-risk detection.
- **Automated Test Coverage:** Complete pipeline verification implemented via `pytest` framework, ensuring strict logic enforcement across clean, medium-risk, and high-risk traffic.

## 📁 Repository Structure

- `szerződésmonitor.py` / `monitor.py`: Core transactional scanning and filtering business logic.
- `test_monitor.py`: Automated testing architecture checking edge-cases and risk levels.
- `compliance_free_request.json`: Structured output representing official internal freeze and block compliance requests.
- `adatbázis.py`: Simulated ledger tracking registered high-risk addresses.
- `követelmények.txt`: Backend dependency environment setup file.

## 🛠️ Setup & Local Execution

To run this simulation inside an isolated Linux/Ubuntu environment (e.g., UserLAnd):

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/BenceKovariDev/binance-transaction-monitor.git](https://github.com/BenceKovariDev/binance-transaction-monitor.git)
   cd binance-transaction-monitor
