import sys
import os
import unittest
from unittest.mock import patch

# --- Path Configuration for Tests ---
# This block allows the tests to find the modules in the 'backend' and 'agents' directories
# when run from the project root (e.g., 'python tests/test_agents.py').
# It temporarily adds the project root to the Python path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now, import the agent functions
from agents.web_search import search_web
from agents.arxiv import search_arxiv
# Note: PDF RAG agent is harder to unit test without a real file or complex mocking.
# For this project, testing web_search and arxiv demonstrates the concept.

class TestSpecialistAgents(unittest.TestCase):

    # --- Test for Web Search Agent ---
    def test_web_search_returns_string(self):
        """
        Tests that the web search agent returns a non-empty string for a valid query.
        This confirms basic functionality and expected output type.
        """
        print("\nRunning test: test_web_search_returns_string")
        # Use a simple, non-controversial query
        result = search_web("latest AI news summary")
        
        # Assertions
        self.assertIsInstance(result, str, "Web search result should be a string.")
        self.assertTrue(len(result) > 0, "Web search result should not be empty.")
        print(f"  Web Search Test Passed: Result length {len(result)} characters.")

    # --- Test for ArXiv Agent ---
    def test_arxiv_search_returns_string(self):
        """
        Tests that the arXiv agent returns a non-empty string for a valid query.
        This confirms basic functionality and expected output type.
        """
        print("\nRunning test: test_arxiv_search_returns_string")
        # Use a simple, broad academic query
        result = search_arxiv("large language models")
        
        # Assertions
        self.assertIsInstance(result, str, "ArXiv search result should be a string.")
        self.assertTrue(len(result) > 0, "ArXiv search result should not be empty.")
        print(f"  ArXiv Search Test Passed: Result length {len(result)} characters.")

    # You could add more tests here, e.g., for specific content in results (more complex),
    # or error handling (e.g., what if the external API fails).

# This allows you to run the tests directly from the command line:
# python tests/test_agents.py
if __name__ == '__main__':
    unittest.main()