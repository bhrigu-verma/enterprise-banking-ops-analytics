-- Aegis Crest Financial - Enterprise Banking Operations Analytics Platform
-- Schema Definition (3NF Normalized, SQLite & ANSI SQL Compatible)

PRAGMA foreign_keys = ON;

-- 1. REGIONS
CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    regional_director VARCHAR(100) NOT NULL,
    target_sla_days DECIMAL(4,2) DEFAULT 2.00,
    digital_fasttrack_enabled INTEGER DEFAULT 0 CHECK (digital_fasttrack_enabled IN (0, 1))
);

-- 2. BRANCHES
CREATE TABLE IF NOT EXISTS branches (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    branch_name VARCHAR(120) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    total_staff INTEGER DEFAULT 10 CHECK (total_staff >= 1),
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE RESTRICT
);

-- 3. EMPLOYEES
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    role VARCHAR(80) NOT NULL,
    department VARCHAR(80) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(12,2) CHECK (salary > 0),
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT
);

-- 4. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL CHECK (category IN ('Deposit', 'Card', 'Consumer Loan', 'Mortgage', 'Commercial')),
    subcategory VARCHAR(50) NOT NULL,
    interest_rate DECIMAL(5,4) DEFAULT 0.0000,
    annual_fee DECIMAL(8,2) DEFAULT 0.00,
    credit_score_min INTEGER DEFAULT 600 CHECK (credit_score_min BETWEEN 300 AND 850)
);

-- 5. CUSTOMERS
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    date_of_birth DATE NOT NULL,
    credit_score INTEGER NOT NULL CHECK (credit_score BETWEEN 300 AND 850),
    dti_ratio DECIMAL(5,4) NOT NULL CHECK (dti_ratio BETWEEN 0.0000 AND 1.0000),
    annual_income DECIMAL(12,2) NOT NULL CHECK (annual_income >= 0),
    employment_status VARCHAR(50) NOT NULL CHECK (employment_status IN ('Employed', 'Self-Employed', 'Retired', 'Student', 'Unemployed')),
    onboard_date DATE NOT NULL,
    onboarding_channel VARCHAR(50) NOT NULL CHECK (onboarding_channel IN ('In-Branch', 'Web Digital', 'Mobile App', 'Partner')),
    is_digital_fasttrack INTEGER DEFAULT 0 CHECK (is_digital_fasttrack IN (0, 1)),
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE RESTRICT
);

-- 6. ACCOUNTS
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('Checking', 'Savings', 'Money Market', 'Certificate of Deposit', 'Credit Card Account')),
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')),
    open_date DATE NOT NULL,
    current_balance DECIMAL(14,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT
);

-- 7. CARDS
CREATE TABLE IF NOT EXISTS cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    card_number_masked VARCHAR(19) NOT NULL UNIQUE,
    card_type VARCHAR(30) NOT NULL CHECK (card_type IN ('Debit', 'Credit Platinum', 'Credit Signature', 'Credit Infinite')),
    issue_date DATE NOT NULL,
    credit_limit DECIMAL(12,2) DEFAULT 0.00 CHECK (credit_limit >= 0),
    current_balance DECIMAL(12,2) DEFAULT 0.00,
    card_status VARCHAR(20) DEFAULT 'Active' CHECK (card_status IN ('Active', 'Blocked', 'Expired', 'Stolen')),
    is_contactless INTEGER DEFAULT 1 CHECK (is_contactless IN (0, 1)),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);

-- 8. TRANSACTIONS
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    card_id INTEGER,
    transaction_date DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_type VARCHAR(30) NOT NULL CHECK (transaction_type IN ('ACH Outbound', 'Wire Transfer', 'POS Purchase', 'ATM Withdrawal', 'Direct Deposit', 'Internal Transfer')),
    channel VARCHAR(30) NOT NULL CHECK (channel IN ('Online Banking', 'Mobile App', 'POS Terminal', 'ATM', 'Branch Counter')),
    merchant_category VARCHAR(60),
    merchant_name VARCHAR(100),
    location_city VARCHAR(80),
    is_flagged_fraud INTEGER DEFAULT 0 CHECK (is_flagged_fraud IN (0, 1)),
    response_code VARCHAR(10) DEFAULT '00' CHECK (response_code IN ('00', '51', '61', '91', '96')),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE SET NULL
);

-- 9. PAYMENTS
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    payment_date DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
    payment_method VARCHAR(40) NOT NULL CHECK (payment_method IN ('Auto-Debit', 'Bill Pay', 'Wire', 'Check', 'Card Payment')),
    status VARCHAR(20) DEFAULT 'Completed' CHECK (status IN ('Completed', 'Pending', 'Failed', 'Reversed')),
    processing_fee DECIMAL(8,2) DEFAULT 0.00,
    clearing_time_seconds INTEGER DEFAULT 45,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- 10. LOANS
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    loan_type VARCHAR(40) NOT NULL CHECK (loan_type IN ('Personal Loan', 'Auto Loan', 'Home Equity', 'Mortgage', 'Small Business Loan')),
    principal_amount DECIMAL(14,2) NOT NULL CHECK (principal_amount > 0),
    interest_rate DECIMAL(5,4) NOT NULL CHECK (interest_rate > 0),
    term_months INTEGER NOT NULL CHECK (term_months IN (12, 24, 36, 48, 60, 120, 180, 360)),
    start_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Approved' CHECK (status IN ('Submitted', 'Under Review', 'Approved', 'Active', 'Defaulted', 'Paid Off', 'Rejected')),
    approval_turnaround_days DECIMAL(5,2) NOT NULL,
    initial_risk_score INTEGER NOT NULL CHECK (initial_risk_score BETWEEN 1 AND 100),
    is_fasttrack_approval INTEGER DEFAULT 0 CHECK (is_fasttrack_approval IN (0, 1)),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE RESTRICT
);

-- 11. LOAN_PAYMENTS
CREATE TABLE IF NOT EXISTS loan_payments (
    loan_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    amount_paid DECIMAL(12,2) NOT NULL CHECK (amount_paid > 0),
    principal_component DECIMAL(12,2) NOT NULL,
    interest_component DECIMAL(12,2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'On-Time' CHECK (payment_status IN ('On-Time', 'Grace Period', 'Late 30', 'Late 60', 'Late 90+', 'Missed')),
    days_overdue INTEGER DEFAULT 0 CHECK (days_overdue >= 0),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE
);

-- 12. SUPPORT_TICKETS
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_id INTEGER,
    branch_id INTEGER NOT NULL,
    ticket_date DATETIME NOT NULL,
    category VARCHAR(60) NOT NULL CHECK (category IN ('Loan Delay', 'Fraud Dispute', 'Digital App Issue', 'Fee Inquiry', 'Account Access', 'Card Decline')),
    priority VARCHAR(20) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),
    status VARCHAR(20) DEFAULT 'Closed' CHECK (status IN ('Open', 'In Progress', 'Escalated', 'Resolved', 'Closed')),
    resolution_time_hours DECIMAL(6,2),
    customer_satisfaction_score INTEGER CHECK (customer_satisfaction_score BETWEEN 1 AND 5),
    escalation_flag INTEGER DEFAULT 0 CHECK (escalation_flag IN (0, 1)),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE SET NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE RESTRICT
);

-- 13. FRAUD_ALERTS
CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_id INTEGER,
    alert_date DATETIME NOT NULL,
    fraud_type VARCHAR(60) NOT NULL CHECK (fraud_type IN ('Identity Theft', 'Card Not Present', 'Account Takeover', 'Synthetic ID', 'Wire Fraud', 'Velocity Spike')),
    risk_score INTEGER NOT NULL CHECK (risk_score BETWEEN 1 AND 100),
    status VARCHAR(20) DEFAULT 'Confirmed Fraud' CHECK (status IN ('Under Investigation', 'Confirmed Fraud', 'False Positive', 'Dismissed')),
    loss_amount DECIMAL(12,2) DEFAULT 0.00 CHECK (loss_amount >= 0),
    investigated_by_emp_id INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE SET NULL,
    FOREIGN KEY (investigated_by_emp_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- INDEXES FOR QUERY OPTIMIZATION & PERFORMANCE CASE STUDY
CREATE INDEX IF NOT EXISTS idx_branches_region ON branches(region_id);
CREATE INDEX IF NOT EXISTS idx_employees_branch ON employees(branch_id);
CREATE INDEX IF NOT EXISTS idx_customers_region ON customers(region_id);
CREATE INDEX IF NOT EXISTS idx_customers_fasttrack ON customers(is_digital_fasttrack, region_id);
CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_accounts_branch ON accounts(branch_id);
CREATE INDEX IF NOT EXISTS idx_cards_account ON cards(account_id);
CREATE INDEX IF NOT EXISTS idx_cards_product ON cards(product_id);

-- Highly queried composite indexes
CREATE INDEX IF NOT EXISTS idx_transactions_acc_date ON transactions(account_id, transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_fraud ON transactions(is_flagged_fraud);

CREATE INDEX IF NOT EXISTS idx_payments_acc_date ON payments(account_id, payment_date);

CREATE INDEX IF NOT EXISTS idx_loans_customer ON loans(customer_id);
CREATE INDEX IF NOT EXISTS idx_loans_reg_status ON loans(region_id, status);
CREATE INDEX IF NOT EXISTS idx_loans_fasttrack ON loans(is_fasttrack_approval, region_id);

CREATE INDEX IF NOT EXISTS idx_loan_payments_loan ON loan_payments(loan_id);
CREATE INDEX IF NOT EXISTS idx_loan_payments_status ON loan_payments(payment_status);

CREATE INDEX IF NOT EXISTS idx_tickets_cust_date ON support_tickets(customer_id, ticket_date);
CREATE INDEX IF NOT EXISTS idx_tickets_branch ON support_tickets(branch_id);
CREATE INDEX IF NOT EXISTS idx_tickets_category ON support_tickets(category);

CREATE INDEX IF NOT EXISTS idx_fraud_acc_date ON fraud_alerts(account_id, alert_date);
CREATE INDEX IF NOT EXISTS idx_fraud_status ON fraud_alerts(status);
