import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
import os
import matplotlib.pyplot as plt

# Function to read OneDrive path from a text file `OneDrive.txt`
def read_path_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            path = file.readline().strip()  # Read the first line and strip whitespace
        return path
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_blocks_with_traffic_counts(
    block_file, npmrds_dataset_csv, osm_boundary_place, buffer_distance=50, output_shapefile=None, output_csv=None
):
    """
    Process Census blocks and apply traffic counts (AADT) from NPMRDS dataset via spatial joins.
    Assign a unique index as the block identifier for easier tracking and ensure operations are limited
    to blocks and roads within Corpus Christi, Texas.
    """
    import matplotlib.pyplot as plt

    # Step 1: Load the block shapefile for all of Texas
    print(f"Loading block shapefile for all of Texas: {block_file}")
    blocks = gpd.read_file(block_file)

    # Assign a unique index to each block
    print("Creating unique index for each block...")
    blocks["BLOCK_ID"] = range(len(blocks))

    # Project blocks to UTM Zone 14N for spatial comparisons
    print("Projecting blocks to UTM Zone 14N for spatial joins...")
    blocks = blocks.to_crs(epsg=32614)

    # Debug: Inspect block columns
    print("Columns in the block shapefile:")
    print(blocks.columns)

    # Step 2: Fetch OSM road network for Corpus Christi
    print(f"Fetching OSM road network for {osm_boundary_place}...")
    road_network = ox.graph_from_place(osm_boundary_place, network_type="drive")
    osm_edges = ox.graph_to_gdfs(road_network, nodes=False)

    # Project OSM roads to match CRS of the blocks
    print("Projecting OSM roads to UTM Zone 14N...")
    osm_edges = osm_edges.to_crs(blocks.crs)

    # Step 3: Create buffer around OSM roads
    print(f"Creating a buffer of {buffer_distance} meters around OSM roads...")
    osm_edges["geometry"] = osm_edges.buffer(buffer_distance)

    # Perform spatial join between buffered OSM roads and Texas blocks
    print("Performing spatial join between OSM roads and Texas blocks...")
    osm_with_blocks = gpd.sjoin(blocks, osm_edges, how="inner", predicate="intersects")

    # Debug: Inspect spatial join results
    print("Sample spatial join result for buffered OSM roads:")
    print(osm_with_blocks.head())

    # Filter blocks to include only those in Corpus Christi that intersect the buffers
    print("Filtering blocks to retain those intersecting the OSM road buffer...")
    corpus_christi_blocks = blocks[blocks["BLOCK_ID"].isin(osm_with_blocks["BLOCK_ID"])].copy()
    print(f"Remaining blocks after filtering: {len(corpus_christi_blocks)}/{len(blocks)}")

    # Step 4: Aggregate block length metrics
    print("Calculating block length metrics...")
    road_groups = osm_with_blocks.groupby("BLOCK_ID")["length"].agg(
        longest_segment="max",     # Longest road segment in the block
        avg_intersection_length="mean"  # Average segment length in the block
    ).reset_index()

    # Merge block length metrics into the filtered blocks
    corpus_christi_blocks = corpus_christi_blocks.merge(road_groups, how="left", on="BLOCK_ID")
    corpus_christi_blocks["longest_segment"] = corpus_christi_blocks["longest_segment"].fillna(0)
    corpus_christi_blocks["avg_intersection_length"] = corpus_christi_blocks["avg_intersection_length"].fillna(0)

    # Debug: Inspect blocks with road metrics
    print("Blocks with road metrics:")
    print(corpus_christi_blocks.head())

    # Step 5: Associate traffic counts (AADT) from NPMRDS roads
    print(f"Loading NPMRDS dataset CSV: {npmrds_dataset_csv}")
    npmrds_df = pd.read_csv(npmrds_dataset_csv)

    # Create geometries for NPMRDS roads using start and end coordinates
    print("Creating geometries for NPMRDS roads...")
    npmrds_df["geometry"] = npmrds_df.apply(
        lambda row: LineString([(row["start_longitude"], row["start_latitude"]),
                                (row["end_longitude"], row["end_latitude"])]),
        axis=1
    )
    npmrds_roads = gpd.GeoDataFrame(npmrds_df, geometry="geometry", crs="EPSG:4326")

    # Project NPMRDS roads to match CRS of Corpus Christi blocks
    print("Projecting NPMRDS roads to UTM Zone 14N...")
    npmrds_roads = npmrds_roads.to_crs(blocks.crs)

    # Create buffer around NPMRDS roads
    print(f"Applying a buffer of {buffer_distance} meters to NPMRDS roads...")
    npmrds_roads["geometry"] = npmrds_roads.buffer(buffer_distance)

    # Perform spatial join between buffered NPMRDS roads and Corpus Christi blocks
    print("Performing spatial join for buffered NPMRDS roads with Corpus Christi blocks...")
    npmrds_with_blocks = gpd.sjoin(corpus_christi_blocks, npmrds_roads, how="inner", predicate="intersects")

    # Debug: Inspect spatial join results for NPMRDS roads
    print("Sample spatial join result for buffered NPMRDS roads:")
    print(npmrds_with_blocks.head())

    # Step 6: Aggregate traffic count metrics (AADT)
    print("Calculating traffic count metrics (AADT)...")
    aadt_metrics = npmrds_with_blocks.groupby("BLOCK_ID")[["aadt"]].mean().reset_index()

    # Merge traffic count metrics into blocks with filtered OSM roads
    corpus_christi_blocks = corpus_christi_blocks.merge(aadt_metrics, how="left", on="BLOCK_ID")
    corpus_christi_blocks["aadt"] = corpus_christi_blocks["aadt"].fillna(0)

    # Visualization
    print("Plotting filtered blocks and intersecting roads...")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot OSM roads (buffered)
    osm_edges.plot(ax=ax, color="red", linewidth=0.5, alpha=0.5, label="Buffered Roads (OSM)")

    # Plot NPMRDS roads (buffered)
    npmrds_roads.plot(ax=ax, color="green", linewidth=0.5, alpha=0.5, label="Buffered Roads (NPMRDS)")

    # Plot filtered blocks (Corpus Christi blocks with roads)
    corpus_christi_blocks.plot(ax=ax, color="blue", alpha=0.5, edgecolor="black", label="Filtered Blocks (Corpus Christi)")

    # Manually construct legend handles
    from matplotlib.patches import Patch

    legend_handles = [
        Patch(color="red", label="Buffered Roads (OSM)"),
        Patch(color="green", label="Buffered Roads (NPMRDS)"),
        Patch(color="blue", label="Filtered Blocks (Corpus Christi)"),
    ]

    # Add legend with custom handles
    plt.legend(handles=legend_handles)
    plt.title("Corpus Christi Blocks and Roads Within Buffered Areas")
    plt.show()

    # Save updated blocks to shapefile and CSV
    if output_shapefile:
        print(f"Saving updated Corpus Christi blocks shapefile to: {output_shapefile}")
        corpus_christi_blocks.to_file(output_shapefile)
    if output_csv:
        print(f"Saving filtered Corpus Christi blocks with metrics to CSV: {output_csv}")
        corpus_christi_blocks[["BLOCK_ID", "longest_segment", "avg_intersection_length", "HOUSING20", "POP20", "aadt"]].to_csv(output_csv, index=False)

    print("Processing completed.")
    return corpus_christi_blocks

def main():
    # Define paths to block shapefile, NPMRDS dataset, and OSM boundary
    one_drive_path = read_path_from_file("OneDrive.txt")

    block_path = os.path.join(one_drive_path, "Data", "tl_2023_48_tabblock20", "tl_2023_48_tabblock20.shp")
    npmrds_path = os.path.join(one_drive_path, "Data", "Corpus_ChristiTMCNPMRDS.csv")
    osm_boundary_place = "Corpus Christi, Texas, USA"

    # Process blocks and save results
    processed_blocks = process_blocks_with_traffic_counts(
        block_file=block_path,
        npmrds_dataset_csv=npmrds_path,
        osm_boundary_place=osm_boundary_place,
        buffer_distance=50,
        output_shapefile="output\\Corpus_Christi_blocks_mod_results.shp",
        output_csv="output\\Corpus_Christi_blocks_mod_results.csv"
    )

    # Print results
    print(processed_blocks.head())

main()
