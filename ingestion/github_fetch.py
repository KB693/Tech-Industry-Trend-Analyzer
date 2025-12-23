import requests
import pandas as pd


GITHUB_TRENDING_API = "https://api.github.com/search/repositories"


def fetch_github_repos(query="machine learning", max_items=50) -> pd.DataFrame:
    """
    Fetch popular GitHub repositories using GitHub Search API.
    """

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_items
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(GITHUB_TRENDING_API, params=params, headers=headers)
    response.raise_for_status()

    items = response.json().get("items", [])

    records = []
    for repo in items:
        records.append({
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "created_at": repo["created_at"],
            "source": "github"
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = fetch_github_repos()
    print(df.head())