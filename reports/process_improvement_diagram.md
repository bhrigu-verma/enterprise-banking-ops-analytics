# Aegis Crest Financial - Process Improvement Workflow Diagram

## Current vs. Target Operational State Architecture

```mermaid
flowchart TD
    subgraph CURRENT_STATE ["Current Flawed State (FastTrack Rollout)"]
        A1[Customer Web/Mobile Application] --> A2{Digital FastTrack Engine}
        A2 -->|Unfiltered Bypass| A3[Instant Approval without Manual Credit/KYC]
        A3 --> A4[High Risk Applicants Admitted - Avg FICO 644.6]
        A4 --> A5[Underwriting Queue Overload - 3.85 Day SLA Breach]
        A4 --> A6[Default Write-Off Spike: 10.7% & $0.95M FastTrack Fraud Loss]
    end

    subgraph PROPOSED_REMEDIATION ["Proposed Target State (Conditional Risk Gating)"]
        B1[Customer Web/Mobile Application] --> B2{Risk-Based Automated Evaluator}
        B2 -->|FICO >= 640 & DTI <= 0.40 & Amt <= $25k| B3[Instant Automated Approval - < 0.5 Days]
        B2 -->|FICO < 640 OR DTI > 0.40 OR Amt > $25k| B4[Targeted Secondary Manual Verification]
        B4 --> B5[Underwriter Decisioning with Identity Verification]
        B5 -->|Approved| B6[High Quality Onboarding]
        B5 -->|Rejected| B7[Prevented Default/Fraud Write-off]
    end
```

## Financial Benefit Simulation Summary

| Metric | Flawed FastTrack State | Proposed Target State | Delta / Net Benefit |
| :--- | :--- | :--- | :--- |
| **Instant Approval Share** | 100% (Unfiltered) | 68% (Low Risk Cohort) | Risk-Scoped Speed |
| **Avg Approval SLA** | 3.85 Days | 1.15 Days | **-2.70 Days (-70%)** |
| **Loan Default Write-Offs** | $4.18M | $1.25M | **+$2.93M Savings** |
| **Confirmed Fraud Losses** | $1.82M | $0.79M | **+$1.03M Savings** |
| **Total Net Annual Recovery**| - | - | **+$3.96M USD** |
