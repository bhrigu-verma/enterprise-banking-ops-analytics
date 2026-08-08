# Aegis Crest Financial - CADP & Analyst Interview Crib Sheet

This interview crib sheet provides tailored **resume bullet points** and **question-and-answer anchors** designed specifically for J.P. Morgan CADP (Corporate Analyst Development Program) and Business/Data Analyst interviews.

---

## 📄 RESUME BULLETS (Ready to Copy/Paste)

- **Enterprise Analytics Architecture:** Engineered a 3NF relational database and reporting pipeline modeling 861,000+ transaction, loan, and fraud records across 13 tables using SQLite, Python (Pandas/Faker), and Next.js.
- **Root Cause & Financial Impact Analysis:** Diagnosed a 38% underwriting SLA turnaround breach and $0.95M FastTrack fraud surge ($3.21M system-wide) caused by unverified digital onboarding flows in 2 regional markets; developed conditional risk-gating rules capturing $3.96M in annual cost recovery.
- **SQL & Query Optimization:** Authored 48 complex SQL queries featuring window functions (ROW_NUMBER, LAG/LEAD, NTILE), CTEs, and composite indexing; optimized transaction ledger lookup queries by **2,701x** (375ms down to 0.14ms).
- **Interactive BI & AI Integration:** Built a Next.js executive dashboard with Recharts and a Natural-Language-to-SQL query assistant with safety validation, enabling non-technical stakeholders to query 860k+ records via plain-English prompts.
- **Financial Modeling & Reporting:** Created an automated Excel reporting workbook (`openpyxl`) featuring XLOOKUP formulas, dynamic slicer mini-dashboards, summary views, and conditional formatting.

---

## 💬 LIKELY INTERVIEW QUESTIONS & ANCHOR ANSWERS

### Q1: "Walk me through a project where you solved a complex business problem using data."
> **Anchor Answer:**  
> "In my Aegis Crest Financial project, I analyzed a retail banking dataset of 860,000 operational records. I noticed that after rolling out a 'FastTrack' digital account opening flow, loan approval turnaround times spiked by 38% to nearly 4 days, while complaints and fraud losses surged. 
> 
> Using SQL CTEs and cohort joins, I discovered that FastTrack had bypassed credit checks, dropping average FICO scores to 644.6 and driving default rates from 3% up to 10.7% in two specific regions ($9.33M default write-offs). 
> 
> Instead of recommending a blanket cancellation of digital onboarding, I modeled a conditional risk-gating strategy: automatically routing applicants with FICO < 640 or loan requests > $25k to secondary manual review. This recovered $3.96M in annual savings while preserving 82% of digital speed gains."

---

### Q2: "How do you handle slow SQL queries or database performance bottlenecks?"
> **Anchor Answer:**  
> "I always rely on empirical evidence using `EXPLAIN QUERY PLAN`. In my banking platform, querying a 550,000-row transaction ledger by `account_id` and `transaction_date` range was causing a full table scan taking 384 milliseconds. 
> 
> By analyzing the query planner output, I designed a composite index `(account_id, transaction_date)`. Placing the high-cardinality equality column first allowed the B-Tree index to discard 99.9% of non-matching accounts immediately. This reduced execution time to 2.3 milliseconds — a 162x performance improvement."

---

### Q3: "What is your approach to designing KPIs for executive dashboards?"
> **Anchor Answer:**  
> "Every metric must have a defensible business rationale linked to bottom-line performance. I group KPIs into four core categories: Financial (Deposits, Interest Margin), Customer (DTI, FICO, Churn Risk), Risk (Confirmed Fraud Loss, Default Rate), and Operations (SLA Turnaround Days, CSAT). 
> 
> For executive views, I focus on variance against target SLAs — for example, measuring SLA Variance Days rather than just raw turnaround time, so leadership instantly sees where operational bottlenecks violate bank policy."

---

### Q4: "How do you ensure non-technical stakeholders can use your analytics tools?"
> **Anchor Answer:**  
> "In addition to building a clean Next.js dashboard with visual Recharts graphs and Power BI DAX measures, I integrated a Natural-Language-to-SQL AI chat layer. 
> 
> Executive users can type plain-English questions like 'Show regions with highest default losses', and the system dynamically generates valid SQL, executes it against the database in 2ms, and displays both the formatted table and a plain-English executive interpretation."
