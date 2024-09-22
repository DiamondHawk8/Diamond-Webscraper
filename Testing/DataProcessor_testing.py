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
        logging.info("\n========== Starting new test ==========")
        # Ensure the output directory for visualizations exists
        if not os.path.exists('visualizations'):
            os.makedirs('visualizations')

    def test_clean_data(self):
        logging.info("========== Starting: test_clean_data ==========")

        # Use more comprehensive raw data for better test coverage
        raw_data = [{'url': 'https://example.com', 'name': 'Test', 'price': '20.5'},
                    {'url': 'https://example.com/page2', 'name': None, 'price': '15.0'},
                    {'url': 'https://example.com/page3', 'name': 'Another', 'price': None}]

        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        self.assertIsInstance(cleaned_data, pd.DataFrame)
        self.assertFalse(cleaned_data.empty)
        logging.info("Completed: test_clean_data")

    def test_handle_missing_data(self):
        logging.info("========== Starting: test_handle_missing_data ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test', 'price': None},
                    {'url': 'https://example.com/page2', 'name': None, 'price': '15.0'}]

        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        # Applying 'fill_value' strategy
        handled_data = processor.handle_missing_data(cleaned_data, strategy='fill_value', value=0)

        # Verify that there are no missing values and the correct replacements were made
        self.assertFalse(handled_data.isnull().values.any())
        self.assertTrue((handled_data['name'] == 0).any())
        logging.info("Completed: test_handle_missing_data")

    def test_save_data_csv(self):
        logging.info("========== Starting: test_save_data_csv ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()  # Make sure it's a DataFrame
        processor.save_data(cleaned_data, 'test_data.csv', 'csv')

        # Check if the file was created and has content
        try:
            with open('test_data.csv', 'r') as f:
                content = f.read()
                self.assertIn('Test', content)
            logging.info("test_save_data_csv: CSV file saved and validated successfully")
        except Exception as e:
            logging.error(f"Error in test_save_data_csv: {e}")
            raise

        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')
            logging.info("CSV test file removed after validation")

        logging.info("Completed: test_save_data_csv")

    def test_save_data_json(self):
        logging.info("========== Starting: test_save_data_json ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()  # Ensure it's a DataFrame
        processor.save_data(cleaned_data, 'test_data.json', 'json')

        # Check if the file was created and has content
        try:
            with open('test_data.json', 'r') as f:
                content = f.read()
                self.assertIn('Test', content)
            logging.info("test_save_data_json: JSON file saved and validated successfully")
        except Exception as e:
            logging.error(f"Error in test_save_data_json: {e}")
            raise

        if os.path.exists('test_data.json'):
            os.remove('test_data.json')
            logging.info("JSON test file removed after validation")

        logging.info("Completed: test_save_data_json")

    def test_visualize_data(self):
        logging.info("========== Starting: test_visualize_data ==========")

        # Use more comprehensive data for visualization
        raw_data = [
            {'url': 'https://example.com', 'views': 100, 'category': 'Tech'},
            {'url': 'https://example.com/page2', 'views': 150, 'category': 'Health'},
            {'url': 'https://example.com/page3', 'views': 90, 'category': 'Tech'},
            {'url': 'https://example.com/page4', 'views': 200, 'category': 'Finance'}
        ]

        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        processor.visualize_data(
            data_frame=cleaned_data,
            output_dir='visualizations',
            visualization_types=['histogram', 'bar']
        )

        # Check if the visualization files were created
        expected_files = ['visualizations/url_bar.png', 'visualizations/category_bar.png',
                          'visualizations/views_histogram.png']
        for file in expected_files:
            self.assertTrue(os.path.exists(file))
            logging.info(f"Visualization created: {file}")

            # Clean up after the test
            os.remove(file)

        logging.info("Completed: test_visualize_data")

    def tearDown(self):
        # Clean up the visualizations directory if empty
        if os.path.exists('visualizations') and not os.listdir('visualizations'):
            os.rmdir('visualizations')


if __name__ == '__main__':
    unittest.main()
