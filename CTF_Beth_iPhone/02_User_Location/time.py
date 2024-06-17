import sqlite3
from datetime import datetime, timedelta

# Function to try to convert BLOB to text if it's not already text
def blob_to_text(blob):
    try:
        return blob.decode('utf-8')
    except AttributeError:
        return str(blob)

# Function to get user input for the date
def get_user_date():
    date_str = input("Enter the date (YYYY-MM-DD): ")
    try:
        user_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        return get_user_date()
    return user_date

# Function to get user input for the contact address
def get_user_address():
    address = input("Enter the contact address: ")
    return address

# Connect to the SQLite database
conn = sqlite3.connect('CallHistory.storedata')
cursor = conn.cursor()

# Define the query to select ZDATE and ZADDRESS columns
query = """
SELECT ZDATE, ZADDRESS
FROM ZCALLRECORD
"""

# Execute the query
cursor.execute(query)
rows = cursor.fetchall()

# Define the reference date for the timestamps
reference_date = datetime(2001, 1, 1)  # Mac Absolute Time reference

# Get the date and contact address from the user
user_date = get_user_date()
user_address = get_user_address()

# Process and print the results
for row in rows:
    zdate = row[0]
    zaddress_blob = row[1]
    
    # Convert ZADDRESS BLOB to text if necessary
    zaddress = blob_to_text(zaddress_blob)
    
    call_date = reference_date + timedelta(seconds=zdate)

    if call_date.date() == user_date and zaddress == user_address:
        print(f"Call made to {zaddress} on {call_date.strftime('%Y-%m-%d at %H:%M:%S')}")
        print(f"UNIX Timestamp: {zdate}")
        print(f"Actual Date-Time: {call_date}")

# Close the connection
conn.close()
