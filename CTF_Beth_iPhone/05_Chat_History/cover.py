import sqlite3
import json
import biplist
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Function to decode BLOBs if necessary
def decode_blob(blob):
    try:
        return blob.decode('utf-8')
    except Exception:
        try:
            plist = biplist.readPlistFromString(blob)
            return plist
        except Exception:
            return str(blob)

# Connect to the SQLite database
conn = sqlite3.connect('45925726866.db')
cursor = conn.cursor()

# Fetch all threads
cursor.execute("SELECT * FROM threads")
threads_data = cursor.fetchall()

# Fetch all messages
cursor.execute("SELECT * FROM messages")
messages_data = cursor.fetchall()

# Close the database connection
conn.close()

# Parse threads into a dictionary
threads_dict = {}
for thread in threads_data:
    thread_id, thread_id_v2, viewer_id, metadata, thread_messages_range, visual_message_info, row_id = thread
    threads_dict[thread_id] = {
        "thread_id": thread_id,
        "thread_id_v2": thread_id_v2,
        "viewer_id": viewer_id,
        "metadata": decode_blob(metadata),
        "thread_messages_range": decode_blob(thread_messages_range),
        "visual_message_info": decode_blob(visual_message_info),
        "messages": []
    }

# Parse messages and associate them with threads
for message in messages_data:
    message_id, thread_id, archive, class_name, row_id = message
    message_dict = {
        "message_id": message_id,
        "archive": decode_blob(archive),
        "class_name": class_name,
        "row_id": row_id
    }
    if thread_id in threads_dict:
        threads_dict[thread_id]["messages"].append(message_dict)
    else:
        # Handle the case where the message's thread_id is not found in threads
        threads_dict[thread_id] = {
            "thread_id": thread_id,
            "messages": [message_dict]
        }

# Convert the threads dictionary to a JSON structure
threads_json = json.dumps(threads_dict, indent=4, default=str)

# Save the JSON to a file
with open('instagram_threads.json', 'w') as json_file:
    json_file.write(threads_json)

# Print the JSON structure (optional)
print(threads_json)
