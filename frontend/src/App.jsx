import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  ShieldX, 
  Zap, 
  Activity, 
  CreditCard, 
  Server, 
  Globe, 
  Clock, 
  RefreshCw, 
  TrendingUp,
  AlertTriangle,
  UserCheck,
  Cpu,
  Layers,
  CheckCircle2
} from 'lucide-react';
import { predictTransaction, checkApiHealth, runDriftCheck, triggerRetrain } from './api';
import './App.css';

const PRESETS = [
  {
    name: '🟢 Coffee Shop ($4.50)',
    data: {
      user_id: 'user_042',
      amount: 4.50,
      location: 'USA',
      merchant: 'grocery',
      device: 'mobile',
      time_of_day: 'morning',
      day_of_week: 'Monday'
    }
  },
  {
    name: '🟡 Electronics ($1,450)',
    data: {
      user_id: 'user_108',
      amount: 1450.00,
      location: 'Germany',
      merchant: 'electronics',
      device: 'laptop',
      time_of_day: 'evening',
      day_of_week: 'Friday'
    }
  },
  {
    name: '🔴 Midnight Crypto ($18,500)',
    data: {
      user_id: 'user_999',
      amount: 18500.00,
      location: 'Russia',
      merchant: 'crypto_exchange',
      device: 'laptop',
      time_of_day: 'midnight',
      day_of_week: 'Sunday'
    }
  },
  {
    name: '⚡ Nigeria Midnight Crypto ($250.00)',
    data: {
      user_id: 'user_101',
      amount: 250.00,
      location: 'Nigeria',
      merchant: 'crypto_exchange',
      device: 'laptop',
      time_of_day: 'midnight',
      day_of_week: 'Sunday'
    }
  }
];

export default function App() {
  const [form, setForm] = useState(PRESETS[0].data);
  const [loading, setLoading] = useState(false);
  const [currentResult, setCurrentResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [apiOnline, setApiOnline] = useState(false);

  // MLOps State
  const [driftState, setDriftState] = useState(null);
  const [driftLoading, setDriftLoading] = useState(false);
  const [retrainState, setRetrainState] = useState(null);
  const [retrainLoading, setRetrainLoading] = useState(false);

  useEffect(() => {
    // Initial health check
    checkHealth();
    // Run initial demo prediction on load
    handlePredict(PRESETS[0].data);
  }, []);

  const checkHealth = async () => {
    const health = await checkApiHealth();
    setApiOnline(health.online);
  };

  const handleInputChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const loadPreset = (presetData) => {
    setForm(presetData);
    handlePredict(presetData);
  };

  const handlePredict = async (dataToSubmit = form) => {
    setLoading(true);
    const result = await predictTransaction(dataToSubmit);
    setCurrentResult(result);
    
    // Add to history log
    const newEntry = {
      ...result,
      id: result.txn_id || Math.random().toString(36).substr(2, 9),
      merchant: dataToSubmit.merchant,
      location: dataToSubmit.location,
      time: new Date().toLocaleTimeString()
    };
    
    setHistory((prev) => [newEntry, ...prev.slice(0, 9)]);
    setLoading(false);
  };

  const handleDriftCheck = async () => {
    setDriftLoading(true);
    const res = await runDriftCheck();
    setDriftState(res);
    setDriftLoading(false);
  };

  const handleRetrain = async () => {
    setRetrainLoading(true);
    const res = await triggerRetrain();
    setRetrainState(res);
    setRetrainLoading(false);
  };

  return (
    <div className="app-container">
      {/* Navbar Header */}
      <header className="glass-panel app-header">
        <div className="brand-section">
          <div className="brand-logo">
            <ShieldCheck size={26} />
          </div>
          <div>
            <h1 className="brand-title">ShieldAI | Fraud Engine</h1>
            <p className="brand-subtitle">Real-Time Isolation Forest Anomaly Detection</p>
          </div>
        </div>

        <div className="header-status">
          <button onClick={checkHealth} className="preset-btn" title="Refresh API Status">
            <RefreshCw size={14} /> Refresh Status
          </button>
          <div className={`status-badge ${apiOnline ? 'online' : 'sim'}`}>
            <div className="dot pulse-online" style={{ backgroundColor: apiOnline ? '#10b981' : '#f59e0b' }} />
            <span>{apiOnline ? 'FastAPI Backend Online' : 'Simulation Mode'}</span>
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <main className="dashboard-grid">
        {/* Left Column: Input Form */}
        <section className="glass-panel section-card">
          <div className="card-title-row">
            <h2 className="card-title">
              <CreditCard className="accent-icon" size={20} color="#6366f1" />
              Transaction Evaluator
            </h2>
          </div>

          {/* Quick Presets */}
          <div className="input-group">
            <span className="input-label">Quick Test Scenarios</span>
            <div className="presets-container">
              {PRESETS.map((preset, idx) => (
                <button 
                  key={idx} 
                  className="preset-btn"
                  onClick={() => loadPreset(preset.data)}
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); handlePredict(); }} className="form-grid">
            <div className="input-group">
              <label className="input-label">User ID</label>
              <input 
                type="text" 
                className="custom-input"
                value={form.user_id} 
                onChange={(e) => handleInputChange('user_id', e.target.value)} 
                required 
              />
            </div>

            <div className="input-group">
              <label className="input-label">Amount ($ USD)</label>
              <input 
                type="number" 
                step="0.01"
                className="custom-input"
                value={form.amount} 
                onChange={(e) => handleInputChange('amount', e.target.value)} 
                required 
              />
            </div>

            <div className="input-group">
              <label className="input-label">Location / Country</label>
              <select 
                className="custom-select"
                value={form.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
              >
                <option value="USA">United States</option>
                <option value="UK">United Kingdom</option>
                <option value="Germany">Germany</option>
                <option value="Nigeria">Nigeria</option>
                <option value="Russia">Russia</option>
                <option value="Brazil">Brazil</option>
                <option value="Japan">Japan</option>
                <option value="UAE">United Arab Emirates</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">Merchant Category</label>
              <select 
                className="custom-select"
                value={form.merchant}
                onChange={(e) => handleInputChange('merchant', e.target.value)}
              >
                <option value="grocery">Grocery Store</option>
                <option value="electronics">Electronics Store</option>
                <option value="crypto_exchange">Crypto Exchange</option>
                <option value="casino">Online Casino</option>
                <option value="weapons">Weapons / Ammunition</option>
                <option value="luxury_watch">Luxury Watches</option>
                <option value="clothing">Clothing Store</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">Device Type</label>
              <select 
                className="custom-select"
                value={form.device}
                onChange={(e) => handleInputChange('device', e.target.value)}
              >
                <option value="mobile">Mobile App</option>
                <option value="laptop">Web Laptop</option>
                <option value="tablet">Tablet</option>
                <option value="POS_terminal">POS Terminal</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">Time of Day</label>
              <select 
                className="custom-select"
                value={form.time_of_day}
                onChange={(e) => handleInputChange('time_of_day', e.target.value)}
              >
                <option value="morning">Morning (6 AM - 12 PM)</option>
                <option value="afternoon">Afternoon (12 PM - 6 PM)</option>
                <option value="evening">Evening (6 PM - 12 AM)</option>
                <option value="midnight">Midnight (12 AM - 6 AM)</option>
              </select>
            </div>

            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? <RefreshCw className="pulse-online" size={18} /> : <Zap size={18} />}
              {loading ? 'Evaluating Model...' : 'Analyze Transaction Risk'}
            </button>
          </form>
        </section>

        {/* Right Column: Prediction Score & Risk Factors */}
        <section className="glass-panel section-card">
          <div className="card-title-row">
            <h2 className="card-title">
              <Activity className="accent-icon" size={20} color="#06b6d4" />
              Risk Analysis Result
            </h2>
            {currentResult && (
              <span className="mono" style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                Mode: {currentResult.source}
              </span>
            )}
          </div>

          {currentResult ? (
            <div className={`result-card ${currentResult.label}`}>
              <div className="result-header">
                <div className="score-main">
                  <span className={`score-number color-${currentResult.label.toLowerCase()}`}>
                    {(currentResult.fraud_score * 100).toFixed(1)}%
                  </span>
                  <span className="score-label">Anomaly Score</span>
                </div>

                <div className={`risk-badge badge-${currentResult.label}`}>
                  {currentResult.label === 'SAFE' && <ShieldCheck size={18} />}
                  {currentResult.label === 'REVIEW' && <ShieldAlert size={18} />}
                  {currentResult.label === 'FRAUD' && <ShieldX size={18} />}
                  <span>{currentResult.label}</span>
                </div>
              </div>

              {/* Score Gauge Bar */}
              <div className="gauge-container">
                <div className="gauge-bar-bg">
                  <div 
                    className={`gauge-bar-fill ${currentResult.label}`}
                    style={{ width: `${Math.min(100, Math.max(5, currentResult.fraud_score * 100))}%` }}
                  />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#9ca3af' }}>
                  <span>0.00 (Normal)</span>
                  <span>Threshold: 0.80 (Fraud)</span>
                  <span>1.00 (Critical)</span>
                </div>
              </div>

              {/* Detected Risk Factors */}
              <div className="risk-factors-list">
                <span className="input-label">Model Insights & Risk Signals</span>
                {(currentResult.risk_factors || [
                  `Fraud Prediction Decision: ${currentResult.is_fraud_predicted ? 'HIGH RISK FLAG' : 'PASSED RISK CHECKS'}`,
                  `User Baseline: ${currentResult.user_id}`,
                  `Evaluated Amount: $${currentResult.amount.toLocaleString()}`
                ]).map((factor, idx) => (
                  <div key={idx} className="risk-factor-item">
                    {currentResult.label === 'FRAUD' ? (
                      <AlertTriangle size={16} color="#ef4444" />
                    ) : currentResult.label === 'REVIEW' ? (
                      <AlertTriangle size={16} color="#f59e0b" />
                    ) : (
                      <UserCheck size={16} color="#10b981" />
                    )}
                    <span>{factor}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
              Select a scenario or click "Analyze Transaction Risk" to view results.
            </div>
          )}
        </section>
      </main>

      {/* MLOps Pipeline Control Panel */}
      <section className="glass-panel section-card" style={{ borderColor: 'rgba(168, 85, 247, 0.3)' }}>
        <div className="card-title-row">
          <h2 className="card-title">
            <Cpu className="accent-icon" size={20} color="#a855f7" />
            MLOps Pipeline & Concept Drift Controls
          </h2>
          <span className="mono" style={{ fontSize: '0.8rem', color: '#a855f7' }}>
            Evidently AI + MLflow Engine
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          {/* Drift Control */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span className="input-label">1. Data Drift Monitor (Evidently AI)</span>
            <button 
              onClick={handleDriftCheck} 
              className="btn-submit" 
              style={{ background: 'linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)' }}
              disabled={driftLoading}
            >
              {driftLoading ? <RefreshCw className="pulse-online" size={18} /> : <Layers size={18} />}
              {driftLoading ? 'Evaluating Drift Metrics...' : '⚡ Run Data Drift Check'}
            </button>

            {driftState && (
              <div className="risk-factor-item" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                  <span style={{ fontWeight: 700, color: driftState.drift_detected ? '#ef4444' : '#10b981' }}>
                    {driftState.drift_detected ? '🚨 CONCEPT DRIFT DETECTED' : '✅ DATA DISTRIBUTION STABLE'}
                  </span>
                  <span className="mono">Score: {(driftState.drift_score * 100).toFixed(1)}%</span>
                </div>
                <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                  Drifted Features: {(driftState.drifted_features || []).join(', ')}
                </div>
              </div>
            )}
          </div>

          {/* Retrain Control */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span className="input-label">2. Automated Model Retrainer (MLflow)</span>
            <button 
              onClick={handleRetrain} 
              className="btn-submit" 
              style={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)' }}
              disabled={retrainLoading}
            >
              {retrainLoading ? <RefreshCw className="pulse-online" size={18} /> : <TrendingUp size={18} />}
              {retrainLoading ? 'Retraining Isolation Forest...' : '🔄 Trigger Automated Retrain'}
            </button>

            {retrainState && (
              <div className="risk-factor-item" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                  <span style={{ fontWeight: 700, color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <CheckCircle2 size={16} /> Model Retrained & Deployed
                  </span>
                  <span className="mono">{retrainState.model_version || 'v2.0'}</span>
                </div>
                <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                  Trained Samples: {retrainState.training_samples?.toLocaleString()} | Timestamp: {retrainState.timestamp}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Activity Log Table */}
      <section className="glass-panel section-card">
        <div className="card-title-row">
          <h2 className="card-title">
            <Globe className="accent-icon" size={20} color="#a855f7" />
            Live Analyzed Transactions Stream
          </h2>
          <span className="mono" style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
            Count: {history.length}
          </span>
        </div>

        <div className="table-container">
          <table className="transaction-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>User ID</th>
                <th>Amount</th>
                <th>Location</th>
                <th>Merchant</th>
                <th>Fraud Score</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td className="mono" style={{ color: '#9ca3af' }}>{item.time}</td>
                  <td className="mono">{item.user_id}</td>
                  <td className="mono" style={{ fontWeight: 600 }}>${item.amount.toLocaleString()}</td>
                  <td>{item.location}</td>
                  <td style={{ textTransform: 'capitalize' }}>{item.merchant.replace('_', ' ')}</td>
                  <td className="mono" style={{ fontWeight: 700 }}>
                    {(item.fraud_score * 100).toFixed(1)}%
                  </td>
                  <td>
                    <span className={`risk-badge badge-${item.label}`} style={{ padding: '3px 10px', fontSize: '0.75rem' }}>
                      {item.label}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
