import os
import re

# Configuration
TARGET_DIR = "n8n-organized-workflows"

def clean_duplicates():
    print(f"Scanning '{TARGET_DIR}' for duplicates (e.g., file_1.json)...")
    deleted_count = 0
    
    # Regex Explanation:
    # ^(.*?)    : Match the base name (non-greedy)
    # _(\d+)    : Match an underscore followed by digits (the duplicate counter)
    # (\.json)$ : Match the .json extension (case insensitive via flag)
    duplicate_pattern = re.compile(r'^(.*)_(\d+)(\.json)$', re.IGNORECASE)

    for root, dirs, files in os.walk(TARGET_DIR):
        # 1. Map all existing files in this folder (lowercase -> actual name)
        # This allows us to find "File.json" even if we are looking for "file.json"
        files_map = {f.lower(): f for f in files}

        for filename in files:
            # Check if this file looks like a duplicate (e.g., "MyFlow_1.json")
            match = duplicate_pattern.match(filename)
            
            if match:
                base_name = match.group(1)    # "MyFlow"
                # number = match.group(2)     # "1"
                extension = match.group(3)    # ".json"

                # Construct the name of the "Original" file we hope to keep
                expected_original = f"{base_name}{extension}".lower()

                # 2. Check if the Original exists
                if expected_original in files_map:
                    original_actual_name = files_map[expected_original]
                    file_to_remove = os.path.join(root, filename)
                    
                    print(f"Found Duplicate: {filename}")
                    print(f"   -> Keeping:   {original_actual_name}")
                    print(f"   -> Deleting:  {filename}")
                    
                    try:
                        os.remove(file_to_remove)
                        deleted_count += 1
                    except OSError as e:
                        print(f"Error deleting {filename}: {e}")
                    print("-" * 20)

    print("=" * 30)
    print(f"Cleanup Complete.")
    print(f"Total files removed: {deleted_count}")
    print("=" * 30)

if __name__ == "__main__":
    if os.path.exists(TARGET_DIR):
        clean_duplicates()
    else:
        print(f"Error: Directory '{TARGET_DIR}' not found.")