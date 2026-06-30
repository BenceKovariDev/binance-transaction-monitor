# Binance On-Chain Transaction Monitor & Compliance Simulation

An automated backend utility designed to monitor smart contract interactions on the BNB Smart Chain (BSC), filter suspicious activities, detect high-risk malicious actors, and trigger automated compliance enforcement mechanisms.

## 🚀 Key Features

- **Heuristic Scam Hunting (New):** Automated proactive scanning of newly deployed smart contracts to flag potential impersonation or phishing attacks (e.g., fraudulent contracts abusing brands like Binance, BUSD, USDT) using advanced keyword pattern matching.
- **On-Chain Risk Analysis:** Real-time checking of transactions against known fraudulent smart contract addresses.
- **Blacklist & Pattern Matching:** Sophisticated lookup logic verifying if interactions originate from previously flagged or blacklisted malicious wallets.
- **Automated Incident Response:** Automatically generates standardized Compliance Asset Freeze Requests (`compliance_freeze_request.json`) to simulate exchange-level account isolation, blocking deposits/withdrawals immediately upon high-risk detection.
- **Automated Test Coverage:** Complete pipeline verification implemented via `pytest` framework, ensuring strict logic enforcement across clean, medium-risk, and high-risk traffic.

## 📁 Repository Structure

- `scam_hunter.py`: Automated proactive script searching for newly deployed fraudulent contract architectures.
- `contract_monitor.py` / `monitor.py`: Core transactional scanning and filtering business logic.
- `test_monitor.py`: Automated testing architecture checking edge-cases and risk levels.
- `compliance_freeze_request.json`: Structured output representing official internal freeze and block compliance requests.
- `database.py`: SQLite relational database tracking user risk metrics and historical transactions.
- `requirements.txt`: Backend dependency environment setup file.

## 🛠️ Setup & Local Execution

To run this simulation inside an isolated Linux/Ubuntu environment (e.g., UserLAnd):

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/BenceKovariDev/binance-transaction-monitor.git](https://github.com/BenceKovariDev/binance-transaction-monitor.git)
   cd binance-transaction-monitor

## 📊 Compliance Workflow

[New Deployments] ──> [Scam Hunter] ──> Keyword/Heuristic Match?
│
└──> [YES] ──> Append to Active Blacklist
│
[On-Chain TX Log] ──> [Rule Engine] <──────────────────────────────┘
│
└──> Match Found? ──> [YES] ──> Trigger Critical Alert
└──> Generate Freeze JSON
