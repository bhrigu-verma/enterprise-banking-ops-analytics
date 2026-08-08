import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { 
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, PieChart, Pie, Cell 
} from 'recharts';
import { 
  BuildingBank, ShieldAlert, Users, TrendingUp, Clock, FileText, Search, MessageSquare, Terminal, RefreshCw, CheckCircle2, AlertTriangle 
} from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('executive');
  
  // NL-to-SQL Chat state
  const [chatQuery, setChatQuery] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [chatResult, setChatResult] = useState(null);

  useEffect(() => {
    fetch('/api/kpis')
      .then(res => res.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if (!chatQuery.trim()) return;
    setChatLoading(true);
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: chatQuery })
    })
      .then(res => res.json())
      .then(resData => {
        setChatResult(resData);
        setChatLoading(false);
      })
      .catch(() => setChatLoading(false));
  };

  const sampleQueries = [
    "Show regions with highest loan default write-offs",
    "What is FastTrack turnaround time vs standard onboarding?",
    "Show monthly fraud loss trend over time",
    "Find high-risk merchants with fraud concentration"
  ];

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-[#0B132B] text-white flex flex-col items-center justify-center space-y-4">
        <RefreshCw className="w-10 h-10 animate-spin text-[#D4AF37]" />
        <h2 className="text-xl font-semibold tracking-wide">Loading Aegis Crest Financial Analytics...</h2>
      </div>
    );
  }

  const k = data.exec || {};
  const COLORS = ['#D4AF37', '#3A506B', '#E63946', '#457B9D', '#2A9D8F'];

  return (
    <div className="min-h-screen bg-[#0B132B] text-slate-100 font-sans">
      <Head>
        <title>Aegis Crest Financial - Enterprise Banking Analytics</title>
        <meta name="description" content="CADP Portfolio Grade Banking Operations Analytics Platform" />
      </Head>

      {/* HEADER */}
      <header className="border-b border-slate-800 bg-[#1C2541] px-8 py-5 flex items-center justify-between shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-[#D4AF37] text-navy-900 rounded-lg font-bold shadow-md">
            ACF
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              Aegis Crest Financial 
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-[#D4AF37]/20 text-[#D4AF37] border border-[#D4AF37]/30">
                Enterprise Ops v2.4
              </span>
            </h1>
            <p className="text-xs text-slate-400">Corporate Banking Operations & Risk Intelligence Engine</p>
          </div>
        </div>

        {/* TOP METRICS STRIP */}
        <div className="hidden md:flex items-center space-x-8 text-sm">
          <div>
            <span className="text-xs text-slate-400 block">Total Active Deposits</span>
            <span className="text-base font-bold text-[#D4AF37]">
              ${((k.total_deposits || 0) / 1e6).toFixed(1)}M
            </span>
          </div>
          <div className="h-8 w-px bg-slate-700" />
          <div>
            <span className="text-xs text-slate-400 block">Active Loan Exposure</span>
            <span className="text-base font-bold text-slate-200">
              ${((k.active_loans || 0) / 1e6).toFixed(1)}M
            </span>
          </div>
          <div className="h-8 w-px bg-slate-700" />
          <div>
            <span className="text-xs text-slate-400 block">Confirmed Fraud Loss</span>
            <span className="text-base font-bold text-rose-400">
              ${((k.fraud_loss || 0) / 1e6).toFixed(2)}M
            </span>
          </div>
        </div>
      </header>

      {/* MAIN LAYOUT */}
      <div className="p-8 max-w-7xl mx-auto space-y-8">

        {/* NAVIGATION TABS & NL-TO-SQL LAUNCHER */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <nav className="flex space-x-2">
            {[
              { id: 'executive', label: 'Executive Scorecard' },
              { id: 'operations', label: 'Operations & SLA Latency' },
              { id: 'customers', label: 'Customer 360 & Onboarding' },
              { id: 'risk', label: 'Risk & Fraud Intelligence' },
              { id: 'nl2sql', label: 'AI Natural-Language-to-SQL' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-[#D4AF37] text-slate-900 font-bold shadow-md'
                    : 'bg-[#1C2541] text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          <div className="text-xs text-slate-400 flex items-center gap-1.5">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Live SQLite Database Connection: 861,206 records
          </div>
        </div>

        {/* TAB 1: EXECUTIVE SCORECARD */}
        {activeTab === 'executive' && (
          <div className="space-y-8">
            {/* KPI CARDS */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Avg Loan Turnaround</span>
                  <Clock className="w-5 h-5 text-[#D4AF37]" />
                </div>
                <div className="mt-3">
                  <span className="text-3xl font-extrabold text-white">{(k.avg_turnaround || 0).toFixed(2)} days</span>
                  <span className="text-xs text-amber-400 block mt-1">+38% vs Q2 Baseline (2.25d target)</span>
                </div>
              </div>

              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Defaulted Loans</span>
                  <AlertTriangle className="w-5 h-5 text-rose-400" />
                </div>
                <div className="mt-3">
                  <span className="text-3xl font-extrabold text-rose-400">${((k.defaulted_loans || 0) / 1e6).toFixed(2)}M</span>
                  <span className="text-xs text-rose-400 block mt-1">Concentrated in FastTrack Regions</span>
                </div>
              </div>

              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Avg CSAT Rating</span>
                  <TrendingUp className="w-5 h-5 text-emerald-400" />
                </div>
                <div className="mt-3">
                  <span className="text-3xl font-extrabold text-white">{(k.avg_csat || 0).toFixed(2)} / 5.0</span>
                  <span className="text-xs text-slate-400 block mt-1">Target: &ge; 4.20</span>
                </div>
              </div>

              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Fraud Write-off Loss</span>
                  <ShieldAlert className="w-5 h-5 text-amber-400" />
                </div>
                <div className="mt-3">
                  <span className="text-3xl font-extrabold text-amber-300">${((k.fraud_loss || 0) / 1e6).toFixed(2)}M</span>
                  <span className="text-xs text-amber-400 block mt-1">+19% Q3-Q4 Growth</span>
                </div>
              </div>
            </div>

            {/* CHARTS ROW */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-4">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  Regional Loan Default Rates (%)
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.regional || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="region_name" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                      <YAxis stroke="#94a3b8" unit="%" />
                      <Tooltip contentStyle={{ backgroundColor: '#0B132B', borderColor: '#334155', borderRadius: '8px' }} />
                      <Bar dataKey="default_rate_pct" name="Default Rate (%)" fill="#E63946" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-4">
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  Confirmed Fraud Loss Trajectory ($ USD)
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.fraud_trend || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="month" stroke="#94a3b8" />
                      <YAxis stroke="#94a3b8" />
                      <Tooltip contentStyle={{ backgroundColor: '#0B132B', borderColor: '#334155', borderRadius: '8px' }} />
                      <Line type="monotone" dataKey="loss_usd" name="Fraud Loss ($)" stroke="#D4AF37" strokeWidth={3} dot={{ r: 4 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: OPERATIONS & SLA LATENCY */}
        {activeTab === 'operations' && (
          <div className="space-y-8">
            <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-6">
              <h3 className="text-lg font-bold text-white">Underwriting SLA Turnaround Latency Breakdown</h3>
              <p className="text-sm text-slate-300">
                Following the Q3 rollout of the digital FastTrack onboarding flow in Regions 2 & 5, approval turnaround times surged from 2.25 days to 3.85 days due to underwriting verification backlogs.
              </p>
              
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data.regional || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="region_name" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" unit=" days" />
                    <Tooltip contentStyle={{ backgroundColor: '#0B132B', borderColor: '#334155', borderRadius: '8px' }} />
                    <Bar dataKey="avg_turnaround" name="Avg Turnaround (Days)" fill="#D4AF37" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: CUSTOMER 360 & ONBOARDING */}
        {activeTab === 'customers' && (
          <div className="space-y-8">
            <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-6">
              <h3 className="text-lg font-bold text-white">Customer Acquisition & FastTrack Risk Segmenting</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-4 bg-[#0B132B] rounded-lg border border-slate-800">
                  <h4 className="text-sm font-semibold text-[#D4AF37] mb-2">FastTrack Digital Cohort</h4>
                  <ul className="text-xs space-y-2 text-slate-300">
                    <li>• Average FICO Score: <strong>644.6</strong> (vs 705 Baseline)</li>
                    <li>• Average DTI Ratio: <strong>45.0%</strong> (vs 25.0% Baseline)</li>
                    <li>• Loan Default Rate: <strong>8.9%</strong> (+5.9% Spike)</li>
                  </ul>
                </div>
                <div className="p-4 bg-[#0B132B] rounded-lg border border-slate-800">
                  <h4 className="text-sm font-semibold text-emerald-400 mb-2">Standard Onboarding Cohort</h4>
                  <ul className="text-xs space-y-2 text-slate-300">
                    <li>• Average FICO Score: <strong>705</strong></li>
                    <li>• Average DTI Ratio: <strong>25.0%</strong></li>
                    <li>• Loan Default Rate: <strong>3.0%</strong></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: RISK & FRAUD INTELLIGENCE */}
        {activeTab === 'risk' && (
          <div className="space-y-8">
            <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-6">
              <h3 className="text-lg font-bold text-white">Risk & Fraud Financial Exposure Audit</h3>
              <p className="text-sm text-slate-300">
                Card Not Present and Synthetic Identity fraud concentrated heavily in accounts onboarded via unverified digital FastTrack flows.
              </p>
            </div>
          </div>
        )}

        {/* TAB 5: NL-TO-SQL AI CHAT LAYER */}
        {activeTab === 'nl2sql' && (
          <div className="space-y-8">
            <div className="bg-[#1C2541] p-6 rounded-xl border border-slate-800 shadow-md space-y-6">
              <div className="flex items-center space-x-3">
                <Terminal className="w-6 h-6 text-[#D4AF37]" />
                <div>
                  <h3 className="text-lg font-bold text-white">Natural-Language-to-SQL Analytics Assistant</h3>
                  <p className="text-xs text-slate-400">Type any plain-English business question to execute live SQL against the 861k-row database.</p>
                </div>
              </div>

              {/* CHAT FORM */}
              <form onSubmit={handleChatSubmit} className="space-y-4">
                <div className="relative">
                  <input
                    type="text"
                    value={chatQuery}
                    onChange={(e) => setChatQuery(e.target.value)}
                    placeholder="e.g. Show regions with highest loan default write-offs..."
                    className="w-full bg-[#0B132B] border border-slate-700 rounded-xl px-5 py-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#D4AF37]"
                  />
                  <button
                    type="submit"
                    disabled={chatLoading}
                    className="absolute right-3 top-3 bg-[#D4AF37] text-slate-900 font-bold px-4 py-2 rounded-lg text-xs hover:bg-[#F4C430] transition-colors"
                  >
                    {chatLoading ? 'Executing...' : 'Run Query'}
                  </button>
                </div>
              </form>

              {/* QUICK SAMPLE PROMPTS */}
              <div className="flex flex-wrap gap-2 pt-2">
                <span className="text-xs text-slate-400 py-1">Try asking:</span>
                {sampleQueries.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => { setChatQuery(q); }}
                    className="text-xs bg-[#0B132B] hover:bg-slate-800 border border-slate-700 text-slate-300 px-3 py-1 rounded-full"
                  >
                    "{q}"
                  </button>
                ))}
              </div>

              {/* CHAT RESULT DISPLAY */}
              {chatResult && (
                <div className="mt-6 space-y-4 bg-[#0B132B] p-6 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <span className="text-xs font-mono text-[#D4AF37] flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      Executed in {chatResult.execution_time_ms} ms
                    </span>
                    <span className="text-xs text-slate-500 font-mono">SQLite 3NF Engine</span>
                  </div>

                  {/* GENERATED SQL */}
                  <div>
                    <span className="text-xs font-semibold text-slate-400 block mb-1">Generated SQL Query:</span>
                    <pre className="bg-[#1C2541] p-4 rounded-lg text-xs font-mono text-emerald-300 overflow-x-auto border border-slate-800">
                      {chatResult.generated_sql}
                    </pre>
                  </div>

                  {/* NARRATIVE EXPLANATION */}
                  <div className="p-4 bg-[#1C2541]/60 rounded-lg border border-slate-800 text-xs text-slate-300">
                    <strong className="text-white block mb-1">Business Interpretation:</strong>
                    {chatResult.explanation}
                  </div>

                  {/* RESULT TABLE */}
                  {chatResult.results && chatResult.results.length > 0 && (
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-xs border-collapse">
                        <thead>
                          <tr className="border-b border-slate-800 bg-[#1C2541] text-slate-300">
                            {chatResult.columns.map((col, idx) => (
                              <th key={idx} className="p-3 font-semibold uppercase tracking-wider">{col}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                          {chatResult.results.map((row, rIdx) => (
                            <tr key={rIdx} className="hover:bg-slate-800/30">
                              {chatResult.columns.map((col, cIdx) => (
                                <td key={cIdx} className="p-3 text-slate-200">{String(row[col])}</td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
