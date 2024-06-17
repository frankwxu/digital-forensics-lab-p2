import os
import hashlib

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def search_files_by_md5(directory, target_md5):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            if md5 == target_md5:
                print("\nFile found at:", file_path)
                print("MD5 Hash:", md5)

# Prompt user for input
directory_to_search = input("Enter the directory to search: ")
target_md5_to_search = input("Enter the target MD5 hash: ")

search_files_by_md5(directory_to_search, target_md5_to_search)
