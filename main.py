import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def search_google(query, api_key=GOOGLE_API_KEY, cse_id=GOOGLE_CSE_ID, max_results=5):
    """
    Search Google for a given query using the Custom Search API.

    Args:
        query (str): The search term.
        api_key (str): Your Google API key.
        cse_id (str): Your Custom Search Engine ID.
        max_results (int): Maximum number of results to return.

    Returns:
        list: A list of dictionaries with title, snippet, and link for each result.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": max_results,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append({
                "title": item["title"],
                "snippet": item["snippet"],
                "link": item["link"],
            })

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []

def search_wikipedia(query, max_results=5):
    """
    Search Wikipedia for a given query.
    
    Args:
        query (str): The search term.
        max_results (int): Maximum number of results to return.

    Returns:
        list: A list of dictionaries with title and link for each result.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data["query"]["search"][:max_results]:
            title = item["title"]
            link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            results.append({"title": title, "link": link})

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []

def display_results(results):
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']}")
        print(f"   {result['snippet']}")
        print(f"   Link: {result['link']}\n")

def main():
    print("Welcome to the CLI Search Aggregator!")
    query = input("Enter your search query: ")
    print("Choose sources: [google, wikipedia] (separate by commas)")
    sources = input("Sources: ").lower().split(",")

    aggregated_results = []

    if "google" in sources:
        google_results = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
        aggregated_results.extend(google_results)

    if "wikipedia" in sources:
        wikipedia_results = search_wikipedia(query)
        aggregated_results.extend(wikipedia_results)

    if aggregated_results:
        print("\nAggregated Results:")
        display_results(aggregated_results)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
