from src.web_search import WebSearchManager

search = WebSearchManager()

print("Testing Charlie Kirk query with enhanced status inference...")
result = search.search_with_refinement('charlie kirk dead or alive', max_results=3, deep_search=True)

print(f"Results found: {result['results_count']}")
print(f"Search method: {result.get('search_method', 'standard')}")

for i, res in enumerate(result['results']):
    print(f"\n{i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"   Content: {res.get('content', '')[:200]}...")
    print(f"   Source: {res.get('source', 'unknown')}")

# Test query extraction too
print(f"\nQuery extraction test:")
extracted = search.extract_search_query("Based off of the most recent news, is Charlie Kirk dead or alive as of right now?", "")
print(f"Extracted: '{extracted}'")
