import osmnx as ox
import geopandas as gpd

# Load your cleaned city boundary GeoJSON
city_boundary = gpd.read_file("path/to/cleanedBoundary.geojson")
city_geom = city_boundary.geometry.values[0]

# Retrieve building geometries using OSMnx
buildings = ox.features_from_polygon(city_geom, tags={"building": True})
buildings_gdf = gpd.GeoDataFrame.from_features(buildings)

# Retrieve road geometries using OSMnx
roads = ox.features_from_polygon(city_geom, tags={"highway": True})
roads_gdf = gpd.GeoDataFrame.from_features(roads)


# Function to calculate nearest road distance and point
def nearest_point_on_polygon(building):
    polygon = building.geometry
    nearest_distance = float("inf")  # Initialize the maximum distance
    nearest_point = None

    # Loop through road geometries to find the nearest point
    for index, road in roads_gdf.iterrows():
        road_geom = road.geometry

        if road_geom.type == "LineString":
            # Calculate the distance from the building polygon to the road LineString
            distance = polygon.distance(road_geom)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_point = road_geom.interpolate(
                    road_geom.project(polygon.centroid)
                )

    return nearest_distance, nearest_point


# Apply function to calculate nearest distance and point for each building
buildings_gdf["nearest_distance"], buildings_gdf["nearest_road_point"] = zip(
    *buildings_gdf.apply(nearest_point_on_polygon, axis=1)
)

# Debugging: Check if columns have been created
print(buildings_gdf.columns)

# Inspect the results
print(buildings_gdf[["geometry", "nearest_distance", "nearest_road_point"]].head())
