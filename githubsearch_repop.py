import requests

# GitHub API URL for searching repositories
GITHUB_API_URL = "https://api.github.com/search/repositories"
url=[]
# Function to search GitHub repositories
def search_github_repositories(query, language=None, max_results=3):
    # Set up the search query with optional language filter
    if language:
        query = f"{query} language:{language}"

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

        # Display the search results
        print(f"\nTop {len(repositories)} repositories for query '{query}':\n")
        for i, repo in enumerate(repositories, 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   Description: {repo['description']}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   Forks: {repo['forks_count']}")
            print(f"   Open Issues: {repo['open_issues_count']}")
            print(f"   Last Updated: {repo['updated_at']}")
            print(f"   Owner: {repo['owner']['login']}")
            print(f"   URL: {repo['html_url']}")
            url.append(repo['html_url'])
            print("---------------------------------------------------")
            
    else:
        # If the API request failed, print the error message
        print(f"Error: Unable to fetch data (status code: {response.status_code})")


    # Ask the user for a search query
query = input("Enter your GitHub search query: ")

    # Ask the user for an optional programming language filter
language = input("Filter by programming language (optional, press Enter to skip): ")

    # Ask the user for the number of results to display
max_results = input("How many results do you want to see? (default is 5): ")
max_results = int(max_results) if max_results else 5

    # Perform the search
search_github_repositories(query, language, max_results)
print(url)
from phi.agent import Agent
from phi.llm.google import Gemini
from phi.embedder.ollama import OllamaEmbedder
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.lancedb import LanceDb, SearchType

# Create a knowledge base from a PDF
knowledge_base = WebsiteKnowledgeBase(
    urls=url,
    # Use LanceDB as the vector database
    vector_db=LanceDb(
        table_name="github",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=OllamaEmbedder(model="nomic-embed-text:latest"),
    ),
)
# Comment out after first run as the knowledge base is loaded
knowledge_base.load()

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    # Add the knowledge base to the agent
    knowledge=knowledge_base,
    show_tool_calls=True,
    instructions=[
        "Always search your knowledge base first and use it if available.",
        "Share the page number or source URL of the information you used in your response.",
        "If health benefits are mentioned, include them in the response.",
        "Important: Use tables where possible.",
    ],
    markdown=True,
)
agent.print_response("How do I make chicken and galangal in coconut milk soup", stream=True)