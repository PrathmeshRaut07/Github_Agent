import requests
import base64
import os

# GitHub API URL for repository contents
GITHUB_CONTENTS_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# Your GitHub Personal Access Token
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")  # Replace with your token

# Headers for authenticated requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Function to recursively fetch all files in a repository
def fetch_all_files(repo_name, path=""):
    owner, repo = repo_name.split("/")
    url = GITHUB_CONTENTS_URL.format(owner=owner, repo=repo, path=path)

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        contents = response.json()
        files = []

        for item in contents:
            if item["type"] == "file":
                # Skip binary files (e.g., images)
                if item["name"].endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.pdf', '.zip', '.exe', '.dll')):
                    print(f"Skipping binary file: {item['name']}")
                    continue
                
                # If it's a file, add it to the list
                files.append({
                    "name": item["name"],
                    "path": item["path"],
                    "url": item["html_url"],
                    "content": fetch_file_content(item["url"])  # Fetch file content
                })
            elif item["type"] == "dir":
                # If it's a directory, recursively fetch its contents
                files.extend(fetch_all_files(repo_name, item["path"]))

        return files
    else:
        print(f"Error: Unable to fetch contents (status code: {response.status_code})")
        return []

# Function to fetch the content of a file
def fetch_file_content(file_url):
    response = requests.get(file_url, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        if file_data.get("content"):
            try:
                # Decode the base64-encoded content
                return base64.b64decode(file_data["content"]).decode("utf-8")
            except UnicodeDecodeError:
                return "File content not available (binary or non-UTF-8 file)."
        else:
            return "File content not available (may be a binary file)."
    else:
        return f"Error: Unable to fetch file content (status code: {response.status_code})"

from urllib.parse import urlparse

def extract_repo_info(github_url):
    # Parse the URL
    parsed_url = urlparse(github_url)
    
    # Split the path to get the parts
    path_parts = parsed_url.path.strip('/').split('/')
    
    # Ensure the URL has both the username and repository name
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1]}"
    else:
        return None
def add_file(repo):
    print(repo)
    repo_name=extract_repo_info(repo)
    print(repo_name)
    files = fetch_all_files(repo_name)
    
    # Initialize an empty string to hold the concatenated content
    all_content = ""

    for file in files:
        # print(f"File: {file['name']}")
        # print(f"Path: {file['path']}")
        # print(f"URL: {file['url']}")
        # print("Content:")
        # print(file["content"])
        # print("---------------------------------------------------")
        
        # Append the content of the current file to the all_content variable
        all_content += file["content"] + "\n"  # Adding a newline for separation

    # Now all_content contains the concatenated content of all files
    return all_content

