# test_data_processor.py

import unittest
from Legacy.data_processor import DataProcessor
import pandas as pd
import logging
import os
import tempfile


class TestDataProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging once for all tests
        logging.basicConfig(
            filename='test_data_processor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        logging.info("\n========== Starting DataProcessor Tests ==========")

    def setUp(self):
        logging.info("========== Starting new test ==========")
        # Create a temporary directory for visualizations
        self.temp_dir = tempfile.mkdtemp()

    def test_clean_data(self):
        logging.info("========== Starting: test_clean_data ==========")

        raw_data = [
            {'url': 'https://example.com', 'name': 'Test', 'price': '20.5', 'date': '2021-01-01'},
            {'url': 'https://example.com/page2', 'name': None, 'price': '15.0', 'date': '2021-02-01'},
            {'url': 'https://example.com/page3', 'name': 'Another', 'price': None, 'date': 'Invalid Date'}
        ]

        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        # Verify data types
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_data['price']), "Price column should be numeric")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_data['date']), "Date column should be datetime")
        self.assertEqual(cleaned_data.loc[0, 'name'], 'Test', "Name should be preserved as 'Test'")

        logging.info("Completed: test_clean_data")

    def test_handle_missing_data(self):
        logging.info("========== Starting: test_handle_missing_data ==========")

        raw_data = [
            {'url': 'https://example.com', 'name': 'Test', 'price': None},
            {'url': 'https://example.com/page2', 'name': None, 'price': '15.0'}
        ]

        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        # Applying 'fill_value' strategy
        handled_data = processor.handle_missing_data(
            cleaned_data, strategy='fill_value', value='N/A'
        )

        # Verify that missing values have been filled with 'N/A'
        self.assertFalse(handled_data.isnull().values.any())
        self.assertTrue((handled_data['name'] == 'N/A').any())
        self.assertTrue((handled_data['price'] == 'N/A').any())

        logging.info("Completed: test_handle_missing_data")

    def test_save_data_csv(self):
        logging.info("========== Starting: test_save_data_csv ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            processor.save_data(cleaned_data, temp_file.name, 'csv')

            # Read from temp_file and perform assertions
            with open(temp_file.name, 'r') as f:
                content = f.read()
                self.assertIn('Test', content)

        # Clean up temporary file
        os.remove(temp_file.name)
        logging.info("Completed: test_save_data_csv")

    def test_save_data_json(self):
        logging.info("========== Starting: test_save_data_json ==========")

        raw_data = [{'url': 'https://example.com', 'name': 'Test'}]
        processor = DataProcessor(raw_data)
        cleaned_data = processor.clean_data()

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            processor.save_data(cleaned_data, temp_file.name, 'json')

            # Read from temp_file and perform assertions
            with open(temp_file.name, 'r') as f:
                content = f.read()
                self.assertIn('Test', content)

        # Clean up temporary file
        os.remove(temp_file.name)
        logging.info("Completed: test_save_data_json")

    def test_visualize_data(self):
        logging.info("========== Starting: test_visualize_data ==========")

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
            output_dir=self.temp_dir,
            visualization_types=['histogram', 'bar_chart']
        )

        # Check if the visualization files were created
        expected_files = [
            os.path.join(self.temp_dir, 'views_histogram.png'),
            os.path.join(self.temp_dir, 'category_bar_chart.png')
        ]

        for file_path in expected_files:
            self.assertTrue(os.path.exists(file_path), f"Visualization file {file_path} should exist.")
            logging.info(f"Visualization created: {file_path}")

        logging.info("Completed: test_visualize_data")

    def tearDown(self):
        # Remove temporary directory and its contents
        if os.path.exists(self.temp_dir):
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
            os.rmdir(self.temp_dir)

    @classmethod
    def tearDownClass(cls):
        logging.info("\n========== Completed DataProcessor Tests ==========")

if __name__ == '__main__':
    unittest.main()
