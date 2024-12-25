import requests

def search_google(query):
    # Replace with actual Google API call
    return [{"title": "Example Result", "link": "https://example.com"}]

def search_wikipedia(query):
    # Replace with actual Wikipedia API call
    return [{"title": "Wikipedia Result", "link": "https://wikipedia.org"}]

def display_results(results):
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']}")
        print(f"   Link: {result['link']}\n")

def main():
    print("Welcome to the CLI Search Aggregator!")
    query = input("Enter your search query: ")
    source = input("Choose a source (google, wikipedia): ").lower()

    if source == "google":
        results = search_google(query)
    elif source == "wikipedia":
        results = search_wikipedia(query)
    else:
        print("Invalid source!")
        return

    display_results(results)

if __name__ == "__main__":
    main()
