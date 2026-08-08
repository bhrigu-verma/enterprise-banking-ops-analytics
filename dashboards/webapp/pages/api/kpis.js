import { createClient } from '@libsql/client';

export default async function handler(req, res) {
  if (!process.env.TURSO_DATABASE_URL || !process.env.TURSO_AUTH_TOKEN) {
    return res.status(500).json({ error: 'Database configuration is missing (TURSO_DATABASE_URL or TURSO_AUTH_TOKEN)' });
  }

  const client = createClient({
    url: process.env.TURSO_DATABASE_URL,
    authToken: process.env.TURSO_AUTH_TOKEN,
  });

  try {
    // 1. Executive KPIs
    const execKpisResult = await client.execute(`
        SELECT 
            (SELECT SUM(current_balance) FROM accounts WHERE status='Active') as total_deposits,
            (SELECT SUM(principal_amount) FROM loans WHERE status IN ('Active', 'Approved')) as active_loans,
            (SELECT SUM(principal_amount) FROM loans WHERE status='Defaulted') as defaulted_loans,
            (SELECT SUM(loss_amount) FROM fraud_alerts WHERE status='Confirmed Fraud') as fraud_loss,
            (SELECT AVG(approval_turnaround_days) FROM loans) as avg_turnaround,
            (SELECT AVG(resolution_time_hours) FROM support_tickets) as avg_res_hours,
            (SELECT AVG(customer_satisfaction_score) FROM support_tickets) as avg_csat
    `);

    // 2. Regional Breakdown
    const regionalResult = await client.execute(`
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
    `);

    // 3. Monthly Fraud Trajectory
    const fraudTrendResult = await client.execute(`
        SELECT 
            STRFTIME('%Y-%m', alert_date) as month,
            ROUND(SUM(loss_amount), 2) as loss_usd,
            COUNT(alert_id) as alert_count
        FROM fraud_alerts
        WHERE status = 'Confirmed Fraud'
        GROUP BY month
        ORDER BY month ASC
    `);

    // 4. Turnaround Comparison Pre vs Post FastTrack
    const turnaroundTrendResult = await client.execute(`
        SELECT 
            r.region_name,
            c.is_digital_fasttrack,
            ROUND(AVG(l.approval_turnaround_days), 2) as avg_turnaround,
            COUNT(l.loan_id) as loan_count
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN regions r ON l.region_id = r.region_id
        GROUP BY r.region_name, c.is_digital_fasttrack
    `);

    // Helper to format rows to JSON objects
    const formatRows = (resultSet) => {
        return resultSet.rows.map(row => {
            let obj = {};
            resultSet.columns.forEach((col, idx) => {
                obj[col] = row[idx];
            });
            return obj;
        });
    };

    const execRow = formatRows(execKpisResult)[0];

    const out = {
        exec: execRow,
        regional: formatRows(regionalResult),
        fraud_trend: formatRows(fraudTrendResult),
        turnaround_trend: formatRows(turnaroundTrendResult)
    };

    res.status(200).json(out);
  } catch (error) {
    console.error("Database query failed:", error);
    res.status(500).json({ error: 'Failed to execute database queries' });
  }
}
