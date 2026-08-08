-- Aegis Crest Financial - Enterprise Banking Operations Analytics Platform
-- Stored Procedures & Operational Triggers (database/stored_procedures.sql)

-- 1. TRIGGER: Auto-flag High Risk Digital FastTrack Applications
-- Triggers whenever a loan application is created for a fasttrack customer with credit score < 620 or DTI > 0.45
CREATE TRIGGER IF NOT EXISTS trg_flag_fasttrack_high_risk
AFTER INSERT ON loans
FOR EACH ROW
WHEN NEW.is_fasttrack_approval = 1 AND NEW.initial_risk_score > 70
BEGIN
    INSERT INTO support_tickets (
        customer_id, account_id, branch_id, ticket_date, category, priority, status, resolution_time_hours, customer_satisfaction_score, escalation_flag
    )
    VALUES (
        NEW.customer_id,
        NEW.account_id,
        (SELECT branch_id FROM accounts WHERE account_id = NEW.account_id),
        DATETIME('now'),
        'Loan Delay',
        'High',
        'Open',
        NULL,
        NULL,
        1
    );
END;

-- 2. TRIGGER: Audit Log for High-Value Fraud Alert Loss Escalations
CREATE TRIGGER IF NOT EXISTS trg_audit_fraud_loss_escalation
AFTER INSERT ON fraud_alerts
FOR EACH ROW
WHEN NEW.loss_amount > 5000.00 AND NEW.status = 'Confirmed Fraud'
BEGIN
    UPDATE support_tickets
    SET priority = 'Critical',
        escalation_flag = 1
    WHERE account_id = NEW.account_id
      AND category = 'Fraud Dispute';
END;
