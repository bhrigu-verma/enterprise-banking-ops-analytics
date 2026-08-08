import { exec } from 'child_process';
import path from 'path';

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query } = req.body;
  if (!query || typeof query !== 'string' || !query.trim()) {
    return res.status(400).json({ error: 'Query prompt is required' });
  }

  const dbPath = path.resolve(process.cwd(), '../../aegis_banking.db');

  const pyScript = `
import sqlite3, json, time, re

raw_prompt = """${query.replace(/"/g, '\\"')}"""
prompt_lower = raw_prompt.lower()

# Known Schema Tables & Views Whitelist
ALLOWED_TABLES = {
    'regions', 'branches', 'employees', 'products', 'customers', 'accounts',
    'cards', 'transactions', 'payments', 'loans', 'loan_payments',
    'support_tickets', 'fraud_alerts', 'v_regional_executive_kpis',
    'v_customer_360', 'v_fasttrack_risk_audit'
}

def generate_sql(p):
    # Dynamic Natural-Language-to-SQL Pattern Engine
    # 1. Ratio / Fraud vs Loan Volume per Region
    if ('ratio' in p or 'worst' in p or 'percent' in p) and 'fraud' in p and ('loan' in p or 'volume' in p):
        return """
        SELECT 
            r.region_name,
            ROUND(SUM(fa.loss_amount), 2) AS total_fraud_loss_usd,
            ROUND(SUM(l.principal_amount), 2) AS total_loan_volume_usd,
            ROUND(100.0 * SUM(fa.loss_amount) / NULLIF(SUM(l.principal_amount), 0), 4) AS fraud_to_loan_ratio_pct
        FROM regions r
        LEFT JOIN customers c ON r.region_id = c.region_id
        LEFT JOIN loans l ON c.customer_id = l.customer_id
        LEFT JOIN accounts a ON c.customer_id = a.customer_id
        LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
        GROUP BY r.region_name
        ORDER BY fraud_to_loan_ratio_pct DESC;
        """, "Calculated the ratio of confirmed fraud write-off losses against total loan origination volume per region."

    # 2. Employment Status & Average Income Breakdown
    if 'employment' in p or ('income' in p and ('status' in p or 'breakdown' in p or 'average' in p)):
        return """
        SELECT 
            employment_status,
            COUNT(customer_id) AS customer_count,
            ROUND(AVG(annual_income), 2) AS avg_annual_income_usd,
            ROUND(AVG(credit_score), 1) AS avg_credit_score,
            ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio
        FROM customers
        GROUP BY employment_status
        ORDER BY avg_annual_income_usd DESC;
        """, "Grouped customer base by employment status to compute average annual income, credit score, and DTI ratio."

    # 3. Regional Default Losses / Write-offs
    if 'default' in p and 'region' in p:
        return """
        SELECT 
            r.region_name, 
            COUNT(l.loan_id) AS total_loans, 
            SUM(CASE WHEN l.status='Defaulted' THEN 1 ELSE 0 END) AS defaulted_loans,
            ROUND(100.0 * SUM(CASE WHEN l.status='Defaulted' THEN 1 ELSE 0 END)/COUNT(l.loan_id), 2) AS default_rate_pct,
            ROUND(SUM(CASE WHEN l.status='Defaulted' THEN l.principal_amount ELSE 0 END), 2) AS default_loss_usd
        FROM regions r 
        JOIN loans l ON r.region_id = l.region_id
        GROUP BY r.region_name 
        ORDER BY default_loss_usd DESC;
        """, "Aggregated loan origination volume and default losses across regions."

    # 4. FastTrack vs Standard Onboarding Turnaround & Credit Comparison
    if 'fasttrack' in p or 'turnaround' in p:
        return """
        SELECT 
            c.is_digital_fasttrack, 
            COUNT(c.customer_id) AS customers,
            ROUND(AVG(c.credit_score), 1) AS avg_fico,
            ROUND(AVG(l.approval_turnaround_days), 2) AS avg_turnaround_days,
            ROUND(100.0 * SUM(CASE WHEN l.status='Defaulted' THEN 1 ELSE 0 END)/COUNT(l.loan_id), 2) AS default_rate_pct
        FROM customers c 
        LEFT JOIN loans l ON c.customer_id = l.customer_id
        GROUP BY c.is_digital_fasttrack;
        """, "Compared FastTrack digital onboarding cohort vs standard onboarding profiles."

    # 5. Fraud Trend Over Time
    if 'fraud' in p and ('trend' in p or 'month' in p or 'time' in p):
        return """
        SELECT 
            STRFTIME('%Y-%m', alert_date) AS month, 
            fraud_type, 
            COUNT(alert_id) AS alerts, 
            ROUND(SUM(loss_amount), 2) AS loss_usd
        FROM fraud_alerts 
        WHERE status = 'Confirmed Fraud'
        GROUP BY month, fraud_type 
        ORDER BY month ASC, loss_usd DESC;
        """, "Tracked confirmed fraud alerts and financial losses over time."

    # 6. Merchant Fraud Concentration
    if 'merchant' in p:
        return """
        SELECT 
            merchant_name, 
            merchant_category, 
            COUNT(transaction_id) AS tx_count,
            SUM(is_flagged_fraud) AS fraud_txs,
            ROUND(100.0 * SUM(is_flagged_fraud) / COUNT(transaction_id), 2) AS fraud_rate_pct,
            ROUND(SUM(amount), 2) AS total_volume_usd
        FROM transactions 
        WHERE merchant_name IS NOT NULL
        GROUP BY merchant_name, merchant_category 
        HAVING fraud_txs >= 3
        ORDER BY fraud_rate_pct DESC 
        LIMIT 10;
        """, "Identified high-velocity fraud merchant targets."

    # 7. Customer Support SLA & CSAT
    if 'support' in p or 'ticket' in p or 'csat' in p or 'complaint' in p:
        return """
        SELECT 
            category, 
            priority, 
            COUNT(ticket_id) AS tickets,
            ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hrs,
            ROUND(AVG(customer_satisfaction_score), 2) AS avg_csat,
            SUM(escalation_flag) AS escalations
        FROM support_tickets
        GROUP BY category, priority 
        ORDER BY tickets DESC 
        LIMIT 10;
        """, "Analyzed operational customer service ticket resolution SLA and CSAT scores."

    # Honest failure return if prompt intent cannot be safely mapped
    return None, None

sql, explanation = generate_sql(prompt_lower)

if not sql:
    out = {
        'error': f"I couldn't generate a valid database query for '{raw_prompt}' based on the available schema. Please try asking about regions, loans, defaults, fraud, merchants, or customer demographics.",
        'query': raw_prompt,
        'results': []
    }
    print(json.dumps(out))
    exit(0)

# SAFETY LAYER VALIDATION
sql_clean = sql.strip()
upper_sql = sql_clean.upper()

# 1. Read-only SELECT/WITH check
if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
    out = {'error': 'Safety Violation: Only read-only SELECT queries are allowed.', 'query': raw_prompt}
    print(json.dumps(out))
    exit(0)

# 2. Table Whitelist Check
found_tables = re.findall(r'\\bFROM\\s+([a-z0-9_]+)|\\bJOIN\\s+([a-z0-9_]+)', sql_clean, re.IGNORECASE)
referenced_tables = {t for tup in found_tables for t in tup if t}
invalid_tables = referenced_tables - ALLOWED_TABLES

if invalid_tables:
    out = {'error': f"Safety Violation: Query references disallowed table(s): {list(invalid_tables)}", 'query': raw_prompt}
    print(json.dumps(out))
    exit(0)

# 3. Automatic LIMIT Enforcement
if "LIMIT" not in upper_sql:
    sql_clean = sql_clean.rstrip(";") + " LIMIT 50;"

# EXECUTION
try:
    t0 = time.perf_counter()
    conn = sqlite3.connect('${dbPath}')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute(sql_clean).fetchall()
    t1 = time.perf_counter()

    out = {
        'query': raw_prompt,
        'generated_sql': sql_clean,
        'execution_time_ms': round((t1 - t0) * 1000, 2),
        'explanation': explanation,
        'columns': [col[0] for col in cursor.description] if cursor.description else [],
        'results': [dict(r) for r in rows]
    }
    print(json.dumps(out))
except Exception as e:
    out = {
        'error': f"Database execution error: {str(e)}",
        'query': raw_prompt,
        'generated_sql': sql_clean
    }
    print(json.dumps(out))
`;

  exec(`python3 -c "${pyScript.replace(/"/g, '\\"')}"`, (err, stdout, stderr) => {
    if (err) {
      console.error(stderr);
      return res.status(500).json({ error: stderr || err.message });
    }
    try {
      const data = JSON.parse(stdout);
      if (data.error) {
        return res.status(400).json(data);
      }
      res.status(200).json(data);
    } catch (e) {
      res.status(500).json({ error: 'Failed to execute query engine' });
    }
  });
}
