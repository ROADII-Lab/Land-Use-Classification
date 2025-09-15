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

---

# Project Description

### ROADII Background

Research, Operational, and Artificial Intelligence Data Integration Initiative (ROADII) is a multi-year initiative led by the United States Department of Transportation (U.S. DOT) Intelligent Transportation Systems Joint Program Office (ITS JPO).

ROADII’s vision is to expand U.S. transportation agencies’ (regional, state, local, tribal, etc.) access to advanced data analytics knowledge and resources including Artificial Intelligence (AI) and Machine Learning (ML). The ROADII team:
- Identifies and evaluates **use cases** that can benefit from advanced data analytics, AI, and ML
- Develops **proofs-of-concept** for use cases
- **Engages stakeholders** with proofs-of-concept and refine based on stakeholder feedback
- **Makes advanced data analytics, AI, and ML tools** available to the public at a central location (e.g., ITS CodeHub) 

The processes and tools developed under ROADII will enable data scientists, researchers, and data providers to test and share new transportation-related AI algorithms; to develop high-value and well-documented AI training datasets; to reduce the barriers of applying AI approaches to transportation data; and to train future transportation researchers.

For more information, visit ITS JPO's website [here](https://www.its.dot.gov/).

### ROADII Use Case - Land Use Classification

- **Title:** Categorizing Land Use on Roadways  
- **Purpose and goals of the project:**  
  The purpose of this work is to support better land-use classification for roadway environments, improving understanding of infrastructure and transportation systems. The project integrates block-level and building-level data, enabling detailed metrics and analysis that can inform decision-making and planning in road-adjacent areas.  
- **Purpose of the source code and how it relates to the overall goals of the project:**  
  The provided source code facilitates the processing and analysis of key metrics related to buildings, blocks, and roads, such as building height, setback distances, population density, building area coverage, and road evacuation routes. It enables streamlined generation of data for use in additional modeling, GIS visualization, and analysis to better understand how land use interacts with roadway networks.  
- **Length of the project:**  
  This use case is currently in the exploratory phase and aims to grow as new requirements arise.

---

# Prerequisites

Requires:

- Python >= 3.7  
- Python libraries:  
  - **Geopandas**: For spatial data manipulation and analysis.  
  - **Shapely**: For geometry creation and analysis.  
  - **Fiona**: For file I/O with shapefiles.  
  - **OSMnx**: For interacting with OpenStreetMap data.  
  - **Pandas**: For tabular data manipulation.  

---

# Usage

## Testing

A placeholder for QA/QC notes and tests performed in ArcGIS will be provided in a later release. Preliminary validation confirms the following:
- Geometry-based overlaps between roads, blocks, and buildings are consistent.
- Metric calculations align with ArcGIS visualizations and documented spot checking.

---

## Execution

The primary workflow and code for replicating this analysis are contained in the `modular_process_CC.ipynb` Jupyter notebook. This notebook includes modular steps for:
1. Data loading and validation.
2. Building-level and block-level metric extraction.
3. Road metrics calculation, including overlap percentages and weighted averages.
4. Generating processed shapefiles for visualization in GIS platforms.
5. Running generated Road shape file through classification functions using input CSV's for Decision Tree, Point, and Classification Priority

To execute the analysis, open the `modular_process_CC.ipynb` notebook in Jupyter and follow the documented instructions for each step.

### One Drive Integration

The user of this script must set their one drive location in a text file named "OneDrive.txt" in the working directory of the script. This is where the data files referenced throughout the notebook are stored. This is processed in the first cell of the jupyter notebook. Below is an example of the contents of OneDrive.txt. It does not show up in the repo as it is included in `git.ignore` so each user can have their own location.

`C:\Users\Michael.Barzach\OneDrive - DOT OST\Land Use`

This folder contains a subfolder named `Data` that containts all relevant input datasets noted below in `Associated Datasets`

---

# Additional Notes

The Python OSMnx library is used in this project, and more information can be found in the following citation as well as the OSMnx documentation:  
Boeing, G. (2024). Modeling and Analyzing Urban Networks and Amenities with OSMnx. Working paper.  
https://geoffboeing.com/publications/osmnx-paper/  

### Associating Block Metrics with Roads

The overlap percentage between road buffers and blocks is calculated as the area of block overlap with the road buffer, divided by the total area of the road buffer. This ensures that metrics aggregation (e.g., building heights, population density) is weighted properly against each road.  
Metrics are aggregated by normalizing weights based on overlap percentages to ensure that total contributions from overlapping blocks sum accurately to 100%.

---

### Associated Datasets

This project uses the following datasets:

- **Census Blocks (2020):**  
  Shapefiles containing census block geometries and demographic attributes (e.g., population, housing units).  
  Source: U.S. Census Bureau TIGER/Line shapefiles.  

- **OpenStreetMap (OSM) Roads:**  
  Road geometries and attributes extracted for Corpus Christi using OSMnx tools.  
  Source: OpenStreetMap (OSM).  

- **OpenStreetMap (OSM) Buildings:**  
  Building geometries for Corpus Christi downloaded using OSMnx (includes building heights and areas).  
  Source: OpenStreetMap (OSM).  

- **Evacuation Routes (TxDOT):**  
  Geometry and attributes for Texas Department of Transportation (TxDOT) evacuation routes.  
  File: `TxDOT Evacuation Routes AGO.shp`.  
  Source: TxDOT.  

- **Employment Density Shapefile:**  
  Contains the geographic distribution of employment density values (in jobs per acre), converted to jobs per square mile for calculations.  
  File: `CBG2010_SLD_YY.shp`.  
  Source: Internal analysis datasets.

- **Urban Area Census Shapefile:**  
  Contains the geometries for urban areas from the census, used to flag roads intersecting or touching urban areas within Corpus Christi.  
  File: `2020_Census_Urban_Areas.shp`.  
  Source: U.S. Census Bureau.

**Additional References:**  
- **Data Dictionary:** [DATADICTIONARY.md](DATADICTIONARY.md)  
The data dictionary provides detailed descriptions of all columns in the datasets, including calculated metrics and associated input data.

---

# Version History and Retention

**Status:** This project is in active development phase.  
**Release Frequency:** This project will be updated when there are stable developments. This will be approximately every month.  
**Retention:** This project will likely remain publicly accessible indefinitely.  
**Release History:** See [CHANGELOG.md](CHANGELOG.md).

---

# License

This project is licensed under the Creative Commons 1.0 Universal (CC0 1.0) License - see the [License.MD](https://github.com/usdot-jpo-codehub/codehub-readme-template/blob/master/LICENSE) for more details.

---

# Contributions

Please read [CONTRIBUTING.md](https://github.com/ITSJPO-TRIMS/R25-IncidentDetection/blob/main/Contributing.MD) for details on our Code of Conduct, the process for submitting pull requests to us, and how contributions will be released.

---

# Contact Information

Contact Name: Eric Englin  
Contact Information: Eric.Englin@dot.gov  

---

# Acknowledgements

Sample citation should be in the below format, with the `formatted fields` replaced with details of your source code:  
_author_surname_or_organization, first_initial. (year)._ Program or source code title _(code_version)_ [Source code]. Provided by ITS/JPO and Volpe Center through GitHub.com. Accessed YYYY-MM-DD from doi_url._

---

## Citing this Code

To cite this code in a publication or report, please cite our associated report/paper and/or our source code. Below is a sample citation for this code:
> ROADII Team. (2024). ROADII README Template (0.1) [Source code]. Provided by ITS JPO through GitHub.com. Accessed 2024-02-23 from https://doi.org/xxx.xxx/xxxx.

When you copy or adapt this code, please include the original URL you copied the source code from and date of retrieval as a comment in your code. Additional information on how to cite can be found in the [ITS CodeHub FAQ](https://its.dot.gov/code/#/faqs).

---

## Contributors

- Michael Barzach (Volpe)    
- Ali Brodeur (Volpe)  
- Sophie Abo (Volpe)  
- Eric Englin (Volpe)
- Jeremy Hicks (Volpe)  

The development of ROADII that contributed to this public version was funded by the U.S. Intelligent Transportation Systems Joint Program Office (ITS JPO) under IAA HWE3A122. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the ITS JPO.
