import os
import osmnx as ox
import geopandas as gpd
import pandas as pd


def standardize_to_crs(gdf: gpd.GeoDataFrame, crs="EPSG:3857") -> gpd.GeoDataFrame:
    """Standardize a GeoDataFrame to a specified CRS."""
    return gdf.to_crs(crs)


def get_buildings_and_roads(place: str) -> tuple:
    """Fetch building and road geometries for the specified place."""
    # Fetch building geometries
    buildings = ox.features_from_place(place, tags={"building": True})
    if "building:levels" not in buildings.columns:
        buildings["building:levels"] = None
    buildings = standardize_to_crs(buildings)

    # Fetch road network
    roads = ox.graph_to_gdfs(
        ox.graph_from_place(place, network_type="all"), nodes=False
    )
    roads = standardize_to_crs(roads)

    return buildings, roads


def calculate_building_stats(buildings_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Process building data to calculate additional statistics (e.g., mean floors)."""
    temp_buildings_gdf = buildings_gdf.copy()
    temp_buildings_gdf["levels"] = pd.to_numeric(
        temp_buildings_gdf["building:levels"], errors="coerce"
    )

    # Calculate summary stats per building
    temp_buildings_gdf["mean_floors"] = temp_buildings_gdf["levels"].mean()
    temp_buildings_gdf["median_floors"] = temp_buildings_gdf["levels"].median()

    return temp_buildings_gdf


def calculate_setback_stats(
    buildings_gdf: gpd.GeoDataFrame, roads_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Calculate average building setbacks based on proximity to roads."""
    temp_buildings_gdf = buildings_gdf.copy().to_crs(roads_gdf.crs)

    # Calculate distance to the nearest road segment
    nearest_road_geom = roads_gdf.geometry.union_all()
    temp_buildings_gdf["setback"] = temp_buildings_gdf.geometry.apply(
        lambda geom: geom.distance(nearest_road_geom)
    )

    return temp_buildings_gdf


def merge_buildings_into_roads(
    buildings_gdf: gpd.GeoDataFrame, roads_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Combine building information into the road GeoDataFrame."""
    # Perform spatial join to associate buildings with road segments
    joined = gpd.sjoin_nearest(
        buildings_gdf, roads_gdf, how="left", distance_col="building_to_road_distance"
    )

    # Aggregate building statistics for each road segment (mean setback as an example)
    road_stats = (
        joined.groupby("index_right")
        .agg(
            mean_building_setback=("setback", "mean"),
            mean_floors=("levels", "mean"),
            median_floors=("levels", "median"),
        )
        .reset_index()
    )

    # Merge aggregated stats back into the road GeoDataFrame
    final_roads_gdf = roads_gdf.reset_index().merge(
        road_stats, left_on="index", right_on="index_right", how="left"
    )

    return final_roads_gdf


def consolidate_geodataframes(
    buildings_gdf: gpd.GeoDataFrame, roads_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Combine building and road networks into a single GeoDataFrame."""
    # Add building data columns into the road GeoDataFrame
    merged_gdf = merge_buildings_into_roads(buildings_gdf, roads_gdf)

    # Append building geometries directly into the road GeoDataFrame
    full_gdf = pd.concat(
        [merged_gdf, buildings_gdf.assign(osmid=None)], ignore_index=True
    )

    return full_gdf


place = "Corpus Christi, Texas, USA"

# Step 1: Fetch buildings and roads
print("Fetching buildings and roads...")
buildings, roads = get_buildings_and_roads(place)

# Step 2: Process building statistics
print("Calculating building statistics...")
buildings = calculate_building_stats(buildings)

# Step 3: Calculate building setbacks
print("Calculating building setbacks...")
buildings_with_setbacks = calculate_setback_stats(buildings, roads)

# Step 4: Merge building data into roads
print("Merging building data into roads...")
roads_with_stats = merge_buildings_into_roads(buildings_with_setbacks, roads)

# Step 5: Consolidate everything into a unified GeoDataFrame
print("Consolidating GeoDataFrames...")
final_geodataframe = consolidate_geodataframes(
    buildings_with_setbacks, roads_with_stats
)

# Print the results
print("Unified GeoDataFrame:")
print(final_geodataframe.head())
print(final_geodataframe.info())
