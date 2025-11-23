import os
import shutil
import re
from pathlib import Path

# ================= CONFIGURATION =================
# The text file containing the list of paths
SOURCE_LIST_FILE = "list.text"

# The destination directory for the organized files
TARGET_DIR = "n8n-organized-workflows"

# Keywords to map filenames/foldernames to Categories
# Order matters: specific keywords should be matched before generic ones if needed.
CATEGORY_MAP = {
    "AI & LLMs": [
        "ai", "gpt", "openai", "chatgpt", "llm", "stable-diffusion", "midjourney", 
        "claude", "voice", "transcribe", "whisper", "bot", "chatbot", "vision"
    ],
    "Marketing & Social": [
        "marketing", "email", "facebook", "twitter", "linkedin", "instagram", 
        "social", "seo", "outreach", "newsletter", "campaign", "lead", "ads", 
        "wordpress", "blog", "content", "youtube", "tiktok"
    ],
    "Messaging & Chat": [
        "whatsapp", "telegram", "slack", "discord", "sms", "twilio", "notification", 
        "message", "chat", "waha", "signal"
    ],
    "DevOps & IT": [
        "git", "github", "gitlab", "docker", "kubernetes", "server", "monitor", 
        "uptime", "backup", "aws", "azure", "cloud", "deployment", "webhook", 
        "api", "http", "error", "log"
    ],
    "Productivity & Office": [
        "notion", "google", "drive", "sheets", "docs", "calendar", "todo", 
        "task", "clickup", "trello", "asana", "jira", "airtable", "office", 
        "outlook", "gmail", "schedule", "meeting"
    ],
    "Data & Databases": [
        "sql", "mysql", "postgres", "mongo", "database", "scrape", "extract", 
        "sync", "backup", "json", "csv", "transform", "data"
    ],
    "Finance & Sales": [
        "stripe", "invoice", "payment", "crm", "hubspot", "salesforce", "pipedrive", 
        "crypto", "bitcoin", "currency", "finance", "accounting", "woo"
    ]
}

# Files to ignore (generic assets)
IGNORE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
# Files to definitely include
INCLUDE_EXTENSIONS = ['.json'] 

# ================= LOGIC =================

def normalize_name(name):
    """Converts 'My Workflow Name' to 'my-workflow-name'"""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')

def get_category(name):
    """Determines category based on the name string."""
    name_lower = name.lower()
    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category
    return "Uncategorized"

def get_smart_name(filepath):
    """
    Returns a tuple (New_Filename, Category_Source_Name).
    If filename is 'template.json', it uses the parent folder name.
    """
    path_obj = Path(filepath)
    filename = path_obj.name
    parent_folder = path_obj.parent.name

    # List of generic names that carry no meaning
    generic_names = ["template.json", "workflow.json", "data.json", "backup.json"]

    if filename.lower() in generic_names:
        # Use the folder name as the new filename
        # e.g., .../whatsapp-typebot/template.json -> whatsapp-typebot.json
        base_name = parent_folder
    else:
        # Use the actual filename, but strip extension for categorization check
        base_name = path_obj.stem

    # Determine category based on this meaningful name
    category = get_category(base_name)
    
    # Reconstruct filename with extension
    final_filename = f"{base_name}{path_obj.suffix}"
    
    return final_filename, category

def main():
    # 1. verify source exists
    if not os.path.exists(SOURCE_LIST_FILE):
        print(f"Error: {SOURCE_LIST_FILE} not found.")
        return

    print(f"Reading from {SOURCE_LIST_FILE}...")
    
    count = 0
    errors = 0
    
    with open(SOURCE_LIST_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Found {len(lines)} paths. Processing...")

    for line in lines:
        original_path = line.strip()
        if not original_path:
            continue
            
        # Only process desired extensions (primarily JSON)
        if not any(original_path.endswith(ext) for ext in INCLUDE_EXTENSIONS):
            continue

        # Handle cases where the file might not exist locally (broken paths in list.text)
        if not os.path.exists(original_path):
            # print(f"Skipping missing file: {original_path}")
            continue

        try:
            # Determine new name and category
            new_filename, category = get_smart_name(original_path)
            
            # Create destination folder
            category_path = os.path.join(TARGET_DIR, category)
            os.makedirs(category_path, exist_ok=True)
            
            # Handle Duplicate Filenames
            destination_file = os.path.join(category_path, new_filename)
            
            # If file exists, append a counter: whatsapp-bot_1.json
            dup_count = 1
            base_stem = Path(new_filename).stem
            base_ext = Path(new_filename).suffix
            
            while os.path.exists(destination_file):
                destination_file = os.path.join(
                    category_path, 
                    f"{base_stem}_{dup_count}{base_ext}"
                )
                dup_count += 1

            # Copy the file
            shutil.copy2(original_path, destination_file)
            count += 1
            
            # Optional: Print progress every 50 files
            if count % 50 == 0:
                print(f"Processed {count} files...")

        except Exception as e:
            print(f"Error processing {original_path}: {e}")
            errors += 1

    print("-" * 30)
    print("PROCESSING COMPLETE")
    print("-" * 30)
    print(f"Total Workflows Organized: {count}")
    print(f"Errors: {errors}")
    print(f"Files located in: {os.path.abspath(TARGET_DIR)}")

if __name__ == "__main__":
    main()