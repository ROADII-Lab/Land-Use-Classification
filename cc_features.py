import osmnx as ox
import geopandas as gpd

land_use = ox.features_from_place("Corpus Christi, TX, USA", {"landuse": True})
print(land_use)
