# 🗄️ SQL Analytics

This folder contains the SQL scripts developed for the **Banking Fraud & Financial Risk Intelligence Platform**.

The SQL layer is used to perform analytical exploration, transaction analysis, customer analysis, bank-level analysis, network analysis and to prepare queries used by the Power BI dashboards.

---

## 📁 SQL Scripts

| Script | Description |
|---|---|
| `01_basic_data_exploration.sql` | Performs initial exploration of the analytical dataset and examines transaction-level data, distributions and key fields. |
| `02_transaction_analysis.sql` | Analyzes transaction volumes, transaction values, payment methods, currencies and suspicious transaction activity. |
| `03_customer_analysis.sql` | Analyzes customer-level transaction behavior, activity and transaction value patterns. |
| `04_bank_analysis.sql` | Evaluates bank-level transaction performance, transaction values, laundering activity and risk indicators. |
| `05_network_analysis.sql` | Analyzes transaction relationships and connectivity between accounts and entities within the financial transaction network. |
| `06_dashboard_queries.sql` | Contains analytical queries used to support KPIs, tables and visualizations across the Power BI dashboards. |

---

## 🔄 SQL Analytics Workflow

```text
MySQL Database
      │
      ▼
01. Basic Data Exploration
      │
      ▼
02. Transaction Analysis
      │
      ▼
03. Customer Analysis
      │
      ▼
04. Bank Analysis
      │
      ▼
05. Network Analysis
      │
      ▼
06. Dashboard Queries
      │
      ▼
Power BI Dashboards
