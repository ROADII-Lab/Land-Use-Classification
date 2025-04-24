import osmnx as ox
import geopandas as gpd

# Step 1: Load your cleaned city boundary GeoJSON
city_boundary = gpd.read_file("Land-Use-Classification/cleanedBoundary.geojson")

# Step 2: Get the geometry of the city (assuming it's a single geometry)
city_geom = city_boundary.geometry.values[0]

# Step 3: Retrieve road geometries using OSMnx
roads = ox.features_from_polygon(city_geom, tags={"highway": True})

# Convert the results to a GeoDataFrame
roads_gdf = gpd.GeoDataFrame.from_features(roads)

# Optionally, inspect the first few rows to check the data
print(roads_gdf.head())

# Additional Step: Convert geometry to WKT format for CSV saving
roads_gdf["geometry_wkt"] = roads_gdf.geometry.apply(lambda geom: geom.wkt)

# Step 5: Save the GeoDataFrame to a CSV file, including relevant attributes
# Select columns to include in the CSV file, including the WKT geometry
columns_to_include = [
    "geometry_wkt",
    "addr:street",
    "highway",
]  # Adjust based on attributes of interest
roads_gdf[columns_to_include].to_csv(
    "Land-Use-Classification/roads_data.csv", index=False
)

print("Road data has been saved to 'roads_data.csv'.")
