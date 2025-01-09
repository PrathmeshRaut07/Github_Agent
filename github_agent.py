from search_repo import search_github_repositories
from fetch_files import add_file
query="Langraph"
contents=[]
repos=search_github_repositories(query)
for repo in repos:
    content=add_file(repo)
    contents.append(content)
print(contents[2])    
