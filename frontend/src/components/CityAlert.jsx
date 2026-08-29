import React from 'react'
import { AlertTriangle, X } from 'lucide-react'

function CityAlert({ alert }) {
  const [dismissed, setDismissed] = React.useState(false)

  if (dismissed) return null

  return (
    <div className="city-alert">
      <AlertTriangle size={20} />
      <span>{alert}</span>
      <button 
        onClick={() => setDismissed(true)}
        style={{ 
          background: 'none', 
          border: 'none', 
          color: 'white', 
          cursor: 'pointer',
          marginLeft: 'auto'
        }}
      >
        <X size={18} />
      </button>
    </div>
  )
}

export default CityAlert
