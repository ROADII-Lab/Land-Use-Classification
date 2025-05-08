import osmnx as ox
import geopandas as gpd
import pandas as pd


def building_floor_mean(place: str) -> float:
    """Creates a mean calculation of the number of floors of buildings for a given place based on OpenStreetMap data. Format: "City, State, Country Abbreviation" (Example: "New York City, New York, USA")

    Args:
        place (str): City, State, Country of place of the desired calculation.

    Returns:
        float: Mean of the number of floors for a place.
    """
    floor_information = ox.features_from_place(place, {"building": True})
    floor_information["levels"] = pd.to_numeric(
        floor_information["building:levels"], errors="coerce"
    )
    return floor_information["levels"].mean()


def building_floor_median(place: str) -> float:
    """Calculates the median number of floors in the buildings for a given area using OpenStreetMap data.

    Args:
        place (str): Place where calculations are desired. Format: "City, State, Country Abbreviation" Example: "Los Angeles, California, USA"

    Returns:
        float: Median number of floors
    """
    floor_information = ox.features_from_place(place, {"building": True})
    floor_information["levels"] = pd.to_numeric(
        floor_information["building:levels"], errors="coerce"
    )
    return floor_information["levels"].median()


def building_floor_stats_by_road(place: str) -> pd.DataFrame:
    """Calculates mean and median number of floors in buildings for each road segment
    in the specified place using OpenStreetMap data.

    Args:
        place (str): City, State, Country of place of the desired calculation.

    Returns:
        pd.DataFrame: DataFrame with mean and median floors for each road segment.
    """
    # Fetch buildings and the road network for the place
    buildings = ox.features_from_place(place, {"building": True})  # Corrected tag
    roads = ox.graph_to_gdfs(
        ox.graph_from_place(place, network_type="all"), nodes=False
    )

    # Convert to GeoDataFrame
    buildings_gdf = gpd.GeoDataFrame(buildings)
    buildings_gdf["levels"] = pd.to_numeric(
        buildings_gdf["building:levels"], errors="coerce"
    )
    # Nearest road segment
    joined = gpd.sjoin_nearest(buildings_gdf, roads, distance_col="distance")
    stats = (
        joined.groupby("index_right")
        .agg(mean_floors=("levels", "mean"), median_floors=("levels", "median"))
        .reset_index()
    )
    stats = stats.merge(
        roads[["osmid", "geometry"]], left_on="index_right", right_on="osmid"
    )

    return stats[["osmid", "geometry", "mean_floors", "median_floors"]]


def building_setback_from_footprint(place: str) -> pd.DataFrame:
    """Calculates average building setbacks for each road segment in a specified place
    using OpenStreetMap building footprints.

    Args:
        place (str): City, State, Country of the desired calculation.

    Returns:
        pd.DataFrame: DataFrame with average setbacks for each road segment.
    """

    buildings = ox.features_from_place(place, {"building": True})
    buildings_gdf = gpd.GeoDataFrame(buildings)
    roads_gdf = ox.graph_to_gdfs(
        ox.graph_from_place(place, network_type="all"), nodes=False
    )

    # Setback = distance from nearest road using building footprint for accuracy
    building_setbacks = []
    for idx, building in buildings_gdf.iterrows():
        # Calculate the distance to the nearest road
        nearest_road_geo = roads_gdf.geometry.unary_union
        distance = building.geometry.distance(
            nearest_road_geo
        )  # Distance to the nearest road
        building_setbacks.append(distance)
    buildings_gdf["setback"] = building_setbacks

    # Average setbacks by road segment
    stats = (
        buildings_gdf.groupby("road_id")
        .agg(average_setback=("setback", "mean"))
        .reset_index()
    )
    stats = stats.merge(
        roads_gdf[["osmid", "geometry"]], left_on="road_id", right_on="osmid"
    )

    return stats[["osmid", "geometry", "average_setback"]]
