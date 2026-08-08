import { exec } from 'child_process';
import path from 'path';

export default function handler(req, res) {
  const dbPath = path.resolve(process.cwd(), '../../aegis_banking.db');
  
  const pyScript = `
import sqlite3, json

conn = sqlite3.connect('${dbPath}')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 1. Executive KPIs
exec_kpis = cursor.execute('''
    SELECT 
        (SELECT SUM(current_balance) FROM accounts WHERE status='Active') as total_deposits,
        (SELECT SUM(principal_amount) FROM loans WHERE status IN ('Active', 'Approved')) as active_loans,
        (SELECT SUM(principal_amount) FROM loans WHERE status='Defaulted') as defaulted_loans,
        (SELECT SUM(loss_amount) FROM fraud_alerts WHERE status='Confirmed Fraud') as fraud_loss,
        (SELECT AVG(approval_turnaround_days) FROM loans) as avg_turnaround,
        (SELECT AVG(resolution_time_hours) FROM support_tickets) as avg_res_hours,
        (SELECT AVG(customer_satisfaction_score) FROM support_tickets) as avg_csat
''').fetchone()

# 2. Regional Breakdown
regional = cursor.execute('''
    SELECT 
        r.region_name,
        r.digital_fasttrack_enabled,
        COUNT(DISTINCT c.customer_id) as customers,
        ROUND(AVG(l.approval_turnaround_days), 2) as avg_turnaround,
        SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) as defaults,
        ROUND(100.0 * SUM(CASE WHEN l.status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) as default_rate_pct,
        COALESCE(ROUND(SUM(fa.loss_amount), 2), 0) as fraud_loss_usd
    FROM regions r
    LEFT JOIN customers c ON r.region_id = c.region_id
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN fraud_alerts fa ON a.account_id = fa.account_id AND fa.status = 'Confirmed Fraud'
    GROUP BY r.region_name, r.digital_fasttrack_enabled
''').fetchall()

# 3. Monthly Fraud Trajectory
fraud_trend = cursor.execute('''
    SELECT 
        STRFTIME('%Y-%m', alert_date) as month,
        ROUND(SUM(loss_amount), 2) as loss_usd,
        COUNT(alert_id) as alert_count
    FROM fraud_alerts
    WHERE status = 'Confirmed Fraud'
    GROUP BY month
    ORDER BY month ASC
''').fetchall()

# 4. Turnaround Comparison Pre vs Post FastTrack
turnaround_trend = cursor.execute('''
    SELECT 
        r.region_name,
        c.is_digital_fasttrack,
        ROUND(AVG(l.approval_turnaround_days), 2) as avg_turnaround,
        COUNT(l.loan_id) as loan_count
    FROM loans l
    JOIN customers c ON l.customer_id = c.customer_id
    JOIN regions r ON l.region_id = r.region_id
    GROUP BY r.region_name, c.is_digital_fasttrack
''').fetchall()

out = {
    'exec': dict(exec_kpis),
    'regional': [dict(r) for r in regional],
    'fraud_trend': [dict(f) for f in fraud_trend],
    'turnaround_trend': [dict(t) for t in turnaround_trend]
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
      res.status(200).json(data);
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse database output' });
    }
  });
}
