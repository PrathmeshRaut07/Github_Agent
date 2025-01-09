import requests
import base64
from dotenv import load_dotenv
load_dotenv()
import os
# GitHub API URLs
GITHUB_API_URL = "https://api.github.com/search/repositories"
GITHUB_CODE_SEARCH_URL = "https://api.github.com/search/code"
GITHUB_CONTENTS_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# Your GitHub Personal Access Token
GITHUB_TOKEN =os.getenv("GITHUB_ACCESS_TOKEN")  # Replace with your token

# Headers for authenticated requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Function to search GitHub repositories
def search_github_repositories(query, language=None, max_results=5):
    if language:
        query = f"{query} language:{language}"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }

    response = requests.get(GITHUB_API_URL, params=params, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        repositories = data['items']

        print(f"\nTop {len(repositories)} repositories for query '{query}':\n")
        for i, repo in enumerate(repositories, 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   Description: {repo['description']}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   URL: {repo['html_url']}")
            print("---------------------------------------------------")
            
        return repositories
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        return []

# Function to search for code files within repositories
def search_code_in_repositories(repositories, code_query, max_results=5):
    for repo in repositories:
        repo_name = repo['full_name']
        print(f"\nSearching for code in repository: {repo_name}")

        params = {
            "q": f"{code_query} repo:{repo_name}",
            "per_page": max_results
        }

        response = requests.get(GITHUB_CODE_SEARCH_URL, params=params, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            code_results = data['items']

            print(f"\nTop {len(code_results)} code results for query '{code_query}' in repository '{repo_name}':\n")
            for i, code in enumerate(code_results, 1):
                print(f"{i}. File: {code['name']}")
                print(f"   Path: {code['path']}")
                print(f"   URL: {code['html_url']}")
                print("---------------------------------------------------")

                # Fetch and display the content of the code file
                fetch_code_content(repo_name, code['path'])
        else:
            print(f"Error: Unable to fetch data (status code: {response.status_code})")

# Function to fetch and display the content of a code file
def fetch_code_content(repo_name, file_path):
    owner, repo = repo_name.split("/")
    url = GITHUB_CONTENTS_URL.format(owner=owner, repo=repo, path=file_path)

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        if file_data.get("content"):
            # Decode the base64-encoded content
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            print(f"\nContent of file '{file_path}':\n")
            print(content)
            print("---------------------------------------------------")
        else:
            print(f"File '{file_path}' is not a text file or is too large to display.")
    else:
        print(f"Error: Unable to fetch file content (status code: {response.status_code})")

# Main script
if __name__ == "__main__":
    # Ask the user for a search query
    query = "shopping agent"

    # Ask the user for an optional programming language filter
    language = "python"

    # Ask the user for the number of results to display
    max_results =3


    # Perform the repository search
    repositories = search_github_repositories(query, language, max_results)

    # Ask the user for a code search query
    if repositories:
        code_query = input("\nEnter your code search query: ")
        search_code_in_repositories(repositories, code_query, max_results)