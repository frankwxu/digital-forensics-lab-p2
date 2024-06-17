import sqlite3
import json

def get_participants_by_message_id(db_path, message_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Debug: Check if the 'messages' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages';")
        if cursor.fetchone() is None:
            return "Error: 'messages' table does not exist."
        
        # Debug: Check if the 'threads' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='threads';")
        if cursor.fetchone() is None:
            return "Error: 'threads' table does not exist."
        
        # Step 1: Get the thread_id for the given message_id
        cursor.execute("SELECT thread_id FROM messages WHERE message_id = ?", (message_id,))
        result = cursor.fetchone()
        if result is None:
            return f"No thread found for message_id: {message_id}"
        thread_id = result[0]
        
        # Step 2: Get the metadata for the thread_id
        cursor.execute("SELECT metadata FROM threads WHERE thread_id = ?", (thread_id,))
        result = cursor.fetchone()
        if result is None:
            return f"No metadata found for thread_id: {thread_id}"
        metadata_blob = result[0]
        
        # Attempt to process the metadata blob
        try:
            metadata_str = metadata_blob.decode('utf-8', errors='ignore')  # Decode with ignore errors
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            return "Failed to decode metadata as JSON"
        except Exception as e:
            return f"An error occurred while processing metadata: {e}"
        
        # Extract participants from the metadata
        participants = metadata.get('participants', [])
        
        # Return the list of participants
        return participants
    
    except Exception as e:
        return f"An error occurred: {e}"
    
    finally:
        # Close the connection
        conn.close()

# Example usage
db_path = '45925726866.db'  # Replace with the path to your SQLite database
message_id = '30011074970704624296208122920304640'
participants = get_participants_by_message_id(db_path, message_id)
print(participants)
