import osmnx as ox
import geopandas as gpd


boundary_gdf = gpd.read_file("Land-Use-Classification\cc_boundary_box.geojson")
boundary_geom = boundary_gdf.geometry.values[0]  # Assuming it's a single MultiPolygon
if not boundary_geom.is_valid:
    print("The MultiPolygon geometry is invalid. Attempting to fix it...")
    boundary_geom = boundary_geom.buffer(0)  # Clean up the geometry

if boundary_geom.is_valid:
    print("The MultiPolygon geometry is now valid.")
    cleaned_gdf = gpd.GeoDataFrame(geometry=[boundary_geom], crs=boundary_gdf.crs)

    cleaned_gdf.to_file(
        "Land-Use-Classification\cleanedBoundary.geojson", driver="GeoJSON"
    )
    print("Cleaned geometry saved as 'cleaned_boundary.geojson'.")
else:
    print("The cleaned geometry is still invalid. Please check the original data.")
