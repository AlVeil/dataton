import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Read the JSON data
with open('data/processed/cityline_2025_4326.geojson', 'r') as f:
    data = json.load(f)

# Create lists to store points for each line
red_line_points = []
blue_line_points = []
stations = []

# Sort features by line color and store coordinates
for feature in data['features']:
    coords = feature['geometry']['coordinates']
    if feature['properties']['line'] == 'red':
        red_line_points.append(coords)
    elif feature['properties']['line'] == 'blue':
        blue_line_points.append(coords)

    # Add station features
    stations.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coords},
        "properties": feature['properties']
    })

# Create LineString features for red and blue lines
red_line = {
    "type": "Feature",
    "geometry": {"type": "LineString", "coordinates": red_line_points},
    "properties": {"line": "red"}
}
blue_line = {
    "type": "Feature",
    "geometry": {"type": "LineString", "coordinates": blue_line_points},
    "properties": {"line": "blue"}
}

# Combine all features into a GeoJSON FeatureCollection
geojson_result = {
    "type": "FeatureCollection",
    "features": [red_line, blue_line] + stations
}

# Save to a GeoJSON file
output_path = 'data/processed/reykjavik_bus_lines.geojson'
with open(output_path, 'w') as f:
    json.dump(geojson_result, f, indent=4)

print(f"GeoJSON saved to {output_path}")
