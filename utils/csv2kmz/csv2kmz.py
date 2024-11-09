import csv
import simplekml
import argparse
import os
"""
A script to convert CSV files containing geographic data into KMZ files.

The input CSV file should contain the following columns:
- Latitude: The latitude coordinate (decimal degrees)
- Longitude: The longitude coordinate (decimal degrees) 
- Description: A description of the point (optional)
- FeatName: The name of the feature/point
- Type: The category/type of the point

The script will create separate KMZ files for each unique Type value in the CSV.
Points with the same Type will be grouped into the same KMZ file.

Example usage:
    python csv2kmz.py input.csv

This will create KMZ files named after each unique Type (e.g. School.kmz, Hospital.kmz)
that can be opened in Google Earth or other KML/KMZ viewers.
"""
def csv_to_kmz(csv_file):
    # Create a dictionary to hold KML objects for each type
    kml_files = {}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row_number, row in enumerate(reader, start=1):
            try:
                # Parse latitude and longitude
                latitude = float(row['Latitude'])
                longitude = float(row['Longitude'])
                
                # Get description and type, handling missing or empty values
                description = row.get('Description', 'No Description')
                feat_name = row.get('FeatName', 'Unknown')
                type_name = row.get('Type', 'Unknown').replace(' ', '')
                
                # Check if we already have a KML object for this type
                if type_name not in kml_files:
                    kml_files[type_name] = simplekml.Kml()

                # Add point to the appropriate KML object
                point = kml_files[type_name].newpoint(name=feat_name, coords=[(longitude, latitude)])
                point.description = description

            except ValueError:
                # Handle empty or invalid latitude/longitude values
                print(f"Warning: Invalid latitude or longitude at row {row_number}. Skipping this row.")
                continue

    # Save each KMZ file by type
    for type_name, kml in kml_files.items():
        kmz_file_name = f"{type_name}.kmz"
        kml.savekmz(kmz_file_name)
        print(f"KMZ file '{kmz_file_name}' has been created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to separate KMZ files for each type.")
    parser.add_argument("csv_file", help="Path to the input CSV file containing latitude, longitude, description, and type.")
    args = parser.parse_args()
    
    csv_to_kmz(args.csv_file)

