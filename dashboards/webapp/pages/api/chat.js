import { createClient } from '@libsql/client';

const ALLOWED_TABLES = new Set([
  'regions', 'branches', 'employees', 'products', 'customers', 'accounts',
  'cards', 'transactions', 'payments', 'loans', 'loan_payments',
  'support_tickets', 'fraud_alerts', 'v_regional_executive_kpis',
  'v_customer_360', 'v_fasttrack_risk_audit'
]);

function generateSql(p) {
  const pLower = p.toLowerCase();
  // 1. Ratio / Fraud vs Loan Volume per Region
  if ((pLower.includes('ratio') || pLower.includes('worst') || pLower.includes('percent')) && pLower.includes('fraud') && (pLower.includes('loan') || pLower.includes('volume'))) {
    return {
      sql: `
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
      `,
      explanation: "Calculated the ratio of confirmed fraud write-off losses against total loan origination volume per region."
    };
  }

  // 2. Employment Status & Average Income Breakdown
  if (pLower.includes('employment') || (pLower.includes('income') && (pLower.includes('status') || pLower.includes('breakdown') || pLower.includes('average')))) {
    return {
      sql: `
        SELECT 
            employment_status,
            COUNT(customer_id) AS customer_count,
            ROUND(AVG(annual_income), 2) AS avg_annual_income_usd,
            ROUND(AVG(credit_score), 1) AS avg_credit_score,
            ROUND(AVG(dti_ratio), 4) AS avg_dti_ratio
        FROM customers
        GROUP BY employment_status
        ORDER BY avg_annual_income_usd DESC;
      `,
      explanation: "Grouped customer base by employment status to compute average annual income, credit score, and DTI ratio."
    };
  }

  // 3. Regional Default Losses / Write-offs
  if (pLower.includes('default') && pLower.includes('region')) {
    return {
      sql: `
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
      `,
      explanation: "Aggregated loan origination volume and default losses across regions."
    };
  }

  // 4. FastTrack vs Standard Onboarding Turnaround & Credit Comparison
  if (pLower.includes('fasttrack') || pLower.includes('turnaround')) {
    return {
      sql: `
        SELECT 
            c.is_digital_fasttrack, 
            COUNT(c.customer_id) AS customers,
            ROUND(AVG(c.credit_score), 1) AS avg_fico,
            ROUND(AVG(l.approval_turnaround_days), 2) AS avg_turnaround_days,
            ROUND(100.0 * SUM(CASE WHEN l.status='Defaulted' THEN 1 ELSE 0 END)/COUNT(l.loan_id), 2) AS default_rate_pct
        FROM customers c 
        LEFT JOIN loans l ON c.customer_id = l.customer_id
        GROUP BY c.is_digital_fasttrack;
      `,
      explanation: "Compared FastTrack digital onboarding cohort vs standard onboarding profiles."
    };
  }

  // 5. Fraud Trend Over Time
  if (pLower.includes('fraud') && (pLower.includes('trend') || pLower.includes('month') || pLower.includes('time'))) {
    return {
      sql: `
        SELECT 
            STRFTIME('%Y-%m', alert_date) AS month, 
            fraud_type, 
            COUNT(alert_id) AS alerts, 
            ROUND(SUM(loss_amount), 2) AS loss_usd
        FROM fraud_alerts 
        WHERE status = 'Confirmed Fraud'
        GROUP BY month, fraud_type 
        ORDER BY month ASC, loss_usd DESC;
      `,
      explanation: "Tracked confirmed fraud alerts and financial losses over time."
    };
  }

  // 6. Merchant Fraud Concentration
  if (pLower.includes('merchant')) {
    return {
      sql: `
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
      `,
      explanation: "Identified high-velocity fraud merchant targets."
    };
  }

  // 7. Customer Support SLA & CSAT
  if (pLower.includes('support') || pLower.includes('ticket') || pLower.includes('csat') || pLower.includes('complaint')) {
    return {
      sql: `
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
      `,
      explanation: "Analyzed operational customer service ticket resolution SLA and CSAT scores."
    };
  }

  return { sql: null, explanation: null };
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query } = req.body;
  if (!query || typeof query !== 'string' || !query.trim()) {
    return res.status(400).json({ error: 'Query prompt is required' });
  }

  const { sql, explanation } = generateSql(query);

  if (!sql) {
    return res.status(400).json({
      error: `I couldn't generate a valid database query for '${query}' based on the available schema. Please try asking about regions, loans, defaults, fraud, merchants, or customer demographics.`,
      query: query,
      results: []
    });
  }

  // SAFETY LAYER VALIDATION
  let sqlClean = sql.trim();
  const upperSql = sqlClean.toUpperCase();

  // 1. Read-only SELECT/WITH check
  if (!(upperSql.startsWith("SELECT") || upperSql.startsWith("WITH"))) {
    return res.status(400).json({ error: 'Safety Violation: Only read-only SELECT queries are allowed.', query });
  }

  // 2. Table Whitelist Check
  const foundTables = [...sqlClean.matchAll(/\b(?:FROM|JOIN)\s+([a-z0-9_]+)/gi)].map(m => m[1].toLowerCase());
  const invalidTables = foundTables.filter(t => !ALLOWED_TABLES.has(t));

  if (invalidTables.length > 0) {
    return res.status(400).json({ error: `Safety Violation: Query references disallowed table(s): ${invalidTables.join(', ')}`, query });
  }

  // 3. Automatic LIMIT Enforcement
  if (!upperSql.includes("LIMIT")) {
    sqlClean = sqlClean.replace(/;$/, "") + " LIMIT 50;";
  }

  if (!process.env.TURSO_DATABASE_URL || !process.env.TURSO_AUTH_TOKEN) {
    return res.status(500).json({ error: 'Database configuration is missing (TURSO_DATABASE_URL or TURSO_AUTH_TOKEN)' });
  }

  const client = createClient({
    url: process.env.TURSO_DATABASE_URL,
    authToken: process.env.TURSO_AUTH_TOKEN,
  });

  try {
    const t0 = performance.now();
    const result = await client.execute(sqlClean);
    const t1 = performance.now();

    const formattedResults = result.rows.map(row => {
        let obj = {};
        result.columns.forEach((col, idx) => {
            obj[col] = row[idx];
        });
        return obj;
    });

    const out = {
      query: query,
      generated_sql: sqlClean,
      execution_time_ms: Number((t1 - t0).toFixed(2)),
      explanation: explanation,
      columns: result.columns,
      results: formattedResults
    };

    res.status(200).json(out);
  } catch (error) {
    console.error("Database execution error:", error);
    res.status(500).json({
      error: `Database execution error: ${error.message}`,
      query: query,
      generated_sql: sqlClean
    });
  }
}
