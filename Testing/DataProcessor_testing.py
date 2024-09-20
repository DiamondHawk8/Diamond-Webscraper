import unittest
from data_processor import DataProcessor
import pandas as pd
import logging
import os

# Set up logging for the test cases
logging.basicConfig(
    filename='test_data_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        """Set up any state that is shared between the test methods."""
        logging.info("\n========== Starting new test ==========")

    def test_clean_data(self):
        logging.info("========== Starting: test_clean_data ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        self.assertIsInstance(cleaned_data, pd.DataFrame)
        self.assertFalse(cleaned_data.empty)
        logging.info("Completed: test_clean_data")

    def test_save_data_csv(self):
        logging.info("========== Starting: test_save_data_csv ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        processor.save_data('test_data.csv', 'csv')

        # Check if the file was created and has content
        try:
            with open('test_data.csv', 'r') as f:
                content = f.read()
                self.assertIn('Test', content)
            logging.info("test_save_data_csv: CSV file saved and validated successfully")
        except Exception as e:
            logging.error(f"Error in test_save_data_csv: {e}")
            raise

        # Cleanup
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')
            logging.info("CSV test file removed after validation")

        logging.info("Completed: test_save_data_csv")

    def test_save_data_json(self):
        logging.info("========== Starting: test_save_data_json ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        processor.save_data('test_data.json', 'json')

        # Check if the file was created and has content
        try:
            with open('test_data.json', 'r') as f:
                content = f.read()
                self.assertIn('Test', content)
            logging.info("test_save_data_json: JSON file saved and validated successfully")
        except Exception as e:
            logging.error(f"Error in test_save_data_json: {e}")
            raise

        # Cleanup
        if os.path.exists('test_data.json'):
            os.remove('test_data.json')
            logging.info("JSON test file removed after validation")

        logging.info("Completed: test_save_data_json")


if __name__ == '__main__':
    unittest.main()
