import pandas as pd
import geopandas as gpd

# Change username to connect to your OneDrive
username = 'Michael.Barzach'
onedrivepath_start = r'C:\\Users\\' 
onedrivepath_end = r'\\OneDrive - DOT OST\\Land Use\Data\\'
onedrivepath_final = onedrivepath_start + username + onedrivepath_end

TMCPath_CorpusChristi = onedrivepath_final + 'Corpus_ChristiTMCNPMRDS.csv'


def readTMC ():
    # Read the TMC CSV file into a DataFrame
    df = pd.read_csv(TMCPath_CorpusChristi)

    # Display the first few rows of the DataFrame
    print(df.head())

def main():
    readTMC()

if __name__ == "__main__":
        main()