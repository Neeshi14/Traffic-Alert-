import requests
import pandas as pd
import time
import random

# Google API Key
API_KEY = "AIzaSyBMI1ndJMecoaZLA5wMYl5eDZXbUOjzjs8"

# List of origin-destination pairs
routes = [
    ("CG Road, Ahmedabad, India", "Gota, Ahmedabad, India"),
    ("SG Highway, Ahmedabad, India", "Naroda, Ahmedabad, India"),
    ("Maninagar, Ahmedabad, India", "Bapunagar, Ahmedabad, India"),
    ("Bopal, Ahmedabad, India", "Chandkheda, Ahmedabad, India"),
    ("Satellite, Ahmedabad, India", "Naranpura, Ahmedabad, India"),
    ("Navrangpura, Ahmedabad, India", "Vastrapur, Ahmedabad, India"),
    ("Paldi, Ahmedabad, India", "Thaltej, Ahmedabad, India"),
    ("Ellis Bridge, Ahmedabad, India", "Iscon, Ahmedabad, India"),
    ("Ashram Road, Ahmedabad, India", "Vasna, Ahmedabad, India"),
    ("Nikol, Ahmedabad, India", "Shahibaug, Ahmedabad, India"),
    ("Gandhigram, Ahmedabad, India", "Memnagar, Ahmedabad, India"),
    ("Kankaria, Ahmedabad, India", "Judges Bungalow, Ahmedabad, India"),
    ("Jodhpur, Ahmedabad, India", "Prahlad Nagar, Ahmedabad, India"),
    ("Narol, Ahmedabad, India", "Motera, Ahmedabad, India"),
    ("Gulbai Tekra, Ahmedabad, India", "Drive-In Road, Ahmedabad, India"),
]

# API Endpoint
url = "https://maps.googleapis.com/maps/api/directions/json"

# CSV File Name
csv_file = "traffic_prediction7.csv"

# Initialize DataFrame
df = pd.DataFrame(columns=[
    "timestamp", "origin", "destination", "distance_km",
    "duration_traffic_min", "duration_normal_min", "congestion_level"
])

# Function to extract duration in minutes from text
def extract_minutes(duration_text):
    if isinstance(duration_text, str) and "min" in duration_text:
        return int(duration_text.split()[0])
    return None

# Collect data continuously
num_rows = 0
max_rows = 10000  # Set the target number of rows

while num_rows < max_rows:
    origin, destination = random.choice(routes)  # Select a random route
   
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "departure_time": "now",
        "traffic_model": "pessimistic",
        "key": API_KEY
    }
   
    response = requests.get(url, params=params)
    data = response.json()
   
    if "routes" in data and len(data["routes"]) > 0:
        route = data["routes"][0]
        leg = route["legs"][0]
       
        duration_traffic_min = extract_minutes(leg.get("duration_in_traffic", {}).get("text"))
        duration_normal_min = extract_minutes(leg.get("duration", {}).get("text"))
        distance_km = float(leg["distance"]["text"].split()[0]) if "distance" in leg else None
        
        # Ensure valid durations
        if duration_traffic_min is not None and duration_normal_min is not None:
            # If API returns a lower traffic duration, swap them
            if duration_traffic_min < duration_normal_min:
                print(f"Warning: Traffic duration ({duration_traffic_min} min) is lower than normal duration ({duration_normal_min} min). Fixing it.")
                duration_traffic_min = duration_normal_min  # Assume best-case scenario
                
            congestion_level = duration_traffic_min / duration_normal_min
            if congestion_level < 1.2:
                congestion_category = "Low"
            elif congestion_level < 1.5:
                congestion_category = "Moderate"
            else:
                congestion_category = "High"
        else:
            congestion_category = "Unknown"

        traffic_data = {
            "timestamp": pd.Timestamp.now(),
            "origin": origin,
            "destination": destination,
            "distance_km": distance_km,
            "duration_traffic_min": duration_traffic_min,
            "duration_normal_min": duration_normal_min,
            "congestion_level": congestion_category
        }

        # Convert dictionary to DataFrame
        new_data = pd.DataFrame([traffic_data])

        # Apply the fix: Only concatenate if new data is valid
        if not new_data.empty:
            df = pd.concat([df, new_data], ignore_index=True)

            # Save to CSV after every 10 rows
            if num_rows % 10 == 0:
                try:
                    df.to_csv(csv_file, index=False)
                except PermissionError:
                    backup_file = "traffic_data_backup.csv"
                    print(f"Permission denied. Saving as {backup_file} instead.")
                    df.to_csv(backup_file, index=False)

            num_rows += 1
            print(f"Collected {num_rows} rows.")

    time.sleep(10)  # Wait 10 seconds before next request

# Final Save
df.to_csv(csv_file, index=False)
print(f"Data collection completed. {num_rows} rows saved in {csv_file}.")
