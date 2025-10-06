import arxiv

def search_arxiv(query: str):
    """
    Searches the ArXiv database for academic papers.
    """
    print(f"-> Searching ArXiv for: '{query}'")
    try:
        # Search for the top 2 most relevant papers.
        search = arxiv.Search(
            query=query,
            max_results=2,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(search.results())
        if not results:
            return "No academic papers found on ArXiv for this topic."

        # Formatting the results with title and a short summary.
        # Truncating the summary to keep the context manageable.
        context = "\n\n".join(
            [f"Paper Title: {result.title}\nSummary: {result.summary[:500]}..." for result in results]
        )
        return context
    except Exception as e:
        # Added a simple try-except block to handle potential API errors.
        print(f"Error searching ArXiv: {e}")
        return "There was an error searching ArXiv."