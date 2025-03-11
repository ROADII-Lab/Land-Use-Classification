import fiona
import geopandas as gpd
from shapely.geometry import shape
import json

texas_buildings_path = "texas.geojson"
cc_boundary_path = "CorpusChristi.geojson"
output_geojson_path = "CorpusChristi_buildings.geojson"

boundary_gdf = gpd.read_file(cc_boundary_path)
boundary_union = boundary_gdf.dissolve().geometry.iloc[0]
cc_minx, cc_miny, cc_maxx, cc_maxy = boundary_union.bounds

# Prepare a file to store only Corpus buildings
# We'll write valid GeoJSON features manually
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
    
print("Finished creating CorpusChristi_buildings.geojson!")
