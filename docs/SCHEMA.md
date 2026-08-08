# Aegis Crest Financial - Data Dictionary & Database Schema

This document details the **13 relational tables** comprising the Aegis Crest Financial 3NF operational database.

---

## Table 1: `regions`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `region_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique region identifier |
| `region_name` | VARCHAR(100) | NOT NULL, UNIQUE | Geographic region name |
| `code` | VARCHAR(10) | NOT NULL, UNIQUE | Region shorthand code (e.g., REG-SE) |
| `regional_director`| VARCHAR(100) | NOT NULL | Director responsible for regional ops |
| `target_sla_days` | DECIMAL(4,2) | DEFAULT 2.00 | Targeted loan approval SLA in days |
| `digital_fasttrack_enabled`| INTEGER | CHECK (0, 1) | FastTrack rollout flag (1 for Regions 2 & 5) |

---

## Table 2: `branches`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `branch_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique branch identifier |
| `region_id` | INTEGER | FK -> `regions(region_id)` | Parent region reference |
| `branch_name` | VARCHAR(120) | NOT NULL | Retail branch title |
| `code` | VARCHAR(20) | NOT NULL, UNIQUE | Branch code |
| `city` | VARCHAR(80) | NOT NULL | City location |
| `state` | VARCHAR(2) | NOT NULL | State abbreviation |
| `zip_code` | VARCHAR(10) | NOT NULL | Postal code |
| `total_staff` | INTEGER | CHECK (total_staff >= 1) | Onsite staff headcount |

---

## Table 3: `employees`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `employee_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique staff identifier |
| `branch_id` | INTEGER | FK -> `branches(branch_id)` | Assigned branch location |
| `first_name` | VARCHAR(50) | NOT NULL | Employee first name |
| `last_name` | VARCHAR(50) | NOT NULL | Employee last name |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Corporate email address |
| `role` | VARCHAR(80) | NOT NULL | Job title (e.g. Senior Loan Officer) |
| `department` | VARCHAR(80) | NOT NULL | Operations, Lending, Risk, Service |
| `hire_date` | DATE | NOT NULL | Employment start date |
| `salary` | DECIMAL(12,2)| CHECK (salary > 0) | Annual compensation USD |
| `is_active` | INTEGER | CHECK (0, 1) | Active employment status |

---

## Table 4: `products`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique banking product ID |
| `product_name` | VARCHAR(100) | NOT NULL, UNIQUE | Commercial product name |
| `category` | VARCHAR(50) | CHECK IN Deposit, Card, Loan, Mortgage | Product umbrella category |
| `subcategory` | VARCHAR(50) | NOT NULL | Specific product tier |
| `interest_rate` | DECIMAL(5,4) | DEFAULT 0.0000 | Standard APR or yield rate |
| `annual_fee` | DECIMAL(8,2) | DEFAULT 0.00 | Product maintenance fee USD |
| `credit_score_min`| INTEGER | CHECK (300-850) | Minimum credit score threshold |

---

## Table 5: `customers`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique customer identifier |
| `region_id` | INTEGER | FK -> `regions(region_id)` | Assigned home region |
| `first_name` | VARCHAR(50) | NOT NULL | Customer first name |
| `last_name` | VARCHAR(50) | NOT NULL | Customer last name |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Email address |
| `phone` | VARCHAR(20) | NOT NULL | Phone contact |
| `address` | VARCHAR(200) | NOT NULL | Residential address |
| `city` | VARCHAR(80) | NOT NULL | Residence city |
| `state` | VARCHAR(2) | NOT NULL | Residence state |
| `zip_code` | VARCHAR(10) | NOT NULL | Zip code |
| `date_of_birth` | DATE | NOT NULL | Birth date |
| `credit_score` | INTEGER | CHECK (300-850) | FICO credit score |
| `dti_ratio` | DECIMAL(5,4) | CHECK (0.0000-1.0000) | Debt-to-income ratio |
| `annual_income` | DECIMAL(12,2)| CHECK (>= 0) | Stated annual income USD |
| `employment_status`| VARCHAR(50)| CHECK IN Employed, Self-Employed...| Employment category |
| `onboard_date` | DATE | NOT NULL | Customer acquisition date |
| `onboarding_channel`| VARCHAR(50)| CHECK IN In-Branch, Web Digital...| Primary acquisition channel |
| `is_digital_fasttrack`| INTEGER | CHECK (0, 1) | FastTrack digital cohort flag |

---

## Table 6: `accounts`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `account_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique account identifier |
| `customer_id` | INTEGER | FK -> `customers(customer_id)` | Account owner reference |
| `branch_id` | INTEGER | FK -> `branches(branch_id)` | Servicing branch location |
| `account_number`| VARCHAR(20) | NOT NULL, UNIQUE | Account number string |
| `account_type` | VARCHAR(50) | CHECK IN Checking, Savings... | Account category |
| `status` | VARCHAR(20) | CHECK IN Active, Dormant, Closed...| Account operational status |
| `open_date` | DATE | NOT NULL | Account opening date |
| `current_balance`| DECIMAL(14,2)| DEFAULT 0.00 | Ledger balance USD |
| `currency` | VARCHAR(3) | DEFAULT 'USD' | Currency code |

---

## Table 7: `cards`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `card_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique payment card ID |
| `account_id` | INTEGER | FK -> `accounts(account_id)` | Linked deposit or credit account |
| `product_id` | INTEGER | FK -> `products(product_id)` | Product tier definition |
| `card_number_masked`| VARCHAR(19)| NOT NULL, UNIQUE | Masked card number |
| `card_type` | VARCHAR(30) | CHECK IN Debit, Credit Signature...| Card tier |
| `issue_date` | DATE | NOT NULL | Card issuance date |
| `credit_limit` | DECIMAL(12,2)| DEFAULT 0.00 | Revolving credit limit |
| `current_balance`| DECIMAL(12,2)| DEFAULT 0.00 | Current card balance |
| `card_status` | VARCHAR(20) | CHECK IN Active, Blocked, Stolen...| Card status |
| `is_contactless`| INTEGER | CHECK (0, 1) | NFC contactless enabled |

---

## Table 8: `transactions`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id`| INTEGER | PRIMARY KEY AUTOINCREMENT | Unique transaction ID |
| `account_id` | INTEGER | FK -> `accounts(account_id)` | Linked account |
| `card_id` | INTEGER | FK -> `cards(card_id)` NULL | Payment card reference (if POS) |
| `transaction_date`| DATETIME | NOT NULL | Timestamp of transaction |
| `amount` | DECIMAL(12,2)| NOT NULL | Transaction dollar amount |
| `transaction_type`| VARCHAR(30)| CHECK IN POS Purchase, Direct Deposit...| Payment rail type |
| `channel` | VARCHAR(30) | CHECK IN Online, POS, ATM, Mobile...| Channel medium |
| `merchant_category`| VARCHAR(60)| NULL | Merchant MCC category |
| `merchant_name` | VARCHAR(100)| NULL | Outlet merchant name |
| `location_city` | VARCHAR(80) | NULL | Transaction city location |
| `is_flagged_fraud`| INTEGER | CHECK (0, 1) | Fraud engine risk flag |
| `response_code` | VARCHAR(10) | DEFAULT '00' | ISO 8583 response code |

---

## Table 9: `payments`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique payment ID |
| `account_id` | INTEGER | FK -> `accounts(account_id)` | Target account |
| `payment_date` | DATETIME | NOT NULL | Clearing timestamp |
| `amount` | DECIMAL(12,2)| CHECK (> 0) | Payment amount USD |
| `payment_method`| VARCHAR(40) | CHECK IN Auto-Debit, Bill Pay... | Clearing method |
| `status` | VARCHAR(20) | CHECK IN Completed, Failed... | Clearing status |
| `processing_fee`| DECIMAL(8,2) | DEFAULT 0.00 | Processing fee USD |
| `clearing_time_seconds`| INTEGER| DEFAULT 45 | Settlement speed seconds |

---

## Table 10: `loans`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `loan_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique loan ID |
| `customer_id` | INTEGER | FK -> `customers(customer_id)` | Borrower customer reference |
| `account_id` | INTEGER | FK -> `accounts(account_id)` | Servicing account |
| `product_id` | INTEGER | FK -> `products(product_id)` | Loan product |
| `region_id` | INTEGER | FK -> `regions(region_id)` | Regional origin |
| `loan_type` | VARCHAR(40) | CHECK IN Personal, Auto, Mortgage...| Category |
| `principal_amount`| DECIMAL(14,2)| CHECK (> 0) | Origination principal USD |
| `interest_rate` | DECIMAL(5,4) | CHECK (> 0) | APR interest rate |
| `term_months` | INTEGER | CHECK IN (12, 24, 36, 48, 60...) | Loan term duration |
| `start_date` | DATE | NOT NULL | Origination start date |
| `status` | VARCHAR(20) | CHECK IN Approved, Active, Defaulted...| Loan lifecycle status |
| `approval_turnaround_days`| DECIMAL(5,2)| NOT NULL | Underwriting SLA turnaround days |
| `initial_risk_score`| INTEGER | CHECK (1-100) | Underwriting risk score |
| `is_fasttrack_approval`| INTEGER | CHECK (0, 1) | FastTrack approval flag |

---

## Table 11: `loan_payments`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `loan_payment_id`| INTEGER | PRIMARY KEY AUTOINCREMENT | Unique payment ID |
| `loan_id` | INTEGER | FK -> `loans(loan_id)` | Loan contract reference |
| `payment_date` | DATE | NOT NULL | Due date of installment |
| `amount_paid` | DECIMAL(12,2)| CHECK (> 0) | Installment amount USD |
| `principal_component`| DECIMAL(12,2)| NOT NULL | Principal reduction |
| `interest_component` | DECIMAL(12,2)| NOT NULL | Interest charge |
| `payment_status`| VARCHAR(20) | CHECK IN On-Time, Late 30, Missed...| Delinquency status |
| `days_overdue` | INTEGER | CHECK (>= 0) | Overdue delay count |

---

## Table 12: `support_tickets`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `ticket_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique ticket ID |
| `customer_id` | INTEGER | FK -> `customers(customer_id)` | Submitting customer |
| `account_id` | INTEGER | FK -> `accounts(account_id)` NULL | Associated account |
| `branch_id` | INTEGER | FK -> `branches(branch_id)` | Servicing branch |
| `ticket_date` | DATETIME | NOT NULL | Creation timestamp |
| `category` | VARCHAR(60) | CHECK IN Loan Delay, Fraud Dispute...| Issue category |
| `priority` | VARCHAR(20) | CHECK IN Low, Medium, High, Critical| Severity priority |
| `status` | VARCHAR(20) | CHECK IN Open, In Progress, Closed | Ticket status |
| `resolution_time_hours`| DECIMAL(6,2)| NULL | Resolution duration in hours |
| `customer_satisfaction_score`| INTEGER| CHECK (1-5) | CSAT rating (1 to 5) |
| `escalation_flag`| INTEGER | CHECK (0, 1) | Management escalation flag |

---

## Table 13: `fraud_alerts`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `alert_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique fraud alert ID |
| `account_id` | INTEGER | FK -> `accounts(account_id)` | Target account |
| `transaction_id`| INTEGER | FK -> `transactions(transaction_id)` NULL| Flagged transaction |
| `alert_date` | DATETIME | NOT NULL | Alert trigger timestamp |
| `fraud_type` | VARCHAR(60) | CHECK IN Identity Theft, CNP... | Fraud attack pattern |
| `risk_score` | INTEGER | CHECK (1-100) | Fraud engine risk score |
| `status` | VARCHAR(20) | CHECK IN Confirmed Fraud, False Positive...| Investigation status |
| `loss_amount` | DECIMAL(12,2)| CHECK (>= 0) | Financial write-off loss USD |
| `investigated_by_emp_id`| INTEGER| FK -> `employees(employee_id)` NULL | Fraud analyst assigned |
