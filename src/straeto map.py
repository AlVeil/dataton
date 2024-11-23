import pandas as pd
import json
import os

def load_gtfs_files (directory):
    """
    Loads GTFS files into pandas DataFrames.

    Args:
        directory (gtfs_directory = "C://Users/alksn/Desktop/DS dream/gagnathon/gtfs"): Path to the directory containing GTFS files.
    
    Returns:
        dict: A dictionary where keys are GTFS file names and values are DataFrames.
    """
    gtfs_files = ["stops.txt", "shapes.txt"]
    dataframes = {}

    for file_name in gtfs_files:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(directory):
            try:
                df = pd.read_csv(file_path)
                dataframes[file_name] = df
                print(f"Loaded {file_name} with {len(df)} rows.")
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        else:
            print(f"{file_name} not found in {directory}.")
    
    return dataframes

def stops_to_geojson(stops_df):
    """
    Converts GTFS stops.txt to GeoJSON format.

    Args:
        stops_df (pd.DataFrame): DataFrame containing stops.txt data.
    
    Returns:
        dict: GeoJSON feature collection for stops.
    """
    features = []
    for _, row in stops_df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["stop_lon"], row["stop_lat"]]
            },
            "properties": {
                "stop_id": row["stop_id"],
                "stop_name": row["stop_name"]
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

def shapes_to_geojson(shapes_df):
    """
    Converts GTFS shapes.txt to GeoJSON format.

    Args:
        shapes_df (pd.DataFrame): DataFrame containing shapes.txt data.
    
    Returns:
        dict: GeoJSON feature collection for shapes.
    """
    shapes_grouped = shapes_df.groupby("shape_id")
    features = []
    
    for shape_id, group in shapes_grouped:
        coordinates = group.sort_values("shape_pt_sequence")[["shape_pt_lon", "shape_pt_lat"]].values.tolist()
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {
                "shape_id": shape_id
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

def save_geojson(geojson_data, output_path):
    """
    Saves GeoJSON data to a file.

    Args:
        geojson_data (dict): GeoJSON data.
        output_path (str): Path to save the GeoJSON file.
    """
    with open(output_path, "w") as f:
        json.dump(geojson_data, f, indent=4)
    print(f"GeoJSON saved to {output_path}")

def main():
    # Path to the GTFS directory
    gtfs_directory = "C:/Users/alksn/Desktop/DS dream/gagnathon/gtfs"  # Update this with the GTFS directory
    output_directory = "C:/Users/alksn/Desktop/DS dream/gagnathon"  # Update with your desired output directory

    # Load GTFS files
    gtfs_data = load_gtfs_files(gtfs_directory)

    # Convert stops.txt to GeoJSON
    if "stops.txt" in gtfs_data:
        stops_geojson = stops_to_geojson(gtfs_data["stops.txt"])
        save_geojson(stops_geojson, os.path.join(output_directory, "stops.geojson"))

    # Convert shapes.txt to GeoJSON
    if "shapes.txt" in gtfs_data:
        shapes_geojson = shapes_to_geojson(gtfs_data["shapes.txt"])
        save_geojson(shapes_geojson, os.path.join(output_directory, "shapes.geojson"))

if __name__ == "__main__":
    main()
