const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://localhost:8000' 
  : window.location.origin;
const API_KEY = 'fraud-api-key-x7k9m2p4';

export async function predictTransaction(transactionData) {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      body: JSON.stringify(transactionData),
    });

    if (!response.ok) {
      throw new Error(`API response status: ${response.status}`);
    }

    const data = await response.json();
    return { ...data, source: 'API' };
  } catch (error) {
    console.warn('FastAPI backend not reached. Running local rule score simulation:', error.message);
    return simulateLocalPrediction(transactionData);
  }
}

export async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (response.ok) {
      const data = await response.json();
      return { online: true, ...data };
    }
    return { online: false };
  } catch {
    return { online: false };
  }
}

export async function runDriftCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/mlops/drift-check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
    });
    if (!response.ok) throw new Error(`Status: ${response.status}`);
    return await response.json();
  } catch {
    return {
      drift_detected: true,
      drift_score: 0.42,
      drifted_features: ['amount', 'location_risk', 'merchant_risk', 'hour'],
      timestamp: new Date().toLocaleTimeString(),
      mode: 'Simulated'
    };
  }
}

export async function triggerRetrain() {
  try {
    const response = await fetch(`${API_BASE_URL}/mlops/retrain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
    });
    if (!response.ok) throw new Error(`Status: ${response.status}`);
    return await response.json();
  } catch {
    return {
      success: true,
      model_version: 'v2.0-auto-retrained',
      training_samples: 10000,
      timestamp: new Date().toLocaleTimeString(),
      mode: 'Simulated'
    };
  }
}

// Fallback scoring engine if backend is offline
function simulateLocalPrediction(txn) {
  let score = 0.05;
  const riskFactors = [];

  const amount = Number(txn.amount) || 0;
  if (amount > 15000) {
    score += 0.45;
    riskFactors.push('Unusually large transaction amount (>$15,000)');
  } else if (amount > 5000) {
    score += 0.25;
    riskFactors.push('High transaction value (>$5,000)');
  }

  const highRiskMerchants = ['crypto_exchange', 'casino', 'weapons', 'luxury_watch'];
  if (highRiskMerchants.includes(txn.merchant)) {
    score += 0.3;
    riskFactors.push(`High-risk merchant category (${txn.merchant})`);
  }

  const highRiskLocations = ['Nigeria', 'Russia', 'North Korea'];
  if (highRiskLocations.includes(txn.location)) {
    score += 0.25;
    riskFactors.push(`Cross-border anomaly location (${txn.location})`);
  }

  if (txn.time_of_day === 'midnight') {
    score += 0.15;
    riskFactors.push('Off-hours transaction velocity at midnight');
  }

  const finalScore = Math.min(0.99, Math.max(0.02, Number(score.toFixed(2))));
  
  let label = 'SAFE';
  if (finalScore >= 0.8) label = 'FRAUD';
  else if (finalScore >= 0.5) label = 'REVIEW';

  return {
    txn_id: 'sim-' + Math.random().toString(36).substring(2, 9),
    user_id: txn.user_id,
    amount: amount,
    fraud_score: finalScore,
    label: label,
    is_fraud_predicted: finalScore >= 0.8,
    risk_factors: riskFactors.length > 0 ? riskFactors : ['Normal transaction behavior within historical baseline'],
    timestamp: new Date().toLocaleTimeString(),
    source: 'Simulation'
  };
}
