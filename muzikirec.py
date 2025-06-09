# Importing Libraries
import pandas as pd
import os
import numpy as np
import logging

# Setting up logging to handle errors and information
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Import Data
def import_data():
    """
    Import the dataset from CSV files.
    """
    try:
        paths = {
            'data': './datasets/data.csv',
            'genre_data': './datasets/data_by_genres.csv',
            'year_data': './datasets/data_by_year.csv',
            'artist_data': './datasets/data_by_artist.csv'
        }

        datasets = {}

        for name, path in paths.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"{name} file not found at {path}")
            datasets[name] = pd.read_csv(path, error_bad_lines=False, warn_bad_lines=True)

        return datasets['data'], datasets['genre_data'], datasets['year_data'], datasets['artist_data']

    except FileNotFoundError as e:
        logging.error(e)
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    except pd.errors.EmptyDataError:
        logging.error("One or more files is empty.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

# Displaying Dataset Rows
def display_data(**datasets):
    """
    Display the first few rows of the provided datasets.
    """
    for name, data in datasets.items():
        if data is not None and not data.empty:
            print(f"\nDisplaying the first few rows of the {name} dataset:")
            print(data.head(2))
        else:
            logging.warning(f"No data available for {name} dataset.")

# Data Information
def data_info(**datasets):
    """
    Display information about the provided datasets.
    """
    for name, data in datasets.items():
        if data is not None and not data.empty:
            print(f"\n{name} dataset information:")
            print(data.info())
        else:
            logging.warning(f"No data available for {name} dataset.")

# Data Preprocessing - Creating Decade Column
def create_decade_column(data):
    """
    Create a decade column in the data dataset.
    """
    if 'year' in data.columns:
        data['decade'] = data['year'].apply(lambda x: (x // 10) * 10 if pd.notnull(x) else np.nan)
        data['decade'] = data['decade'].astype('Int64')  # Ensuring correct data type
        logging.info("Decade column created successfully.")
    else:
        logging.error("Year column not found in the dataset.")
    
    return data

# Main Function
def main():
    """
    Main function to run MuzikiRec.
    """
    print("Welcome to MuzikiRec - Music Recommendation System")
    logging.info("Importing data...")

    data, genre_data, year_data, artist_data = import_data()  # Import data from CSV files

    if data is not None and not data.empty:
        display_data(data=data)
        data_info(data=data, genre_data=genre_data)

        # Creating decade column
        data = create_decade_column(data)
        display_data(data=data)

        # Displaying first 2 rows of genre_data, year_data, artist_data
        display_data(genre_data=genre_data, year_data=year_data, artist_data=artist_data)

    else:
        logging.error("No data to display. Please check the import process.")

if __name__ == "__main__":
    main()