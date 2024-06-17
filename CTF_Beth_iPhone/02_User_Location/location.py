import sqlite3
from geopy.geocoders import Nominatim

def extract_location_name(db_file, target_unix_timestamp):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to extract location based on the given UNIX timestamp
    query = """
    SELECT ZLOCATIONLATITUDE, ZLOCATIONLONGITUDE
    FROM ZRTLEARNEDLOCATIONOFINTERESTVISITMO
    WHERE ? BETWEEN ZENTRYDATE AND ZEXITDATE
    """

    cursor.execute(query, (target_unix_timestamp,))
    location_data = cursor.fetchone()

    if location_data:
        latitude, longitude = location_data
        location = get_location_name(latitude, longitude)
        print(f"Location Name: {location}")
    else:
        print("No location data found for the given timestamp.")

    conn.close()

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="location_explorer")
    location = geolocator.reverse((latitude, longitude))
    return location.address if location else "Unknown"

if __name__ == "__main__":
    db_file = "Local.sqlite"
    
    # Prompt the user to enter the UNIX timestamp
    unix_timestamp_input = input("Enter the UNIX timestamp: ")

    # Validate and use the user input
    try:
        target_unix_timestamp = float(unix_timestamp_input)
    except ValueError:
        print("Invalid UNIX timestamp.")
    else:
        extract_location_name(db_file, target_unix_timestamp)
