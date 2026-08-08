#!/usr/bin/env python3
"""
Aegis Crest Financial - Synthetic Data Generator
Generates ~800,000 rows across 13 tables with realistic banking skew,
correlations, and an embedded business problem in FastTrack digital onboarding regions (Regions 2 & 5).
"""

import os
import sqlite3
import random
import math
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

# Set seeds for deterministic generation
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "aegis_banking.db"))
SCHEMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql"))

def init_db(conn):
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()

def generate_data():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode = MEMORY;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA foreign_keys = OFF;")
    
    print("1. Initializing schema...")
    init_db(conn)
    
    cursor = conn.cursor()
    
    # ---------------------------------------------------------
    # 1. REGIONS (5 regions)
    # ---------------------------------------------------------
    print("2. Generating Regions...")
    regions_data = [
        (1, "Northeast Corridor", "REG-NE", "Eleanor Vance", 2.0, 0),
        (2, "Southeast Hub", "REG-SE", "Marcus Thorne", 2.0, 1),       # FastTrack Spike Region
        (3, "Midwest Central", "REG-MWC", "Sarah Jenkins", 2.0, 0),
        (4, "West Coast Metro", "REG-WC", "David Sterling", 2.0, 0),
        (5, "Midwest West", "REG-MWW", "Patricia Morales", 2.0, 1)    # FastTrack Spike Region
    ]
    cursor.executemany("""
        INSERT INTO regions (region_id, region_name, code, regional_director, target_sla_days, digital_fasttrack_enabled)
        VALUES (?, ?, ?, ?, ?, ?)
    """, regions_data)
    
    # ---------------------------------------------------------
    # 2. BRANCHES (25 branches, 5 per region)
    # ---------------------------------------------------------
    print("3. Generating Branches...")
    branches_data = []
    cities_by_region = {
        1: [("New York", "NY", "10001"), ("Boston", "MA", "02108"), ("Philadelphia", "PA", "19102"), ("Stamford", "CT", "06901"), ("Jersey City", "NJ", "07302")],
        2: [("Atlanta", "GA", "30301"), ("Charlotte", "NC", "28202"), ("Miami", "FL", "33101"), ("Tampa", "FL", "33602"), ("Nashville", "TN", "37201")],
        3: [("Chicago", "IL", "60601"), ("Columbus", "OH", "43215"), ("Indianapolis", "IN", "46204"), ("Detroit", "MI", "48226"), ("Milwaukee", "WI", "53202")],
        4: [("San Francisco", "CA", "94102"), ("Seattle", "WA", "98101"), ("Los Angeles", "CA", "90012"), ("San Diego", "CA", "92101"), ("Phoenix", "AZ", "85001")],
        5: [("Denver", "CO", "80202"), ("Minneapolis", "MN", "55401"), ("Kansas City", "MO", "64106"), ("Omaha", "NE", "68102"), ("Salt Lake City", "UT", "84101")]
    }
    
    branch_id_counter = 1
    for r_id in range(1, 6):
        for idx, (city, state, zip_code) in enumerate(cities_by_region[r_id]):
            b_name = f"Aegis {city} Main Branch" if idx == 0 else f"Aegis {city} {fake.street_name()} Branch"
            b_code = f"BR-{r_id}{idx+1:02d}"
            staff = random.randint(12, 35)
            branches_data.append((branch_id_counter, r_id, b_name, b_code, city, state, zip_code, staff))
            branch_id_counter += 1
            
    cursor.executemany("""
        INSERT INTO branches (branch_id, region_id, branch_name, code, city, state, zip_code, total_staff)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, branches_data)
    
    # ---------------------------------------------------------
    # 3. EMPLOYEES (150 employees, 6 per branch)
    # ---------------------------------------------------------
    print("4. Generating Employees...")
    employees_data = []
    emp_id_counter = 1
    roles = [("Branch Manager", "Operations", 115000), ("Assistant Manager", "Operations", 85000), 
             ("Senior Loan Officer", "Lending", 92000), ("Loan Specialist", "Lending", 68000),
             ("Fraud Analyst", "Risk", 78000), ("Customer Service Lead", "Service", 62000)]
    
    for b_id in range(1, 26):
        for role, dept, base_sal in roles:
            fn = fake.first_name()
            ln = fake.last_name()
            email = f"{fn.lower()}.{ln.lower()}{emp_id_counter}@aegiscrest.com"
            hire_d = fake.date_between(start_date='-6y', end_date='-1y').strftime('%Y-%m-%d')
            sal = float(base_sal + random.randint(-5000, 10000))
            employees_data.append((emp_id_counter, b_id, fn, ln, email, role, dept, hire_d, sal, 1))
            emp_id_counter += 1
            
    cursor.executemany("""
        INSERT INTO employees (employee_id, branch_id, first_name, last_name, email, role, department, hire_date, salary, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees_data)
    
    # ---------------------------------------------------------
    # 4. PRODUCTS (15 products)
    # ---------------------------------------------------------
    print("5. Generating Products...")
    products_data = [
        (1, "Aegis Essential Checking", "Deposit", "Checking", 0.0005, 0.00, 580),
        (2, "Aegis Premier Yield Checking", "Deposit", "Checking", 0.0150, 12.00, 680),
        (3, "High-Yield Reserve Savings", "Deposit", "Savings", 0.0425, 0.00, 620),
        (4, "Platinum Freedom Credit Card", "Card", "Credit Platinum", 0.1899, 0.00, 660),
        (5, "Signature Rewards Credit Card", "Card", "Credit Signature", 0.2299, 95.00, 700),
        (6, "Infinite Wealth Elite Card", "Card", "Credit Infinite", 0.2499, 495.00, 750),
        (7, "Standard Auto Financing", "Consumer Loan", "Auto", 0.0649, 0.00, 620),
        (8, "Unsecured Personal Term Loan", "Consumer Loan", "Personal", 0.1099, 0.00, 640),
        (9, "FastTrack Express Personal Loan", "Consumer Loan", "Personal", 0.1499, 0.00, 580), # Higher risk product
        (10, "Home Equity Line of Credit (HELOC)", "Consumer Loan", "Home Equity", 0.0799, 50.00, 710),
        (11, "30-Year Fixed Mortgage", "Mortgage", "Mortgage 30Y", 0.0685, 0.00, 680),
        (12, "15-Year Fixed Mortgage", "Mortgage", "Mortgage 15Y", 0.0615, 0.00, 700),
        (13, "Small Business Working Capital", "Commercial", "Business Line", 0.0950, 150.00, 670),
        (14, "Commercial Real Estate Loan", "Commercial", "CRE", 0.0750, 500.00, 720),
        (15, "Student Advantage Checking", "Deposit", "Checking", 0.0010, 0.00, 300)
    ]
    cursor.executemany("""
        INSERT INTO products (product_id, product_name, category, subcategory, interest_rate, annual_fee, credit_score_min)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, products_data)
    
    # ---------------------------------------------------------
    # 5. CUSTOMERS (25,000 customers)
    # ---------------------------------------------------------
    print("6. Generating 25,000 Customers...")
    customers_data = []
    start_date_base = datetime(2024, 1, 1)
    
    for c_id in range(1, 25001):
        # Assign region: 20% per region
        r_id = (c_id % 5) + 1
        fn = fake.first_name()
        ln = fake.last_name()
        email = f"{fn.lower()}.{ln.lower()}{c_id}@example.com"
        phone = fake.phone_number()[:15]
        addr = fake.street_address()
        city_tuple = cities_by_region[r_id][(c_id % 5)]
        city, state, zip_code = city_tuple[0], city_tuple[1], city_tuple[2]
        dob = fake.date_of_birth(minimum_age=18, maximum_age=75).strftime('%Y-%m-%d')
        
        # Onboarding date over 2 years (2024-2025)
        days_offset = random.randint(0, 720)
        onboard_dt = start_date_base + timedelta(days=days_offset)
        onboard_str = onboard_dt.strftime('%Y-%m-%d')
        
        # Embedded Business Problem: FastTrack Digital Onboarding rollout in Regions 2 & 5 starting July 2024 (days_offset >= 182)
        is_fasttrack_period = (onboard_dt >= datetime(2024, 7, 1) and onboard_dt <= datetime(2024, 12, 31))
        is_spike_region = (r_id in [2, 5])
        
        if is_spike_region and is_fasttrack_period and random.random() < 0.55:
            # FastTrack digital cohort: Lower credit scores, higher DTI, lower income
            channel = 'Web Digital'
            is_fasttrack = 1
            credit_score = int(np.random.normal(615, 45))
            credit_score = max(350, min(820, credit_score))
            dti = round(float(np.random.beta(3, 4) * 0.55 + 0.20), 4) # higher DTI ~0.45
            dti = min(0.95, max(0.10, dti))
            income = round(float(np.random.lognormal(10.6, 0.4)), 2) # median ~$40k
            emp_status = random.choice(['Employed', 'Self-Employed', 'Student', 'Unemployed'])
        else:
            channel = random.choices(['In-Branch', 'Web Digital', 'Mobile App', 'Partner'], weights=[0.40, 0.30, 0.25, 0.05])[0]
            is_fasttrack = 1 if (channel in ['Web Digital', 'Mobile App'] and random.random() < 0.15) else 0
            credit_score = int(np.random.normal(705, 55))
            credit_score = max(400, min(850, credit_score))
            dti = round(float(np.random.beta(2, 5) * 0.40 + 0.10), 4) # avg ~0.25
            income = round(float(np.random.lognormal(11.1, 0.5)), 2) # median ~$66k
            emp_status = random.choices(['Employed', 'Self-Employed', 'Retired', 'Student'], weights=[0.75, 0.12, 0.08, 0.05])[0]
            
        customers_data.append((
            c_id, r_id, fn, ln, email, phone, addr, city, state, zip_code,
            dob, credit_score, dti, income, emp_status, onboard_str, channel, is_fasttrack
        ))
        
    cursor.executemany("""
        INSERT INTO customers (
            customer_id, region_id, first_name, last_name, email, phone, address, city, state, zip_code,
            date_of_birth, credit_score, dti_ratio, annual_income, employment_status, onboard_date, onboarding_channel, is_digital_fasttrack
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers_data)
    
    # ---------------------------------------------------------
    # 6. ACCOUNTS (35,000 accounts)
    # ---------------------------------------------------------
    print("7. Generating 35,000 Accounts...")
    accounts_data = []
    acc_id_counter = 1
    
    for c in customers_data:
        c_id, r_id, _, _, _, _, _, _, _, _, _, _, _, income, _, onboard_str, channel, is_fasttrack = c
        # Each region has 5 branches (e.g. region 1 -> branch 1..5)
        branch_id = (r_id - 1) * 5 + random.randint(1, 5)
        
        # Primary deposit account
        acc_num_1 = f"ACC-{c_id:06d}-1"
        acc_type_1 = 'Checking' if random.random() < 0.70 else 'Savings'
        bal_1 = round(float(np.random.lognormal(8.0, 1.2)), 2) if is_fasttrack == 0 else round(float(np.random.lognormal(6.5, 1.0)), 2)
        accounts_data.append((acc_id_counter, c_id, branch_id, acc_num_1, acc_type_1, 'Active', onboard_str, bal_1, 'USD'))
        acc_id_counter += 1
        
        # Secondary account for 40% of customers
        if random.random() < 0.40:
            acc_num_2 = f"ACC-{c_id:06d}-2"
            acc_type_2 = 'Savings' if acc_type_1 == 'Checking' else 'Credit Card Account'
            bal_2 = round(float(np.random.lognormal(7.5, 1.1)), 2)
            accounts_data.append((acc_id_counter, c_id, branch_id, acc_num_2, acc_type_2, 'Active', onboard_str, bal_2, 'USD'))
            acc_id_counter += 1

    cursor.executemany("""
        INSERT INTO accounts (account_id, customer_id, branch_id, account_number, account_type, status, open_date, current_balance, currency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, accounts_data)
    
    # ---------------------------------------------------------
    # 7. CARDS (28,000 cards)
    # ---------------------------------------------------------
    print("8. Generating 28,000 Cards...")
    cards_data = []
    card_id_counter = 1
    
    for acc in accounts_data:
        acc_id, c_id, b_id, acc_num, acc_type, status, open_date, bal, _ = acc
        if acc_type in ['Checking', 'Credit Card Account']:
            prod_id = random.choice([1, 4, 5]) if acc_type == 'Checking' else random.choice([4, 5, 6])
            card_num = f"4532-{card_id_counter:04d}-****-{random.randint(1000, 9999)}"
            c_type = 'Debit' if acc_type == 'Checking' else 'Credit Signature'
            limit = 0.00 if c_type == 'Debit' else float(random.choice([2500, 5000, 10000, 15000, 25000]))
            cards_data.append((card_id_counter, acc_id, prod_id, card_num, c_type, open_date, limit, round(bal * 0.3, 2), 'Active', 1))
            card_id_counter += 1

    cursor.executemany("""
        INSERT INTO cards (card_id, account_id, product_id, card_number_masked, card_type, issue_date, credit_limit, current_balance, card_status, is_contactless)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cards_data)
    
    # ---------------------------------------------------------
    # 8. TRANSACTIONS (~550,000 transactions)
    # ---------------------------------------------------------
    print("9. Generating ~550,000 Transactions...")
    transactions_data = []
    tx_id_counter = 1
    
    channels = ['Online Banking', 'Mobile App', 'POS Terminal', 'ATM', 'Branch Counter']
    merchant_cats = ['Grocery Stores', 'Gas Stations', 'Online Retail', 'Restaurants & Dining', 'Travel & Airlines', 'Electronics', 'Utilities']
    merchant_names = ['Amazon.com', 'Walmart', 'Target', 'Shell Gas', 'Starbucks', 'Uber', 'Apple Store', 'Netflix', 'Home Depot']
    cities = ['New York', 'Atlanta', 'Chicago', 'San Francisco', 'Denver', 'Miami', 'Seattle', 'Dallas', 'Boston']
    
    # Map accounts for quick lookup
    accounts_list = accounts_data
    num_accounts = len(accounts_list)
    
    for i in range(550000):
        acc = accounts_list[i % num_accounts]
        acc_id = acc[0]
        c_id = acc[1]
        c_info = customers_data[c_id - 1]
        is_fasttrack = c_info[17]
        r_id = c_info[1]
        
        # Transaction date in 2024-2025
        dt_base = datetime(2024, 1, 1) + timedelta(minutes=random.randint(0, 1051200))
        dt_str = dt_base.strftime('%Y-%m-%d %H:%M:%S')
        
        # Amount: log-normal distribution
        amt = round(float(np.random.lognormal(3.8, 1.1)), 2) # median ~$45, mean ~$120
        amt = max(1.50, min(8500.00, amt))
        
        tx_type = random.choices(
            ['POS Purchase', 'Direct Deposit', 'ATM Withdrawal', 'ACH Outbound', 'Wire Transfer'],
            weights=[0.50, 0.25, 0.12, 0.10, 0.03]
        )[0]
        
        ch = random.choice(channels)
        m_cat = random.choice(merchant_cats) if tx_type == 'POS Purchase' else None
        m_name = random.choice(merchant_names) if tx_type == 'POS Purchase' else None
        city = random.choice(cities)
        
        # Fraud probability spike in FastTrack cohort Q3-Q4 2024
        is_fasttrack_period = (dt_base >= datetime(2024, 7, 1) and dt_base <= datetime(2024, 12, 31))
        if is_fasttrack == 1 and (r_id in [2, 5]) and is_fasttrack_period:
            fraud_prob = 0.045 # Elevated fraud rate ~4.5%
        else:
            fraud_prob = 0.008 # Baseline fraud rate ~0.8%
            
        is_fraud = 1 if (random.random() < fraud_prob) else 0
        resp_code = '00' if is_fraud == 0 else random.choice(['51', '61', '91', '96'])
        
        card_id = random.randint(1, len(cards_data)) if tx_type == 'POS Purchase' else None
        
        transactions_data.append((
            tx_id_counter, acc_id, card_id, dt_str, amt, tx_type, ch, m_cat, m_name, city, is_fraud, resp_code
        ))
        tx_id_counter += 1
        
        if len(transactions_data) >= 50000:
            cursor.executemany("""
                INSERT INTO transactions (
                    transaction_id, account_id, card_id, transaction_date, amount, transaction_type, channel, merchant_category, merchant_name, location_city, is_flagged_fraud, response_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, transactions_data)
            transactions_data = []

    if transactions_data:
        cursor.executemany("""
            INSERT INTO transactions (
                transaction_id, account_id, card_id, transaction_date, amount, transaction_type, channel, merchant_category, merchant_name, location_city, is_flagged_fraud, response_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, transactions_data)
        
    # ---------------------------------------------------------
    # 9. PAYMENTS (~90,000 payments)
    # ---------------------------------------------------------
    print("10. Generating ~90,000 Payments...")
    payments_data = []
    pay_id_counter = 1
    
    for i in range(90000):
        acc = accounts_list[i % num_accounts]
        acc_id = acc[0]
        dt_base = datetime(2024, 1, 1) + timedelta(minutes=random.randint(0, 1051200))
        dt_str = dt_base.strftime('%Y-%m-%d %H:%M:%S')
        amt = round(float(np.random.lognormal(5.2, 0.9)), 2) # mean ~$250
        amt = max(10.00, min(12000.00, amt))
        method = random.choice(['Auto-Debit', 'Bill Pay', 'Wire', 'Check', 'Card Payment'])
        status = random.choices(['Completed', 'Pending', 'Failed'], weights=[0.94, 0.04, 0.02])[0]
        fee = 0.00 if method in ['Auto-Debit', 'Bill Pay'] else 15.00
        
        payments_data.append((pay_id_counter, acc_id, dt_str, amt, method, status, fee, random.randint(10, 120)))
        pay_id_counter += 1
        
        if len(payments_data) >= 30000:
            cursor.executemany("""
                INSERT INTO payments (payment_id, account_id, payment_date, amount, payment_method, status, processing_fee, clearing_time_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, payments_data)
            payments_data = []

    if payments_data:
        cursor.executemany("""
            INSERT INTO payments (payment_id, account_id, payment_date, amount, payment_method, status, processing_fee, clearing_time_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, payments_data)

    # Build customer to accounts mapping for accurate FK references
    cust_to_accounts = {}
    for acc in accounts_data:
        acc_id, c_id = acc[0], acc[1]
        if c_id not in cust_to_accounts:
            cust_to_accounts[c_id] = []
        cust_to_accounts[c_id].append(acc_id)

    # ---------------------------------------------------------
    # 10. LOANS (~15,000 loans)
    # ---------------------------------------------------------
    print("11. Generating 15,000 Loans...")
    loans_data = []
    loan_id_counter = 1
    
    for i in range(15000):
        c = customers_data[i % len(customers_data)]
        c_id, r_id, _, _, _, _, _, _, _, _, _, credit_score, dti, income, _, onboard_str, _, is_fasttrack = c
        acc_id = cust_to_accounts[c_id][0]
        
        l_type = random.choices(
            ['Personal Loan', 'Auto Loan', 'Home Equity', 'Mortgage', 'Small Business Loan'],
            weights=[0.35, 0.30, 0.15, 0.12, 0.08]
        )[0]
        
        prod_id = 9 if (l_type == 'Personal Loan' and is_fasttrack == 1) else (8 if l_type == 'Personal Loan' else 7)
        principal = round(float(np.random.lognormal(9.6, 0.8)), 2) # median ~$15k
        principal = max(2500.00, min(250000.00, principal))
        rate = round(0.05 + (850 - credit_score) * 0.0003, 4)
        term = random.choice([12, 24, 36, 48, 60, 120])
        
        start_dt = datetime.strptime(onboard_str, '%Y-%m-%d') + timedelta(days=random.randint(5, 60))
        start_str = start_dt.strftime('%Y-%m-%d')
        
        is_fasttrack_period = (start_dt >= datetime(2024, 7, 1) and start_dt <= datetime(2024, 12, 31))
        
        # Embedded Business Metric: Turnaround Time and Default Rate Spike
        if is_fasttrack == 1 and (r_id in [2, 5]) and is_fasttrack_period:
            turnaround = round(float(np.random.normal(3.85, 0.65)), 2)
            turnaround = max(1.50, min(7.50, turnaround))
            status_weights = [0.05, 0.05, 0.65, 0.10, 0.09, 0.06] # Approved, Active, Defaulted, Paid Off, Submitted, Rejected
            loan_status = random.choices(['Approved', 'Active', 'Defaulted', 'Paid Off', 'Submitted', 'Rejected'], weights=status_weights)[0]
            risk_score = random.randint(65, 95)
            is_fasttrack_app = 1
        else:
            turnaround = round(float(np.random.normal(2.25, 0.35)), 2)
            turnaround = max(0.80, min(4.20, turnaround))
            status_weights = [0.10, 0.68, 0.03, 0.14, 0.02, 0.03] # Defaulted ~3.0%
            loan_status = random.choices(['Approved', 'Active', 'Defaulted', 'Paid Off', 'Submitted', 'Rejected'], weights=status_weights)[0]
            risk_score = random.randint(15, 55)
            is_fasttrack_app = 0
            
        loans_data.append((
            loan_id_counter, c_id, acc_id, prod_id, r_id, l_type, principal, rate, term,
            start_str, loan_status, turnaround, risk_score, is_fasttrack_app
        ))
        loan_id_counter += 1

    cursor.executemany("""
        INSERT INTO loans (
            loan_id, customer_id, account_id, product_id, region_id, loan_type, principal_amount, interest_rate, term_months, start_date, status, approval_turnaround_days, initial_risk_score, is_fasttrack_approval
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, loans_data)
    
    # ---------------------------------------------------------
    # 11. LOAN_PAYMENTS (~60,000 loan payments)
    # ---------------------------------------------------------
    print("12. Generating ~60,000 Loan Payments...")
    loan_payments_data = []
    lp_id_counter = 1
    
    for l in loans_data:
        l_id, c_id, acc_id, prod_id, r_id, l_type, principal, rate, term, start_str, status, turnaround, risk_score, is_ft = l
        num_payments = random.randint(3, 12) if status in ['Active', 'Defaulted', 'Paid Off'] else 0
        monthly_pmt = round((principal * (1 + rate * (term / 12.0))) / term, 2)
        
        start_dt = datetime.strptime(start_str, '%Y-%m-%d')
        for p_idx in range(num_payments):
            pmt_dt = (start_dt + timedelta(days=30 * (p_idx + 1))).strftime('%Y-%m-%d')
            interest_comp = round(monthly_pmt * 0.35, 2)
            principal_comp = round(monthly_pmt - interest_comp, 2)
            
            if status == 'Defaulted' and p_idx >= (num_payments - 2):
                p_status = random.choice(['Late 60', 'Late 90+', 'Missed'])
                days_over = random.choice([45, 75, 110])
            else:
                p_status = 'On-Time'
                days_over = 0
                
            loan_payments_data.append((
                lp_id_counter, l_id, pmt_dt, monthly_pmt, principal_comp, interest_comp, p_status, days_over
            ))
            lp_id_counter += 1

    cursor.executemany("""
        INSERT INTO loan_payments (
            loan_payment_id, loan_id, payment_date, amount_paid, principal_component, interest_component, payment_status, days_overdue
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, loan_payments_data)
    
    # ---------------------------------------------------------
    # 12. SUPPORT_TICKETS (~22,000 support tickets)
    # ---------------------------------------------------------
    print("13. Generating ~22,000 Support Tickets...")
    tickets_data = []
    ticket_id_counter = 1
    
    for i in range(22000):
        c = customers_data[i % len(customers_data)]
        c_id, r_id, _, _, _, _, _, _, _, _, _, _, _, _, _, onboard_str, _, is_ft = c
        branch_id = (r_id - 1) * 5 + random.randint(1, 5)
        acc_id = random.choice(cust_to_accounts[c_id])
        
        t_dt = datetime(2024, 1, 1) + timedelta(minutes=random.randint(0, 1051200))
        t_str = t_dt.strftime('%Y-%m-%d %H:%M:%S')
        is_fasttrack_period = (t_dt >= datetime(2024, 7, 1) and t_dt <= datetime(2024, 12, 31))
        
        if is_ft == 1 and (r_id in [2, 5]) and is_fasttrack_period:
            cat = random.choices(['Loan Delay', 'Fraud Dispute', 'Digital App Issue', 'Fee Inquiry'], weights=[0.42, 0.30, 0.20, 0.08])[0]
            prio = random.choices(['High', 'Critical', 'Medium'], weights=[0.45, 0.35, 0.20])[0]
            res_hours = round(float(np.random.normal(38.0, 12.0)), 2)
            csat = random.choices([1, 2, 3, 4], weights=[0.45, 0.30, 0.15, 0.10])[0]
            escalation = 1 if prio in ['High', 'Critical'] and random.random() < 0.65 else 0
        else:
            cat = random.choice(['Loan Delay', 'Fraud Dispute', 'Digital App Issue', 'Fee Inquiry', 'Account Access', 'Card Decline'])
            prio = random.choices(['Low', 'Medium', 'High'], weights=[0.50, 0.35, 0.15])[0]
            res_hours = round(float(np.random.normal(14.0, 4.0)), 2)
            csat = random.choices([3, 4, 5], weights=[0.15, 0.45, 0.40])[0]
            escalation = 1 if prio == 'High' and random.random() < 0.10 else 0
            
        tickets_data.append((
            ticket_id_counter, c_id, acc_id, branch_id, t_str, cat, prio, 'Closed', res_hours, csat, escalation
        ))
        ticket_id_counter += 1

    cursor.executemany("""
        INSERT INTO support_tickets (
            ticket_id, customer_id, account_id, branch_id, ticket_date, category, priority, status, resolution_time_hours, customer_satisfaction_score, escalation_flag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tickets_data)
    
    # ---------------------------------------------------------
    # 13. FRAUD_ALERTS (~8,500 fraud alerts)
    # ---------------------------------------------------------
    print("14. Generating ~8,500 Fraud Alerts...")
    fraud_data = []
    alert_id_counter = 1
    
    for i in range(8500):
        c = customers_data[i % len(customers_data)]
        c_id, r_id, _, _, _, _, _, _, _, _, _, _, _, _, _, onboard_str, _, is_ft = c
        acc_id = random.choice(cust_to_accounts[c_id])
        
        a_dt = datetime(2024, 1, 1) + timedelta(minutes=random.randint(0, 1051200))
        a_str = a_dt.strftime('%Y-%m-%d %H:%M:%S')
        is_fasttrack_period = (a_dt >= datetime(2024, 7, 1) and a_dt <= datetime(2024, 12, 31))
        
        if is_ft == 1 and (r_id in [2, 5]) and is_fasttrack_period:
            f_type = random.choices(['Identity Theft', 'Card Not Present', 'Synthetic ID', 'Account Takeover'], weights=[0.40, 0.35, 0.15, 0.10])[0]
            risk_score = random.randint(75, 99)
            loss_amt = round(float(np.random.lognormal(7.8, 1.0)), 2)
            status = 'Confirmed Fraud'
        else:
            f_type = random.choice(['Identity Theft', 'Card Not Present', 'Account Takeover', 'Synthetic ID', 'Wire Fraud', 'Velocity Spike'])
            risk_score = random.randint(45, 80)
            loss_amt = round(float(np.random.lognormal(6.2, 0.8)), 2)
            status = random.choices(['Confirmed Fraud', 'False Positive', 'Dismissed'], weights=[0.45, 0.40, 0.15])[0]
            
        emp_id = random.randint(1, 150)
        tx_id = random.randint(1, 550000)
        
        fraud_data.append((
            alert_id_counter, acc_id, tx_id, a_str, f_type, risk_score, status, loss_amt, emp_id
        ))
        alert_id_counter += 1

    cursor.executemany("""
        INSERT INTO fraud_alerts (
            alert_id, account_id, transaction_id, alert_date, fraud_type, risk_score, status, loss_amount, investigated_by_emp_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, fraud_data)
    
    conn.commit()
    print("Database committed successfully.")
    
    # Run total count audit
    print("\n--- DATABASE RECORD COUNT AUDIT ---")
    tables = ['regions', 'branches', 'employees', 'products', 'customers', 'accounts', 'cards', 'transactions', 'payments', 'loans', 'loan_payments', 'support_tickets', 'fraud_alerts']
    total_rows = 0
    for t in tables:
        cnt = cursor.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        total_rows += cnt
        print(f"Table {t:20s}: {cnt:>10,d} rows")
    print(f"TOTAL SYSTEM ROWS      : {total_rows:>10,d} rows\n")
    
    conn.close()

if __name__ == '__main__':
    generate_data()
