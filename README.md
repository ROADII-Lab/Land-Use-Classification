# README Outline:
* Project Description
* Prerequisites
* Usage
    * Testing
    * Execution
* Additional Notes
* Version History and Retention
* License
* Contributions
* Contact Information
* Acknowledgements

# Project Description
### ROADII Use Case - Land Use Classification
- **Title:** Categorizing Land Use on Roadways 
- **Purpose and goals of the project:**  
  The purpose of this work is to support better land-use classification for roadway environments, improving understanding of infrastructure and transportation systems. The project integrates block-level and building-level data, enabling detailed metrics and analysis that can inform decision-making and planning in road-adjacent areas. 
- **Purpose of the source code and how it relates to the overall goals of the project:**  
  The provided source code facilitates the processing and analysis of key metrics related to buildings, blocks, and roads, such as building height, setback distances, population density, building area coverage, and road evacuation routes. It enables streamlined generation of data for use in additional modeling, GIS visualization, and analysis to better understand how land use interacts with roadway networks.
- **Length of the project:**  
  This use case is currently in the exploratory phase and aims to grow as new requirements arise.

# Prerequisites
Requires:
- Python >= 3.7
- Python libraries:
  - **Geopandas**: For spatial data manipulation and analysis.
  - **Shapely**: For geometry creation and analysis.
  - **Fiona**: For file I/O with shapefiles.
  - **OSMnx**: For interacting with OpenStreetMap data.
  - **Pandas**: For tabular data manipulation.
- Datasets (see **Associated Datasets** below for details).

# Usage

## Testing
A placeholder for QA/QC notes and tests done in ArcGIS will be provided here in a later release. Preliminary validation confirms the following:
- Geometry-based overlaps between roads, blocks, and buildings are consistent.
- Metric calculations align with ArcGIS visualizations and documented spot checking.

## Execution
The primary workflow and code for replicating this analysis are contained in the `modular_process_CC.ipynb` Jupyter notebook. This notebook includes modular steps for:
1. Data loading and validation.
2. Building-level and block-level metric extraction.
3. Road metrics calculation, including overlap percentages and weighted averages.
4. Generating processed shapefiles for visualization in GIS platforms.

To execute the analysis, open the `modular_process_CC.ipynb` notebook in Jupyter and follow the documented instructions for each step.

# Additional Notes
The Python OSMnx library is used in this project and more information can be found at the following citation as well as the OSMnx documentation.
Boeing, G. (2024). Modeling and Analyzing Urban Networks and Amenities with OSMnx. Working paper. 
https://geoffboeing.com/publications/osmnx-paper/

### Associating Block Metrics with Roads
The overlap percentage between road buffers and blocks is calculated as the area of block overlap with the road buffer, divided by the total area of the road buffer. This ensures that metrics aggregation (e.g., building heights, population density) is weighted properly against each road. 

Metrics are aggregated by normalizing weights based on overlap percentages to ensure that total contributions from overlapping blocks sum accurately to 100%.

### Associated Datasets:
This project uses the following input datasets:
- **Census Blocks (2020):**
  - Shapefiles containing census block geometries and demographic attributes (e.g., population, housing units).
  - Source: U.S. Census Bureau TIGER/Line shapefiles.
- **OpenStreetMap (OSM) Roads:**
  - Road geometries and attributes extracted for Corpus Christi using OSMnx tools.
  - Source: OpenStreetMap (OSM).
- **OpenStreetMap (OSM) Buildings:**
  - Building geometries for Corpus Christi downloaded using OSMnx (includes building heights and areas).
  - Source: OpenStreetMap (OSM).
- **Evacuation Routes (TxDOT):**
  - Geometry and attributes for Texas Department of Transportation (TxDOT) evacuation routes.
  - File: `TxDOT Evacuation Routes AGO.shp`.
  - Source: TxDOT.

**Additional Reference File: [DATADICTIONARY.md](DATADICTIONARY.md)**
- The data dictionary provides detailed descriptions of all columns in the datasets, including calculated metrics and associated input data.

# Version History and Retention
**Status:** This project is in active development phase.  
**Release Frequency:** This project will be updated when there are stable developments. This will be approximately every month.  
**Retention:** This project will likely remain publicly accessible indefinitely.  
**Release History:** See [CHANGELOG.md](CHANGELOG.md).

# License
This project is licensed under the Creative Commons 1.0 Universal (CC0 1.0) License - see the [License.MD](https://github.com/usdot-jpo-codehub/codehub-readme-template/blob/master/LICENSE) for more details.

# Contributions
Please read [CONTRIBUTING.md](https://github.com/ITSJPO-TRIMS/R25-IncidentDetection/blob/main/Contributing.MD) for details on our Code of Conduct, the process for submitting pull requests to us, and how contributions will be released.

# Contact Information
Contact Name: Eric Englin  
Contact Information: Eric.Englin@dot.gov  

# Acknowledgements
*Sample citation should be in the below format, with the `formatted fields` replaced with details of your source code*  
_`author_surname_or_organization`, `first_initial`. (`year`)._ `program_or_source_code_title` _(`code_version`) [Source code]. Provided by ITS/JPO and Volpe Center through GitHub.com. Accessed YYYY-MM-DD from `doi_url`._

## Citing this code
To cite this code in a publication or report, please cite our associated report/paper and/or our source code. Below is a sample citation for this code:  
> ROADII Team. (2024). _ROADII README Template_ (0.1) [Source code]. Provided by ITS JPO through GitHub.com. Accessed 2024-02-23 from https://doi.org/xxx.xxx/xxxx.  
When you copy or adapt from this code, please include the original URL you copied the source code from and date of retrieval as a comment in your code. Additional information on how to cite can be found in the [ITS CodeHub FAQ](https://its.dot.gov/code/#/faqs).

## Contributors
- Michael Barzach (Volpe)
- Jeremy Hicks (Volpe)
- Ali Brodeur (Volpe)
- Sophie Abo (Volpe)
- Eric Englin (Volpe)  
The development of ROADII that contributed to this public version was funded by the U.S. Intelligent Transportation Systems Joint Program Office (ITS JPO) under IAA HWE3A122. Any opinions, findings, conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the ITS JPO.