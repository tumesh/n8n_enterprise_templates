import os
import json
import hashlib
import shutil
import subprocess
from pathlib import Path

# Configuration
TARGET_DIR = "n8n-unified-templates"
STAGING_DIR = os.path.join(TARGET_DIR, "workflows_staging")
TEMP_DIR = "temp_repos"

# The Source List provided
REPOS = [
    "https://github.com/Salheen10/n8n-free-automation-templates-5000.git",
    "https://github.com/jz-clln/150-n8n-templates.git",
    "https://github.com/Danitilahun/n8n-workflow-templates.git",
    "https://github.com/devlikeapro/waha-n8n-templates.git",
    "https://github.com/creativetimofficial/free-n8n-workflow-templates-collection.git",
    "https://github.com/ritik-prog/n8n-automation-templates-5000.git",
    "https://github.com/lucaswalter/n8n-ai-automations.git",
    "https://github.com/Marvomatic/n8n-templates.git",
    "https://github.com/wassupjay/n8n-free-templates.git",
    "https://github.com/enescingoz/awesome-n8n-templates.git"
]

# Keywords for auto-categorization
CATEGORIES = {
    "marketing": ["marketing", "email", "social", "facebook", "twitter", "linkedin", "seo"],
    "devops": ["docker", "server", "monitor", "aws", "azure", "git", "cicd"],
    "ai": ["openai", "gpt", "chatgpt", "ai", "llm", "stable diffusion"],
    "productivity": ["notion", "slack", "telegram", "todo", "calendar", "schedule"],
    "finance": ["crypto", "stripe", "invoice", "payment", "bitcoin"],
    "databases": ["mysql", "postgres", "mongodb", "sql"]
}

def calculate_hash(file_path):
    """Generate MD5 hash to detect duplicate file contents."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def setup_dirs():
    if not os.path.exists(STAGING_DIR):
        os.makedirs(STAGING_DIR)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def clone_repos():
    print("--- Cloning Repositories ---")
    
    # FIX: Define the full path to git.exe if Python can't find it automatically
    # Common default: r"C:\Program Files\Git\cmd\git.exe"
    # If "git" works in your terminal, you can leave this as just "git"
    # If it fails, replace "git" below with r"C:\Path\To\Your\git.exe"
    GIT_COMMAND = "git" 

    # Verify git exists before running
    if shutil.which(GIT_COMMAND) is None:
        # Fallback: Try to find it in default Windows location
        default_path = r"C:\Program Files\Git\cmd\git.exe"
        if os.path.exists(default_path):
            GIT_COMMAND = default_path
        else:
            print("ERROR: Git is not found on your system or PATH.")
            print("Please install Git or update the GIT_COMMAND variable in the script.")
            return

    for repo in REPOS:
        repo_name = repo.split("/")[-1].replace(".git", "")
        dest = os.path.join(TEMP_DIR, repo_name)
        if not os.path.exists(dest):
            print(f"Cloning {repo_name}...")
            try:
                # We use shell=True for Windows compatibility if PATH is tricky, 
                # but explicit pathing (above) is safer.
                subprocess.run([GIT_COMMAND, "clone", repo, dest], check=True)
            except Exception as e:
                print(f"Failed to clone {repo_name}: {e}")
        else:
            print(f"Skipping {repo_name} (already exists)")

def process_templates():
    print("\n--- Processing and Merging Templates ---")
    seen_hashes = set()
    count = 0
    duplicates = 0

    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            if file.endswith(".json"):
                src_path = os.path.join(root, file)
                
                # 1. Validate if it's likely an n8n file
                try:
                    with open(src_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        # n8n workflows usually have a "nodes" key
                        if "nodes" not in content and "connections" not in content:
                            continue 
                except:
                    continue # Skip invalid JSON

                # 2. Deduplicate
                file_hash = calculate_hash(src_path)
                if file_hash in seen_hashes:
                    duplicates += 1
                    continue
                seen_hashes.add(file_hash)

                # 3. Categorize based on filename
                category = "uncategorized"
                filename_lower = file.lower()
                for cat, keywords in CATEGORIES.items():
                    if any(k in filename_lower for k in keywords):
                        category = cat
                        break
                
                # 4. Move to Staging
                dest_folder = os.path.join(STAGING_DIR, category)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                # Handle filename collisions
                final_name = file
                if os.path.exists(os.path.join(dest_folder, final_name)):
                    final_name = f"{count}_{file}"
                
                shutil.copy2(src_path, os.path.join(dest_folder, final_name))
                count += 1

    print(f"\nDONE! Processed {count} unique templates.")
    print(f"Skipped {duplicates} duplicates.")
    print(f"Templates are located in: {STAGING_DIR}")

if __name__ == "__main__":
    setup_dirs()
    clone_repos()
    process_templates()
    # Cleanup of temp dir can be added here if desired