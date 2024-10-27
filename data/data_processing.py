# data/data_processing.py

from datetime import datetime
from config.settings import EXPECTED_RANGES
import logging

def parse_sensor_data(line):
    try:
        data = {}
        pairs = line.split(',')
        for pair in pairs:
            if ':' not in pair:
                continue  # Skip invalid pairs
            key, value = pair.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value == '':
                continue  # Skip if value is empty
            try:
                value = float(value)
            except ValueError:
                logging.warning(f"Invalid value for {key}: {value}")
                continue
            if key in EXPECTED_RANGES:
                min_val, max_val = EXPECTED_RANGES[key]
                if min_val <= value <= max_val:
                    data[key] = value
                else:
                    logging.warning(f"Value out of range for {key}: {value}")
            else:
                data[key] = value  # Handle unexpected keys
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return data
    except Exception as e:
        logging.error(f"Error parsing sensor data: {e}")
        return None
