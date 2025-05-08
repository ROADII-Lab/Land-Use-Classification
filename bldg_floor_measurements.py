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
    floor_information = ox.features_from_place(place, {"building:True"})
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
    floor_information = ox.features_from_place(place, {"building:True"})
    floor_information["levels"] = pd.to_numeric(
        floor_information["building:levels"], errors="coerce"
    )
    return floor_information["levels"].median()
