# Corpus Christi Data Dictionary

This document provides a description of the columns contained in the shapefiles created by the data processing script. The datasets include **buildings**, **blocks**, and **roads** information, derived from spatial analysis and processed metrics.

---

## 1. Buildings Subset (`Corpus_Christi_buildings_subset.shp`)

| Column Name      | Description                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| `geometry`       | Geometries representing building footprints (polygons).                                       |
| `height`         | The height of the building in meters.                                                         |
| `setback_ft`     | Building setback calculated in feet as the closest point on the building to the union of all road geometries. |
| `build_idx`      | Unique ID for each building, assigned during processing.                                      |
| `build_area_sm`  | The area of the building footprint in square miles.                                           |
| `height_m`       | Building height in meters (converted from `height` if provided).                              |
| `height_ft`      | Building height in feet, calculated as `height_m * 3.28084`.                                  |

---

## 2. Blocks Processed (`Corpus_Christi_blocks_processed.shp`)

| Column Name   | Description                                                                                   |
|---------------|-----------------------------------------------------------------------------------------------|
| `STATEFP20`   | State FIPS code in 2020 Census data.                                                          |
| `COUNTYFP20`  | County FIPS code in 2020 Census data.                                                         |
| `TRACTCE20`   | Census tract code in 2020 Census data.                                                        |
| `BLOCKCE20`   | Census block code in 2020 Census data.                                                        |
| `GEOID20`     | Unique ID for census geography combining state, county, tract, and block FIPS codes.          |
| `ALAND20`     | Land area of the census block in square meters.                                               |
| `AWATER20`    | Water area of the census block in square meters.                                              |
| `HOUSING20`   | Total number of housing units in the census block in 2020.                                    |
| `POP20`       | Population in the census block as of the 2020 Census.                                         |
| `geometry`    | Geometries representing the boundaries of census blocks (polygons).                           |
| `BLOCK_ID`    | Unique identifier for each block, assigned during processing.                                 |
| `area_sm`     | Total area of the block in square miles (converted from `ALAND20`).                           |
| `pop_den`     | Population density (people per square mile), calculated as `POP20 / area_sm`.                 |
| `avg_hght`    | Average building height in the block in feet, excluding buildings with height data of `0`.    |
| `avg_sback`   | Average building setback distance (distance to nearest road, feet).                           |
| `bld_area`    | Total area of all building footprints in the block in square miles.                           |
| `bld_cnt`     | Total number of buildings in the block.                                                       |
| `bld_ctsm`    | Building count per square mile, calculated as `bld_cnt / area_sm`.                            |
| `bld_prc`     | Building area percentage, calculated as `(bld_area / area_sm) * 100`.                         |

---

## 3. Roads Processed (`Corpus_Christi_roads_processed.shp`)

| Column Name       | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| `osmid`           | OpenStreetMap ID for the road segment.                                                        |
| `highway`         | OpenStreetMap classification of the road (e.g., `residential`, `primary`, `secondary`).       |
| `lanes`           | Number of lanes on the road (if available).                                                   |
| `name`            | Name of the road segment or street.                                                           |
| `oneway`          | Indicates whether the road is one-way (`True`/`False`).                                       |
| `length`          | Length of the road segment in meters (FIX TO BE CALCULATED ON ROAD GEOMETRY).                 |
| `maxspeed`        | Maximum speed limit on the road (if available, in mph or km/h).                               |
| `geometry`        | Geometries representing the road as LineStrings.                                              |
| `road_id`         | Unique ID assigned to each road during processing.                                            |
| `agg_pop`         | Weighted average population density for roads based on overlapping blocks' `pop_den`.         |
| `agg_area`        | Weighted average building area for roads based on overlapping blocks' `bld_area`.             |
| `agg_ctsm`        | Weighted average building count per square mile for roads based on overlapping blocks' `bld_ctsm`. |
| `agg_bldprc`      | Weighted average of building area coverage percentage (`bld_prc`) for overlapping blocks.     |
| `agg_hght`        | Weighted average building height for roads based on overlapping blocks' `avg_hght`.           |
| `agg_sback`       | Weighted average building setback distance for roads based on overlapping blocks' `avg_sback`. |
| `block_ids`       | List of `BLOCK_ID`s that overlap with the road buffer.                                        |
| `overlap_percs`   | List of overlap percentages corresponding to the `block_ids` (same index alignment).          |
| `evac_flag`       | Flag indicating overlap with evacuation routes:                                               |
|                   | - `0`: No overlap                                                                             |
|                   | - `1`: Overlaps with Major Evacuation Routes                                                  |
|                   | - `2`: Overlaps with Potential Contraflow Routes                                              |
|                   | - `3`: Overlaps with Potential EvacuLanes                                                     |

---

## Overlap Percentages and Weighted Average Calculation

### Explanation of `block_ids` and `overlap_percs`:
1. **`block_ids`:**
   - A list of block IDs (`BLOCK_ID`) that overlap with the buffered geometry of the road.
   - Each road contains blocks whose boundaries intersect the **road buffer geometry**.

2. **`overlap_percs`:**
   - A list of overlap percentages corresponding to the blocks listed in `block_ids`.
   - Represents the proportion of the block area that overlaps with the road buffer area.

### Weighted Average Calculation:
Columns such as `agg_pop`, `agg_area`, `agg_ctsm`, `agg_hght`, `agg_sback`, and `agg_bldprc` are calculated as **weighted averages** based on overlap percentages.

#### Formula for Weighted Average:
For a metric `M` (e.g., `bld_area`, `avg_hght`):
1. Normalize the overlap percentages:
   ```math
   normalized_weight = overlap_percentage / total_overlap_percentage
2. Multiply each block's metric by its normalized weight:
   ```math
   Weighted Metric = Σ (block_metric * normalized_weight)