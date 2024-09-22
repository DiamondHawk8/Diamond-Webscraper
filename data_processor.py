import pandas as pd
import logging
import os
import matplotlib.pyplot as plt


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

        # TODO, probably remove this
        self.normalized_data = None  # Set when normalize_data is called

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

        # TODO create lists of potential numeric and date values
        # Process each column selectively
        for col in df.columns:
            if isinstance(col, str):  # Ensure the column name is a string
                if col.lower().startswith(('price', 'amount', 'quantity', 'value', 'total', 'sum', 'score')):
                    # Numeric-like columns
                    try:
                        df[col] = pd.to_numeric(df[col])
                        if df[col].isnull().any():
                            logging.warning(f"Failed to fully convert column {col} to numeric")
                    except Exception as e:
                        logging.warning(f"Failed to convert column {col} to numeric: {e}")

                elif col.lower().startswith(('date', 'time', 'created', 'modified', 'at')):  # Date-like columns
                    try:
                        df[col] = pd.to_datetime(df[col])
                        if df[col].isnull().any():
                            logging.warning(f"Failed to fully convert column {col} to datetime")
                    except Exception as e:
                        logging.warning(f"Failed to convert column {col} to datetime: {e}")

                else:
                    logging.info(f"Skipping conversion for column {col}")

        return df

    def handle_missing_data(self, data_frame, strategy, value=None):
        """
        Handles missing values based on the strategy specified in config.yaml.
        """

        # Check to see if any values need to be handled in the first place
        total_missing_before = data_frame.isnull().sum().sum()

        if total_missing_before == 0:
            logging.info("No missing values detected")
            return data_frame

        logging.info(f"Handling missing data with method: {strategy}")
        # Processing is not done in place in case the original frame is needed later
        if strategy == 'drop':
            # TODO revise to all, and extrapolate data with more advanced reasoning (phase 4?)
            processed_data_frame = data_frame.dropna(axis=0, how='any')
        elif strategy == 'fill_mean':
            processed_data_frame = data_frame.fillna(data_frame.mean())
        elif strategy == 'fill_median':
            processed_data_frame = data_frame.fillna(data_frame.median())
        elif strategy == 'fill_value':
            # TODO allow alue filling (phase 4)
            processed_data_frame = data_frame.fillna(value)
        else:
            logging.warning(f"Strategy '{strategy}' is not supported.")
            return data_frame

        # Log the number of rows/columns affected
        total_missing_after = processed_data_frame.isnull().sum().sum()
        rows_affected = (total_missing_before - total_missing_after) / data_frame.shape[1]  # Average rows affected
        logging.info(f"Handled {total_missing_before - total_missing_after} missing values across approximately"
                     f" {rows_affected} rows.")
        return processed_data_frame

    # TODO Potentially change mode to append/allow choice
    def save_data(self, data_frame, file_path, file_format='csv'):
        """
        Saves the cleaned data to a file (CSV or JSON).

        Args:
            data_frame: the data to be saved as a DataFrame.
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

                    data_frame.to_csv(file_path, index=False)
                    logging.info(f"Data successfully saved to {file_path} in CSV format.")
                else:
                    data_frame.to_json(file_path)
                    logging.info(f"Data successfully saved to {file_path} in JSON format.")

        except Exception as e:
            logging.error(f"Error while saving data: {e}")
            raise e

    # TODO, add more advanced visualization options and customization (phase 3?)
    def visualize_data(self, data_frame, output_dir, visualization_types):
        """
        Generates data visualizations based on the DataFrame columns.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"Visualization output directory created at {output_dir}")

        for column in data_frame.columns:
            data = data_frame[column]

            # Check if the column is numeric
            if data_frame[column].dtype in ['int64', 'float64']:
                if 'histogram' in visualization_types:
                    # Plot the histogram for numeric data
                    plt.figure()
                    data.hist(bins=15, edgecolor='black')
                    plt.title(f'Histogram of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')

                    plot_path = os.path.join(output_dir, f"{column}_histogram.png")
                    plt.savefig(plot_path)
                    plt.close()
                    logging.info(f"Histogram saved for column '{column}' at {plot_path}")

            # Check if the column is categorical (object type)
            elif data_frame[column].dtype == 'object':
                if 'bar' in visualization_types:
                    # Generate a bar plot for categorical data
                    plt.figure()
                    data.value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
                    plt.title(f'Bar Plot of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Count')

                    plot_path = os.path.join(output_dir, f"{column}_bar.png")
                    plt.savefig(plot_path)
                    plt.close()
                    logging.info(f"Bar plot saved for column '{column}' at {plot_path}")
            else:
                logging.warning(f"Column '{column}' is neither numeric nor categorical and will be skipped.")
