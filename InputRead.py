import pandas as pd
import fiona
import geopandas as gpd
from shapely.geometry import shape
import json

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

    # Display the first few rows of the DataFrame
    print(df.head())

def CropBuildingData():
    texas_buildings_path = OneDrivePath + "\\Data\\texas.geojson"
    cc_boundary_path = OneDrivePath + "\\Data\\CorpusChristi_Boundary.geojson"
    output_geojson_path = OneDrivePath + "\\Output\\CorpusChristi_buildings.geojson"

    boundary_gdf = gpd.read_file(cc_boundary_path)
    boundary_union = boundary_gdf.dissolve().geometry.iloc[0]
    cc_minx, cc_miny, cc_maxx, cc_maxy = boundary_union.bounds

    # Prepare a file to store only Corpus buildings
    with fiona.open(texas_buildings_path) as src, open(output_geojson_path, "w") as out_file:
        out_file.write('{"type": "FeatureCollection","features": [\n')
        
        total_features = len(src)
        print(f"Total features: {total_features}")
        first_feature = True
        
        for i, feature in enumerate(src):
            if i % 500000 == 0:
                print(f"Processed {i} features...")

            geom = shape(feature["geometry"])
            
            # bounding box check
            b_minx, b_miny, b_maxx, b_maxy = geom.bounds
            if (b_maxx < cc_minx or b_minx > cc_maxx or
                b_maxy < cc_miny or b_miny > cc_maxy):
                continue

            if geom.within(boundary_union):
                # Write the feature to the output file (as valid JSON)
                if not first_feature:
                    out_file.write(",\n")  # comma between features
                json.dump(feature, out_file)
                first_feature = False

        out_file.write("\n]}")
        
    print("Finished creating CorpusChristi_buildings.geojson")

def main():
    ReadTMC()
    CropBuildingData()

if __name__ == "__main__":
    # Create Text file called OneDrive.txt in root directory containing Path to OneDrive data folder
    OneDrivetxt = 'OneDrive.txt'
    OneDrivePath = read_path_from_file(OneDrivetxt)
    main()