# Karachi test areas with GeoJSON polygons and landmarks
# Coordinates are approximate bounding boxes for demo purposes

KARACHI_AREAS = {
    "clifton": {
        "name": "Clifton",
        "description": "Affluent coastal neighborhood with sea breeze",
        "polygon": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [67.015, 24.805],
                        [67.045, 24.805],
                        [67.045, 24.830],
                        [67.015, 24.830],
                        [67.015, 24.805]
                    ]]
                }
            }]
        },
        "landmarks": [
            {"name": "Clifton Beach", "type": "public_space", "lat": 24.810, "lon": 67.025},
            {"name": "The Forum School", "type": "school", "lat": 24.815, "lon": 67.028},
            {"name": "Clifton Park", "type": "public_space", "lat": 24.818, "lon": 67.022},
            {"name": "Dolmen Mall", "type": "market", "lat": 24.813, "lon": 67.030},
        ]
    },
    "korangi": {
        "name": "Korangi Industrial Area",
        "description": "Industrial zone with high concrete coverage and low ventilation",
        "polygon": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [67.120, 24.820],
                        [67.150, 24.820],
                        [67.150, 24.845],
                        [67.120, 24.845],
                        [67.120, 24.820]
                    ]]
                }
            }]
        },
        "landmarks": [
            {"name": "Korangi Factory Complex", "type": "construction", "lat": 24.830, "lon": 67.135},
            {"name": "Korangi Public School", "type": "school", "lat": 24.832, "lon": 67.128},
            {"name": "Sector 33 Market", "type": "market", "lat": 24.835, "lon": 67.140},
            {"name": "Korangi General Hospital", "type": "hospital", "lat": 24.828, "lon": 67.132},
        ]
    },
    "saddar": {
        "name": "Saddar",
        "description": "Dense commercial district with heavy traffic and concrete",
        "polygon": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [67.005, 24.855],
                        [67.025, 24.855],
                        [67.025, 24.870],
                        [67.005, 24.870],
                        [67.005, 24.855]
                    ]]
                }
            }]
        },
        "landmarks": [
            {"name": "Empress Market", "type": "market", "lat": 24.862, "lon": 67.010},
            {"name": "Saddar Bus Terminal", "type": "public_space", "lat": 24.865, "lon": 67.015},
            {"name": "City School Saddar", "type": "school", "lat": 24.860, "lon": 67.008},
            {"name": "Jinnah Hospital", "type": "hospital", "lat": 24.858, "lon": 67.012},
        ]
    },
    "lyari": {
        "name": "Lyari",
        "description": "Dense residential area with limited green cover",
        "polygon": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [66.985, 24.860],
                        [67.005, 24.860],
                        [67.005, 24.880],
                        [66.985, 24.880],
                        [66.985, 24.860]
                    ]]
                }
            }]
        },
        "landmarks": [
            {"name": "Lyari General Hospital", "type": "hospital", "lat": 24.870, "lon": 66.995},
            {"name": "Baghdadi Market", "type": "market", "lat": 24.868, "lon": 66.992},
            {"name": "Lyari Football Ground", "type": "public_space", "lat": 24.872, "lon": 66.998},
        ]
    }
}

# For demo fallback when API is slow/unavailable
MOCK_HEATMAP_DATA = {
    "clifton": {
        "temperature_stats": {"min": 34.2, "max": 36.8, "mean": 35.4},
        "geojson": None  # Would contain actual tile data
    },
    "korangi": {
        "temperature_stats": {"min": 39.5, "max": 44.2, "mean": 41.8},
        "geojson": None
    },
    "saddar": {
        "temperature_stats": {"min": 37.1, "max": 40.5, "mean": 38.8},
        "geojson": None
    },
    "lyari": {
        "temperature_stats": {"min": 38.0, "max": 42.3, "mean": 40.1},
        "geojson": None
    }
}
