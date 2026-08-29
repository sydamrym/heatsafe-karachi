import React from 'react'
import { 
  AlertTriangle, Shield, Thermometer, Droplets, 
  Clock, MapPin, School, ShoppingBag, HardHat, 
  Hospital, Trees, Sun, ChevronRight 
} from 'lucide-react'

const ICONS = {
  school: School,
  market: ShoppingBag,
  construction: HardHat,
  hospital: Hospital,
  public_space: Trees
}

const RISK_LABELS = {
  SAFE: { icon: Shield, label: 'Safe Conditions' },
  CAUTION: { icon: Sun, label: 'Use Caution' },
  HIGH: { icon: Thermometer, label: 'High Risk' },
  DANGER: { icon: AlertTriangle, label: 'Danger Zone' },
  EXTREME: { icon: AlertTriangle, label: 'EXTREME EMERGENCY' }
}

function AreaCard({ area, riskColor }) {
  const riskInfo = RISK_LABELS[area.risk.risk_level] || RISK_LABELS.SAFE
  const RiskIcon = riskInfo.icon

  return (
    <div className="area-card">
      {/* Header */}
      <div className="area-header" style={{ borderLeft: `4px solid ${riskColor}` }}>
        <div className="area-title-row">
          <MapPin size={18} color={riskColor} />
          <h2>{area.area_name}</h2>
          <span className="risk-badge" style={{ background: riskColor }}>
            <RiskIcon size={14} /> {area.risk.risk_level}
          </span>
        </div>
        <p className="area-message">{area.risk.message}</p>
      </div>

      {/* AI Summary */}
      <div className="ai-summary">
        <div className="ai-label">
          <Shield size={14} /> AI Safety Analysis
        </div>
        <p>{area.ai_summary}</p>
      </div>

      {/* Temperature Stats */}
      <div className="temp-grid">
        <div className="temp-item">
          <Thermometer size={18} />
          <div>
            <span className="temp-value">{area.temperature_stats.max}°C</span>
            <span className="temp-label">Maximum</span>
          </div>
        </div>
        <div className="temp-item">
          <Thermometer size={18} />
          <div>
            <span className="temp-value">{area.temperature_stats.mean}°C</span>
            <span className="temp-label">Average</span>
          </div>
        </div>
        <div className="temp-item">
          <Droplets size={18} />
          <div>
            <span className="temp-value">{area.risk.wet_bulb || '--'}°C</span>
            <span className="temp-label">Wet Bulb</span>
          </div>
        </div>
        <div className="temp-item">
          <Thermometer size={18} />
          <div>
            <span className="temp-value">{area.risk.heat_index || '--'}°C</span>
            <span className="temp-label">Heat Index</span>
          </div>
        </div>
      </div>

      {/* Safest Window */}
      <div className="safest-window">
        <Clock size={16} />
        <div>
          <strong>Safest Outdoor Window:</strong>
          <p>{area.safest_window}</p>
        </div>
      </div>

      {/* Action Items */}
      <div className="actions-section">
        <h3><ChevronRight size={16} /> Recommended Actions</h3>
        <ul>
          {area.risk.actions.map((action, i) => (
            <li key={i} className={action.includes('URGENT') || action.includes('SUSPEND') ? 'urgent' : ''}>
              {action.includes('🎓') && <School size={14} />}
              {action.includes('🏗️') && <HardHat size={14} />}
              {action.includes('🛒') && <ShoppingBag size={14} />}
              {action.includes('🏥') && <Hospital size={14} />}
              {!action.includes('🎓') && !action.includes('🏗️') && !action.includes('🛒') && !action.includes('🏥') && <Shield size={14} />}
              {action}
            </li>
          ))}
        </ul>
      </div>

      {/* Landmarks */}
      <div className="landmarks-section">
        <h3><MapPin size={16} /> Key Locations</h3>
        <div className="landmarks-grid">
          {area.landmarks.map((lm, i) => {
            const Icon = ICONS[lm.type] || MapPin
            return (
              <div key={i} className="landmark-chip">
                <Icon size={14} />
                <span>{lm.name}</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default AreaCard
