# 🔍 Crypto Transaction Monitoring & AML Tuning Engine

This project demonstrates a production-ready conceptual approach to **Transaction Monitoring and Anti-Money Laundering (AML) Threshold Tuning** within a cryptocurrency exchange environment. It is designed to simulate how a compliance automation system flags suspicious financial patterns.

## 🚀 Overview
The system models a relational database consisting of users (including their KYC status and risk profiles) and transaction logs. It implements a fine-tuned **Velocity Alert Engine** written in Python and SQL. The primary goal is to detect **Structuring (Smurfing)** patterns—specifically targeting users trying to bypass reporting thresholds by executing multiple small transactions in a short time window.

### ⚙️ Applied Business Logic (Tuned Thresholds)
* **Time Window:** 30 minutes
* **Transaction Velocity Limit:** Maximum 10 transactions allowed
* **Action:** Triggers a Strategic AML Alert if a user exceeds 10 transactions within 30 minutes, automatically pulling KYC parameters and Risk scores via an optimized SQL `INNER JOIN`.
* **Optimization Goal:** Thresholds were tuned up from 5tx/10min to 10tx/30min to drastically reduce False Positives caused by legitimate trading bots.

## 📂 Project Structure
* `database.py` - Refactored script that initializes the relational SQLite schema (`users` and `transactions` tables with FOREIGN KEY constraints) and populates them with realistic test scenarios.
* `monitor.py` - The core monitoring engine running the time-window velocity clustering algorithm.
* `requirements.txt` - Project dependencies (utilizes Python 3 standard library).

## 🛠️ Installation & How to Run (Ubuntu / UserLAnd)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/BenceKovariDev/binance-transaction-monitor.git](https://github.com/BenceKovariDev/binance-transaction-monitor.git)
   cd binance-transaction-monitor
