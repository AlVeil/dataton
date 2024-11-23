import folium

# Initialize a map
m = folium.Map(location=[64.128, -21.817], zoom_start=10)

# Add the GeoJSON layer
folium.GeoJson(
    "C:/Users/alksn/Desktop/DS dream/gagnathon/stops.geojson",  # Replace with the path to your GeoJSON file
    name="GeoJSON Layer",
    style_function=lambda x: {'color': 'blue', 'weight': 2, 'fillOpacity': 0.4}
).add_to(m)

# Save the Folium map
m.save("geojson_map.html")

# Paths to the files
folium_map_path = "C:/Users/alksn/Desktop/DS dream/gagnathon/dataton/geojson_map.html"
local_map_path = "C:/Users/alksn/Desktop/DS dream/gagnathon/dataton/map.html"
combined_map_path = "C:/Users/alksn/Desktop/DS dream/gagnathon/dataton/combined_map.html"

# Read the contents of the Folium map
with open(folium_map_path, "r") as folium_file:
    folium_content = folium_file.read()

# Read the contents of your local HTML map
with open(local_map_path, "r") as local_map_file:
    local_map_content = local_map_file.read()

# Combine the two maps into one HTML file
combined_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Combined Map</title>
</head>
<body>
    <h1>Combined Map</h1>
    <div style="width: 100%; height: 50%;">{folium_content}</div>
    <div style="width: 100%; height: 50%;">{local_map_content}</div>
</body>
</html>
"""

# Save the combined map as an HTML file
with open(combined_map_path, "w") as combined_file:
    combined_file.write(combined_content)

print(f"Combined map saved to {combined_map_path}")

# Example of embedding the standalone map into Folium's output
combined_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Combined Map</title>
</head>
<body>
    <h1>GeoJSON + HTML Map</h1>
    <div style="width: 100%; height: 50%;">{folium_content}</div>
    <div style="width: 100%; height: 50%;">{local_map_content}</div>
</body>
</html>
"""

with open("combined_map.html", "w") as combined_map:
    combined_map.write(combined_content)
