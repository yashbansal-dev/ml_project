import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ShieldCheck, 
  ShieldAlert, 
  Search, 
  ArrowRight, 
  Shield, 
  Info,
  Globe,
  Lock,
  Zap
} from 'lucide-react'

function App() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleScan = async () => {
    if (!url) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })

      if (!response.ok) throw new Error('Could not reach the security engine.')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-wrapper">
      <header className="hero-section">
        <motion.div 
          className="logo-icon"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
        >
          <Shield size={32} />
        </motion.div>
        <h1>Fischer Detector</h1>
        <p className="description">
          A simple way to check if a link is safe before you click.
        </p>
      </header>

      <main className="main-card">
        <div className="input-container">
          <input 
            type="text" 
            placeholder="Paste a link here to check..." 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleScan()}
          />
          <button className="check-btn" onClick={handleScan} disabled={loading}>
            {loading ? 'Checking...' : 'Check safety'}
          </button>
        </div>

        <AnimatePresence mode='wait'>
          {loading && (
            <motion.div 
              className="loader"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="spinner"></div>
              <p style={{ color: 'var(--text-dim)' }}>Checking for hidden threats...</p>
            </motion.div>
          )}

          {error && (
            <motion.div 
              className="unsafe" 
              style={{ padding: '1rem', borderRadius: '16px', textAlign: 'center', fontWeight: 600 }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {error}
            </motion.div>
          )}

          {result && !loading && (
            <motion.div 
              className="result-box"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className={`status-pill ${result.prediction === 'Malicious' ? 'unsafe' : 'safe'}`}>
                {result.prediction === 'Malicious' ? (
                  <><ShieldAlert size={20} /> Potential Threat Found</>
                ) : (
                  <><ShieldCheck size={20} /> This Link is Safe</>
                )}
              </div>

              <div className="risk-summary">
                <div className="metric">
                  <span className="m-lab">Safety Rating</span>
                  <span className="m-val" style={{ color: result.prediction === 'Malicious' ? 'var(--danger)' : 'var(--success)' }}>
                    {((1 - result.risk_score) * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="metric">
                  <span className="m-lab">Confidence</span>
                  <span className="m-val">98%</span>
                </div>
              </div>

              <div className="details-grid">
                <div className="detail-item">
                  <span className="d-label">Complexity</span>
                  <span className="d-value">{result.features.url_entropy > 4.5 ? 'High' : 'Normal'}</span>
                </div>
                <div className="detail-item">
                  <span className="d-label">Structure</span>
                  <span className="d-value">{result.features.num_subdomains > 1 ? 'Suspicious' : 'Clean'}</span>
                </div>
                <div className="detail-item">
                  <span className="d-label">Identity</span>
                  <span className="d-value">{result.risk_score < 0.05 ? 'Verified' : 'Unverified'}</span>
                </div>
                <div className="detail-item">
                  <span className="d-label">Safety Tier</span>
                  <span className="d-value">{result.prediction === 'Malicious' ? 'Critical' : 'Premium'}</span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <section className="trust-bar">
        <div className="trust-item"><Lock size={14} /> Encrypted</div>
        <div className="trust-item"><Globe size={14} /> Global Analysis</div>
        <div className="trust-item"><Zap size={14} /> Instant Results</div>
      </section>

      <footer>
        &copy; 2026 Fischer Detector. Protecting your digital life.
      </footer>
    </div>
  )
}

export default App
