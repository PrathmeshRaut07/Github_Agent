# github_search.py

import requests

# GitHub API URL for searching repositories
GITHUB_API_URL = "https://api.github.com/search/repositories"

# Function to search GitHub repositories
def search_github_repositories(query, language=None, max_results=5):
    # Set up the search query with optional language filter
    if language:
        query = f"{query} language:{language}"
    urls = []
    # Parameters for the API request
    params = {
        "q": query,
        "sort": "stars",  # Sort by stars (you can change this to 'forks', 'updated', etc.)
        "order": "desc",  # Order by descending (most stars first)
        "per_page": max_results  # Limit the number of results
    }

    # Make the API request to GitHub
    response = requests.get(GITHUB_API_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        repositories = data['items']

        # Collect the URLs of the repositories
        for repo in repositories:
            urls.append(repo['html_url'])
        return urls