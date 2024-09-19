import pandas as pd
import logging


class DataProcessor:
    """
    A class to clean and transform scraped data.
    """

    def __init__(self, data):
        """
        Initializes the DataProcessor instance with the scraped data.

        Args:
            data (list): The raw data extracted from the WebScraper (e.g., list of dictionaries).
        """
        self.data = data
        self.cleaned_data = self.clean_data()

    def clean_data(self):
        """
        Cleans the raw scraped data.

        Returns:
            pandas.DataFrame: The cleaned data as a DataFrame.
        """
        logging.info("Cleaning data")
        df = pd.DataFrame(self.data)
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        # Attempt to ensure data is properly managed
        # If column cannot be converted, remains as its original type
        for col in df.columns:
            # Check if the column is likely numeric
            if df[col].dtype == 'object':
                try:
                    # Convert to numeric if possible, ignoring errors.
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except Exception as e:
                    logging.warning(f"Failed to convert column {col} to numeric: {e}")

            # If the column looks like dates, try to convert to datetime
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except Exception as e:
                logging.warning(f"Failed to convert column {col} to datetime: {e}")
        return df

    # TODO Potentially change mode to append/allow choice
    def save_data(self, file_path, file_format='csv'):
        """
        Saves the cleaned data to a file (CSV or JSON).

        Args:
            file_path (str): The output file path (including filename).
            file_format (str): The format to save the data ('csv' or 'json'). Defaults to 'csv'.
        """
        logging.info("Saving data")
        try:
            if file_format not in ['csv', 'json']:
                logging.error(f"File format must be 'csv' or 'json'. Found: {file_format}")
                raise ValueError('file_format must be either "csv" or "json"')
            else:
                if file_format == 'csv':

                    self.cleaned_data.to_csv(file_path, index=False)
                    logging.info(f"Data successfully saved to {file_path} in CSV format.")
                else:
                    self.cleaned_data.to_json(file_path)
                    logging.info(f"Data successfully saved to {file_path} in JSON format.")

        except Exception as e:
            logging.error(f"Error while saving data: {e}")
            raise e
