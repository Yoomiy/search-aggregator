import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def search_google(query, api_key, cse_id, max_results=5):
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
        if 'snippet' in result:
            print(f"   {result['snippet']}")
        print(f"   Link: {result['link']}")
        print(f"   Source: {result['source']}\n")

def duplicate_results(results):
    seen = set()
    unique_results = []
    for result in results:
        if result['link'] not in seen:
            seen.add(result['link'])
            unique_results.append(result)
    return unique_results
            
def main():
    print("Welcome to the CLI Search Aggregator!")
    query = input("Enter your search query: ")
    print("Choose sources: [google, wikipedia] (separate by commas)")
    sources = [source.strip() for source in input("Sources: ").lower().split(",")]

    aggregated_results = []

    if "google" in sources:
        google_results = search_google(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
        for result in google_results:
            result["source"] = "google"
        aggregated_results.extend(google_results)

    if "wikipedia" in sources:
        wikipedia_results = search_wikipedia(query)
        for result in wikipedia_results:
            result["source"] = "wikipedia"
        aggregated_results.extend(wikipedia_results)

    if aggregated_results:
        aggregated_results = duplicate_results(aggregated_results)
        print("\nAggregated Results:")
        display_results(aggregated_results)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
