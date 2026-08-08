# Aegis Crest Financial - KPI & Metric Dictionary

This dictionary defines the **24 core key performance indicators (KPIs)** monitored across Financial, Customer, Risk, and Operations categories in the Aegis Crest Financial Analytics Platform.

---

## 1. FINANCIAL KPIs

| KPI Name | Category | Definition | Exact Formula | Target Benchmark | Business Importance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Active Deposits** | Financial | Total USD balance across active deposit accounts. | `SUM(accounts.current_balance WHERE status='Active')` | > $500M | Core liquidity foundation for loan funding. |
| **Active Loan Exposure** | Financial | Outstanding principal balance on active/approved loans. | `SUM(loans.principal_amount WHERE status IN ('Active', 'Approved'))` | > $200M | Main interest-earning credit asset portfolio. |
| **Defaulted Principal Loss**| Financial | Total principal balance write-off from defaulted loans. | `SUM(loans.principal_amount WHERE status='Defaulted')` | < 3.0% of portfolio | Direct loss against net operating income. |
| **Portfolio Default Rate** | Financial | Percentage of total loans issued that have defaulted. | `100.0 * Defaulted Loans / Total Loans` | < 3.5% | Key credit model health metric. |
| **Est. Interest Revenue** | Financial | Annualized interest income yield from active loans. | `SUM(loans.principal_amount * loans.interest_rate)` | > $18M / year | Top-line lending revenue driver. |
| **Avg Transaction Size** | Financial | Average dollar value per transaction. | `AVG(transactions.amount)` | $100 - $150 | Measures payment network customer engagement. |

---

## 2. CUSTOMER & ONBOARDING KPIs

| KPI Name | Category | Definition | Exact Formula | Target Benchmark | Business Importance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Customer Base** | Customer | Total unique retail banking customers. | `COUNT(customers.customer_id)` | > 20,000 | Baseline market penetration measure. |
| **FastTrack Adoption Pct** | Customer | Share of customers onboarded via digital FastTrack. | `100.0 * FastTrack Customers / Total Customers` | 20% - 30% | Digital transformation adoption rate. |
| **Average FICO Score** | Customer | Portfolio-wide weighted average credit score. | `AVG(customers.credit_score)` | > 700 | Primary indicator of customer creditworthiness. |
| **Average DTI Ratio** | Customer | Weighted average Debt-to-Income ratio. | `AVG(customers.dti_ratio)` | < 0.32 | Assesses borrower debt capacity and leverage. |
| **Product Density** | Customer | Average number of banking products held per customer. | `AVG(Accounts + Cards + Loans per Customer)` | > 2.2 | Measures relationship depth & cross-sell. |
| **High DTI Exposure Pct** | Customer | Percentage of borrowers with DTI > 40%. | `100.0 * High DTI Borrowers / Total Borrowers` | < 15% | Audits subprime lending exposure. |

---

## 3. RISK & FRAUD KPIs

| KPI Name | Category | Definition | Exact Formula | Target Benchmark | Business Importance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Confirmed Fraud Losses** | Risk | Total dollars lost to confirmed fraudulent activity. | `SUM(fraud_alerts.loss_amount WHERE status='Confirmed Fraud')` | < $500k / year | Direct financial protection metric. |
| **Transaction Fraud Rate**| Risk | Percentage of transactions flagged as fraudulent. | `100.0 * Flagged Fraud Transactions / Total Transactions` | < 1.0% | Measures payment gateway security. |
| **High Risk Alert Count** | Risk | Fraud alerts triggered with risk score >= 75. | `COUNT(fraud_alerts WHERE risk_score >= 75)` | < 500 / quarter | Prioritizes fraud investigation queues. |
| **Net Operational Loss** | Risk | Combined financial losses from defaults & fraud. | `Defaulted Principal Loss + Confirmed Fraud Loss` | < $3.0M | Overall risk appetite boundary metric. |
| **False Positive Rate** | Risk | Share of fraud alerts dismissed as non-fraud. | `100.0 * False Positive Alerts / Total Alerts` | < 35% | Prevents customer friction from false declines. |
| **Fraud Investigation Time**| Risk | Average hours to resolve a fraud alert. | `AVG(Hours to status resolution)` | < 24.0 Hours | Limits ongoing account exploitation. |

---

## 4. OPERATIONS & SERVICE KPIs

| KPI Name | Category | Definition | Exact Formula | Target Benchmark | Business Importance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Avg Approval Turnaround**| Operations | Days from loan application submission to approval. | `AVG(loans.approval_turnaround_days)` | <= 2.00 Days | Core operational SLA for lending. |
| **SLA Variance Days** | Operations | Difference between turnaround time and 2.0d target.| `Avg Approval Turnaround - 2.00` | <= 0.00 Days | Highlights underwriting latency spikes. |
| **Ticket Resolution Hours**| Operations | Hours from ticket creation to status closure. | `AVG(support_tickets.resolution_time_hours)` | <= 18.0 Hours | Customer support speed benchmark. |
| **Avg CSAT Score** | Operations | Customer satisfaction rating on closed tickets. | `AVG(support_tickets.customer_satisfaction_score)` | >= 4.20 / 5.0 | Key measure of customer sentiment. |
| **Ticket Escalation Rate** | Operations | Percentage of support tickets escalated to mgmt. | `100.0 * Escalated Tickets / Total Tickets` | < 10% | Pinpoints recurring service breakages. |
| **FastTrack SLA Breach Pct**| Operations | FastTrack loan applications exceeding 2.5d SLA. | `100.0 * FastTrack Loans > 2.5d / Total FastTrack Loans` | < 5.0% | Tracks digital workflow bottlenecking. |
