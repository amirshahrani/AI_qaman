import json

filename = "location_updated.json"

def extract_location_data(filename):
    """
    Reads a GeoJSON file and extracts IDs and coordinates.
    Returns a dictionary: { 'id': [lat, long] }
    """
    extracted_data = {}

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        # Check if the file is a FeatureCollection (standard GeoJSON)
        if 'features' in data:
            items = data['features']
        else:
            # Fallback if the file is just a plain list of objects
            items = data

        for item in items:
            # 1. Navigate into 'properties' to get the 'id'
            # We use .get() to avoid crashing if a key is missing
            location_id = item.get('properties', {}).get('id')

            # 2. Navigate into 'geometry' to get the 'coordinates'
            coordinates = item.get('geometry', {}).get('coordinates')

            if location_id and coordinates:
                extracted_data[location_id] = coordinates

        print("Data loaded successfully.")
        return extracted_data

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {filename}.")
        return {}

locations = extract_location_data(filename)


output_filename = "location_output.json"

# Write this data to a file so we can test the reading function
with open(output_filename, 'w') as f:
    json.dump(locations, f, indent=4)
print(f"Created temporary file: {output_filename}\n")

# Print the results
print("\n--- Extracted Results ---")
for loc_id, coords in locations.items():
    print(f"ID: {loc_id}")
    print(f"Coordinates: {coords}")
    print("-" * 20)
    
    
