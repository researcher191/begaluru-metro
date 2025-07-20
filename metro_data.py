import pandas as pd
import os

def load_station_data():
    """
    Load Bengaluru metro station data from CSV
    """
    file_path = os.path.join('data', 'bengaluru_metro_stations.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # If file not found, create sample data
        stations = {
            'Station_ID': list(range(1, 51)),
            'Station_Name': [
                'Baiyappanahalli', 'Swami Vivekananda Road', 'Indiranagar', 'Halasuru', 
                'Trinity', 'MG Road', 'Cubbon Park', 'Dr. BR Ambedkar Station', 
                'Vidhana Soudha', 'Sir M. Visvesvaraya Station', 'Majestic', 'City Railway Station',
                'Magadi Road', 'Hosahalli', 'Vijayanagar', 'Attiguppe', 
                'Deepanjali Nagar', 'Mysore Road', 'Nayandahalli', 'Rajarajeshwari Nagar',
                'Jnanabharathi', 'Pattanagere', 'Kengeri', 'Nagasandra', 
                'Dasarahalli', 'Jalahalli', 'Peenya Industry', 'Peenya', 
                'Goraguntepalya', 'Yeshwanthpur', 'Sandal Soap Factory', 'Mahalakshmi',
                'Rajajinagar', 'Kuvempu Road', 'Srirampura', 'Sampige Road',
                'Chickpete', 'Krishna Rajendra Market', 'National College', 'Lalbagh',
                'South End Circle', 'Jayanagar', 'Rashtriya Vidyalaya Road', 'Banashankari',
                'Jayaprakash Nagar', 'Yelachenahalli', 'Konanakunte Cross', 'Doddakallasandra',
                'Vajarahalli', 'Thalaghattapura'
            ],
            'Line': [
                'Purple Line', 'Purple Line', 'Purple Line', 'Purple Line',
                'Purple Line', 'Purple Line', 'Purple Line', 'Purple Line',
                'Purple Line', 'Purple Line', 'Purple Line', 'Purple Line',
                'Purple Line', 'Purple Line', 'Purple Line', 'Purple Line',
                'Purple Line', 'Purple Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line', 'Green Line', 'Green Line',
                'Green Line', 'Green Line'
            ],
            'Latitude': [
                12.9955, 12.9852, 12.9784, 12.9716,
                12.9699, 12.9753, 12.9765, 12.9785,
                12.9813, 12.9846, 12.9766, 12.9783,
                12.9768, 12.9752, 12.9596, 12.9492,
                12.9428, 12.9371, 12.9384, 12.9257,
                12.9174, 12.9148, 12.9076, 13.0844,
                13.0726, 13.0607, 13.0393, 13.0328,
                13.0250, 13.0179, 13.0091, 13.0012,
                12.9909, 12.9859, 12.9841, 12.9815,
                12.9708, 12.9615, 12.9567, 12.9501,
                12.9428, 12.9346, 12.9259, 12.9168,
                12.9074, 12.8999, 12.8912, 12.8823,
                12.8734, 12.8645
            ],
            'Longitude': [
                77.6412, 77.6348, 77.6383, 77.6310,
                77.6227, 77.6194, 77.5893, 77.5857,
                77.5873, 77.5847, 77.5713, 77.5696,
                77.5539, 77.5451, 77.5387, 77.5338,
                77.5294, 77.5229, 77.5291, 77.5196,
                77.5103, 77.5007, 77.4826, 77.5037,
                77.5121, 77.5246, 77.5296, 77.5352,
                77.5403, 77.5459, 77.5544, 77.5636,
                77.5705, 77.5710, 77.5736, 77.5720,
                77.5743, 77.5771, 77.5762, 77.5853,
                77.5878, 77.5908, 77.5837, 77.5763,
                77.5704, 77.5663, 77.5602, 77.5541,
                77.5474, 77.5412
            ]
        }
        
        df = pd.DataFrame(stations)
        os.makedirs('data', exist_ok=True)
        df.to_csv(file_path, index=False)
        return df

def load_connection_data():
    """
    Load Bengaluru metro connection data from CSV
    """
    file_path = os.path.join('data', 'bengaluru_metro_connections.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # If file not found, create sample data
        connections = []
        
        # Purple Line connections
        for i in range(1, 18):
            connections.append({
                'Station_1': i,
                'Station_2': i + 1,
                'Line': 'Purple Line',
                'Distance_KM': 1.2 + (0.2 * (i % 3 - 1))
            })
        
        # Green Line connections
        for i in range(19, 50):
            connections.append({
                'Station_1': i,
                'Station_2': i + 1,
                'Line': 'Green Line',
                'Distance_KM': 1.1 + (0.15 * (i % 4 - 1))
            })
        
        # Connect Purple and Green lines at Majestic (ID: 11 and 36)
        connections.append({
            'Station_1': 11,
            'Station_2': 36,
            'Line': 'Interchange',
            'Distance_KM': 0.2
        })
        
        df = pd.DataFrame(connections)
        os.makedirs('data', exist_ok=True)
        df.to_csv(file_path, index=False)
        return df

def load_passenger_data():
    """
    Load Bengaluru metro passenger data from CSV
    """
    file_path = os.path.join('data', 'passenger_data.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # If file not found, create sample data
        import numpy as np
        
        # Create monthly passenger data for 2019-2023
        years = list(range(2019, 2024))
        months = list(range(1, 13))
        
        data = []
        
        for year in years:
            for month in months:
                # Base passengers with seasonal patterns
                base_passengers = 1000000 + (year - 2019) * 200000
                
                # Add seasonal patterns
                if month in [6, 7, 8]:  # Monsoon season
                    seasonal_factor = 0.9
                elif month in [10, 11, 12]:  # Festival season
                    seasonal_factor = 1.2
                else:
                    seasonal_factor = 1.0
                
                # COVID-19 effect for 2020-2021
                if year == 2020:
                    if month >= 3:  # From March 2020
                        covid_factor = 0.3 if month <= 5 else 0.5
                    else:
                        covid_factor = 1.0
                elif year == 2021:
                    covid_factor = 0.7 if month <= 6 else 0.85
                else:
                    covid_factor = 1.0
                
                # Growth factor
                growth_factor = 1.0 + (year - 2019) * 0.1
                
                # Calculate passengers with some randomness
                passengers = int(base_passengers * seasonal_factor * covid_factor * growth_factor * 
                                 (1 + np.random.uniform(-0.05, 0.05)))
                
                # Purple Line and Green Line allocation
                purple_line_share = 0.6 + np.random.uniform(-0.05, 0.05)
                green_line_share = 1 - purple_line_share
                
                data.append({
                    'Year': year,
                    'Month': month,
                    'Passengers': passengers,
                    'Purple_Line_Passengers': int(passengers * purple_line_share),
                    'Green_Line_Passengers': int(passengers * green_line_share)
                })
        
        df = pd.DataFrame(data)
        os.makedirs('data', exist_ok=True)
        df.to_csv(file_path, index=False)
        return df
