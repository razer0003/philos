from src.web_search import WebSearchManager

search = WebSearchManager()

# Test the Charlie Kirk query with new RSS and breaking news search
print("Testing enhanced news search for 'charlie kirk dead or alive'...")
result = search._search_news_feeds('charlie kirk dead or alive', 3)

print(f"RSS/News results found: {len(result['results'])}")
for i, res in enumerate(result['results']):
    print(f"{i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"   Content: {res.get('content', '')[:100]}...")
    print(f"   Source: {res.get('source', 'unknown')}")
    if res.get('published'):
        print(f"   Published: {res.get('published')}")
    print()

# Test breaking news search specifically
print("\nTesting breaking news search for 'charlie kirk dead or alive'...")
breaking_result = search._search_breaking_news('charlie kirk dead or alive')

print(f"Breaking news results found: {len(breaking_result['results'])}")
for i, res in enumerate(breaking_result['results']):
    print(f"{i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"   Content: {res.get('content', '')[:100]}...")
    print(f"   Source: {res.get('source', 'unknown')}")
    print()

# Test full search with refinement
print("\nTesting full search with refinement...")
full_result = search.search_with_refinement('charlie kirk dead or alive', max_results=5, deep_search=True)

print(f"Full search successful: {full_result['success']}")
print(f"Total results: {full_result['results_count']}")
print(f"Search method: {full_result.get('search_method', 'standard')}")
if full_result.get('refined_query'):
    print(f"Used refined query: {full_result['refined_query']}")

for i, res in enumerate(full_result['results'][:3]):
    print(f"{i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"   Content: {res.get('content', '')[:100]}...")
    print(f"   Source: {res.get('source', 'unknown')}")
    print()
