import requests
import pandas as pd
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"


def fetch_arxiv_papers(
    search_query="cat:cs.AI",
    max_results=50
) -> pd.DataFrame:
    """
    Fetch papers from arXiv API.

    Returns:
        DataFrame with title, summary, published date, and category.
    """

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(ARXIV_API_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    records = []

    for entry in root.findall("atom:entry", ns):
        records.append({
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip(),
            "published": entry.find("atom:published", ns).text,
            "source": "arxiv"
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = fetch_arxiv_papers()
    print(df.head())