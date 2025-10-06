# importing the DDGS class from the duckduckgo_search library
# This library allows us to perform free web searches without needing an API key.
from ddgs import DDGS

def search_web(query: str):
    """
    This function performs a web search using the DuckDuckGo Search API (DDGS).
    I chose this library because:
      - It's free to use.
      - Doesn't require authentication.
      - Returns structured results that are easy to handle.
    """

    # Printing the query to understand what is being searched
    print(f" Searching the web for: '{query}'")

    # Using a context manager to automatically close the connection after the search
    with DDGS() as ddgs:
        # Fetching top 3 results to keep the output short and relevant
        results = [r for r in ddgs.text(query, max_results=3)]

        # Checking if the search returned anything
        if not results:
            return "No results found from the web search."

        # Preparing a clean and readable string to summarize the results
        # Each result shows its title and a short snippet (body text)
        formatted_results = []
        for res in results:
            title = res.get("title", "No Title")
            snippet = res.get("body", "No Description")
            formatted_results.append(f"Title: {title}\nSnippet: {snippet}")

        # Joining all results into one formatted string with spacing between them
        context = "\n\n".join(formatted_results)

        # Returning this text — it can later be used as context for an LLM or summary model
        return context
