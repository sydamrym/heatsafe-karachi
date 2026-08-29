import React from 'react'
import { MapContainer, TileLayer, Polygon, Popup, Marker, Circle } from 'react-leaflet'
import L from 'leaflet'
import { AlertTriangle, Thermometer } from 'lucide-react'
import { renderToString } from 'react-dom/server'

// Fix Leaflet default icons
import icon from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
})
L.Marker.prototype.options.icon = DefaultIcon

const AREA_BOUNDS = {
  "Clifton": [[24.805, 67.015], [24.830, 67.045]],
  "Korangi Industrial Area": [[24.820, 67.120], [24.845, 67.150]],
  "Saddar": [[24.855, 67.005], [24.870, 67.025]],
  "Lyari": [[24.860, 66.985], [24.880, 67.005]]
}

const RISK_COLORS = {
  SAFE: '#22c55e',
  CAUTION: '#facc15',
  HIGH: '#ea580c',
  DANGER: '#dc2626',
  EXTREME: '#7f1d1d'
}

const getPolygonForArea = (areaName) => {
  const bounds = AREA_BOUNDS[areaName]
  if (!bounds) return []
  const [[sw_lat, sw_lng], [ne_lat, ne_lng]] = bounds
  return [
    [sw_lat, sw_lng],
    [sw_lat, ne_lng],
    [ne_lat, ne_lng],
    [ne_lat, sw_lng],
    [sw_lat, sw_lng]
  ]
}

const getCenter = (areaName) => {
  const bounds = AREA_BOUNDS[areaName]
  if (!bounds) return [24.86, 67.0]
  const [[sw_lat, sw_lng], [ne_lat, ne_lng]] = bounds
  return [(sw_lat + ne_lat) / 2, (sw_lng + ne_lng) / 2]
}

const createCustomIcon = (riskLevel, temp) => {
  const color = RISK_COLORS[riskLevel] || '#64748b'
  const iconHtml = renderToString(
    <div style={{
      background: color,
      borderRadius: '50%',
      width: '36px',
      height: '36px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 'bold',
      fontSize: '12px',
      border: '3px solid white',
      boxShadow: '0 2px 8px rgba(0,0,0,0.4)'
    }}>
      {Math.round(temp)}°
    </div>
  )
  return L.divIcon({
    html: iconHtml,
    className: 'custom-marker',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
  })
}

function HeatMap({ areas, selectedArea, onSelectArea }) {
  const karachiCenter = [24.86, 67.0]

  return (
    <MapContainer 
      center={karachiCenter} 
      zoom={12} 
      style={{ height: '100%', width: '100%', minHeight: '450px' }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {areas.map(area => {
        const polygon = getPolygonForArea(area.area_name)
        const center = getCenter(area.area_name)
        const isSelected = selectedArea?.area_name === area.area_name
        const riskColor = RISK_COLORS[area.risk.risk_level] || '#64748b'
        const maxTemp = area.temperature_stats.max || 35

        return (
          <React.Fragment key={area.area_name}>
            {/* Heat zone polygon */}
            <Polygon
              positions={polygon}
              pathOptions={{
                fillColor: riskColor,
                fillOpacity: isSelected ? 0.5 : 0.25,
                color: riskColor,
                weight: isSelected ? 3 : 1,
                dashArray: isSelected ? null : '5, 5'
              }}
              eventHandlers={{
                click: () => onSelectArea(area)
              }}
            >
              <Popup>
                <div style={{ minWidth: '200px', fontFamily: 'system-ui' }}>
                  <h3 style={{ margin: '0 0 8px', color: riskColor }}>{area.area_name}</h3>
                  <p style={{ margin: '4px 0', fontSize: '14px' }}>
                    <strong>Max:</strong> {maxTemp}°C
                  </p>
                  <p style={{ margin: '4px 0', fontSize: '14px' }}>
                    <strong>Risk:</strong> <span style={{ color: riskColor, fontWeight: 'bold' }}>{area.risk.risk_level}</span>
                  </p>
                  <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                    {area.risk.message.substring(0, 80)}...
                  </p>
                  <button 
                    onClick={() => onSelectArea(area)}
                    style={{
                      marginTop: '8px',
                      background: '#f97316',
                      color: 'white',
                      border: 'none',
                      padding: '6px 16px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontWeight: '600'
                    }}
                  >
                    View Details
                  </button>
                </div>
              </Popup>
            </Polygon>

            {/* Temperature marker */}
            <Marker
              position={center}
              icon={createCustomIcon(area.risk.risk_level, maxTemp)}
              eventHandlers={{
                click: () => onSelectArea(area)
              }}
            />

            {/* Heat radius circle for danger zones */}
            {(area.risk.risk_level === 'DANGER' || area.risk.risk_level === 'EXTREME') && (
              <Circle
                center={center}
                radius={1500}
                pathOptions={{
                  fillColor: riskColor,
                  fillOpacity: 0.1,
                  color: riskColor,
                  weight: 1,
                  dashArray: '10, 10'
                }}
              />
            )}
          </React.Fragment>
        )
      })}
    </MapContainer>
  )
}

export default HeatMap
