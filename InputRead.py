import pandas as pd
import fiona
import geopandas as gpd
from shapely.geometry import shape
import geojson
import json
import folium

# Function to read One Drive path from file OneDrive.txt
def read_path_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            path = file.readline().strip()  # Read the first line and strip whitespace
        return path
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def ReadTMC ():
    TMCPath_CorpusChristi = OneDrivePath + '\\Data\\Corpus_ChristiTMCNPMRDS.csv'
    # Read the TMC CSV file into a DataFrame
    df = pd.read_csv(TMCPath_CorpusChristi)


def CropBuilding():
    texas_buildings_path = OneDrivePath + "\\Data\\texas.geojson"
    cc_boundary_path = OneDrivePath + "\\Data\\CorpusChristi_Boundary.geojson"
    output_path = OneDrivePath + '\\Output\\CC_Buildings.geojson'

    # Step 1: Load the GeoJSON files
    buildings_gdf = gpd.read_file(texas_buildings_path)
    corpus_christi_boundary_gdf = gpd.read_file(cc_boundary_path)

    # Step 2: Ensure that both GeoDataFrames have the same CRS (Coordinate Reference System)
    if buildings_gdf.crs != corpus_christi_boundary_gdf.crs:
        buildings_gdf = buildings_gdf.to_crs(corpus_christi_boundary_gdf.crs)

    # Step 3: Perform the spatial operation to get buildings within Corpus Christi
    buildings_within_cc = gpd.overlay(buildings_gdf, corpus_christi_boundary_gdf, how='intersection')

    # Step 4: Extract only the necessary polygon geometry
    result_gdf = buildings_within_cc[['geometry']]

    # Step 5: Save the result to a new GeoJSON file (if needed)
    result_gdf.to_file(output_path, driver='GeoJSON')

    print("Processing complete! The buildings within Corpus Christi have been extracted.")

def plotCCBuildings():
    # Step 1: Load the GeoJSON file using GeoPandas
    geojson_path = OneDrivePath + "\\Output\\CC_Buildings.geojson"
    corpus_christi_gdf = gpd.read_file(geojson_path)

    # Step 2: Create a Folium map centered on Corpus Christi
    center = corpus_christi_gdf.geometry.centroid.iloc[0].y, corpus_christi_gdf.geometry.centroid.iloc[0].x

    m = folium.Map(location=center, zoom_start=12)

    # Step 3: Add the GeoJSON layer to the map
    folium.GeoJson(
        corpus_christi_gdf,
        name="Corpus Christi"
    ).add_to(m)

    # Step 4: Add layer control (optional)
    folium.LayerControl().add_to(m)

    # Step 5: Save the map to an HTML file
    m.save(OneDrivePath + "\\Output\\corpus_christi_map.html")
    print("Map has been created and saved as 'corpus_christi_map.html'.")

def main():
    #ReadTMC()
    #CropBuilding
    plotCCBuildings()

if __name__ == "__main__":
    # Create Text file called OneDrive.txt in root directory containing Path to OneDrive data folder
    OneDrivetxt = 'OneDrive.txt'
    OneDrivePath = read_path_from_file(OneDrivetxt)
    main()