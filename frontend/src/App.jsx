import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { AlertTriangle, Thermometer, Shield, Clock, MapPin, Activity, Wind, Droplets } from 'lucide-react'
import HeatMap from './components/HeatMap'
import AreaCard from './components/AreaCard'
import CityAlert from './components/CityAlert'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedArea, setSelectedArea] = useState(null)
  const [error, setError] = useState(null)

  const fetchDashboard = async () => {
    setLoading(true)
    setError(null)
    try {
      const today = new Date().toISOString().split('T')[0]
      const res = await axios.get(`${API_BASE}/api/dashboard?date=${today}&time=14:00`)
      setDashboard(res.data)
    } catch (err) {
      console.error(err)
      setError("Failed to load heat data. Make sure your backend is running.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboard()
    const interval = setInterval(fetchDashboard, 300000) // Refresh every 5 min
    return () => clearInterval(interval)
  }, [])

  const getRiskColor = (level) => {
    const colors = {
      SAFE: '#22c55e',
      CAUTION: '#facc15',
      HIGH: '#ea580c',
      DANGER: '#dc2626',
      EXTREME: '#7f1d1d'
    }
    return colors[level] || '#64748b'
  }

  const getRiskIcon = (level) => {
    if (level === 'EXTREME' || level === 'DANGER') return <AlertTriangle size={20} />
    if (level === 'HIGH') return <Thermometer size={20} />
    return <Shield size={20} />
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Thermometer className="logo-icon" size={32} />
            <div>
              <h1>HeatSafe Karachi</h1>
              <p>AI-Powered Hyperlocal Heat Risk Intelligence</p>
            </div>
          </div>
          <div className="header-meta">
            <span className="badge">Powered by FortyGuard</span>
            <span className="timestamp">
              <Clock size={14} /> {dashboard?.timestamp || 'Loading...'}
            </span>
          </div>
        </div>
      </header>

      {/* City Alert Banner */}
      {dashboard?.city_wide_alert && (
        <CityAlert alert={dashboard.city_wide_alert} />
      )}

      {/* Main Content */}
      <main className="main">
        {loading && !dashboard ? (
          <div className="loading">
            <Activity size={48} className="spin" />
            <p>Analyzing Karachi's micro-climate with FortyGuard AI...</p>
            <p className="loading-sub">This may take 30-60 seconds for first load</p>
          </div>
        ) : error ? (
          <div className="error">
            <AlertTriangle size={48} />
            <p>{error}</p>
            <button onClick={fetchDashboard}>Retry</button>
          </div>
        ) : (
          <>
            {/* Stats Row */}
            <div className="stats-row">
              {dashboard?.areas?.map(area => (
                <div 
                  key={area.area_name}
                  className={`stat-card ${selectedArea?.area_name === area.area_name ? 'active' : ''}`}
                  onClick={() => setSelectedArea(area)}
                  style={{ borderLeft: `4px solid ${getRiskColor(area.risk.risk_level)}` }}
                >
                  <div className="stat-header">
                    <MapPin size={16} />
                    <span className="stat-name">{area.area_name}</span>
                    <span className="stat-risk" style={{ color: getRiskColor(area.risk.risk_level) }}>
                      {getRiskIcon(area.risk.risk_level)} {area.risk.risk_level}
                    </span>
                  </div>
                  <div className="stat-temp">
                    <Thermometer size={18} />
                    <span className="temp-max">{area.temperature_stats.max}°C</span>
                    <span className="temp-mean">avg {area.temperature_stats.mean}°C</span>
                  </div>
                  {area.risk.wet_bulb && (
                    <div className="stat-wb">
                      <Droplets size={14} /> Wet Bulb: {area.risk.wet_bulb}°C
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Map + Detail Panel */}
            <div className="content-grid">
              <div className="map-section">
                <HeatMap 
                  areas={dashboard?.areas || []} 
                  selectedArea={selectedArea}
                  onSelectArea={setSelectedArea}
                />
              </div>

              <div className="detail-panel">
                {selectedArea ? (
                  <AreaCard area={selectedArea} riskColor={getRiskColor(selectedArea.risk.risk_level)} />
                ) : (
                  <div className="detail-placeholder">
                    <MapPin size={48} />
                    <p>Click an area card or map zone to see detailed heat risk analysis</p>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>HeatSafe Karachi — Hackathon Project | Data: FortyGuard Temperature API </p>
      </footer>
    </div>
  )
}

export default App
