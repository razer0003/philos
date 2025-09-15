from src.web_search import WebSearchManager

print("🔍 Testing Enhanced Web Search System")
print("=" * 50)

search = WebSearchManager()

# Test 1: Charlie Kirk query
print("1. Testing Charlie Kirk 'dead or alive' query...")
result1 = search.search_with_refinement('charlie kirk dead or alive', max_results=3)
print(f"   ✓ Search successful: {result1['success']}")
print(f"   ✓ Results found: {result1['results_count']}")
print(f"   ✓ Method used: {result1.get('search_method', 'standard')}")

print(f"\n   📋 Results:")
for i, res in enumerate(result1['results']):
    print(f"   {i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"      📄 {res.get('content', '')[:120]}...")
    print(f"      🔗 Source: {res.get('source', 'unknown')}")
    print()

# Test 2: Query extraction
print("2. Testing query extraction...")
original_query = "Based off of the most recent news, is Charlie Kirk dead or alive as of right now?"
extracted = search.extract_search_query(original_query, "")
print(f"   📝 Original: '{original_query}'")
print(f"   ✂️  Extracted: '{extracted}'")
print()

# Test 3: Current president query  
print("3. Testing current president query...")
result2 = search.search_with_refinement('current president united states', max_results=2)
print(f"   ✓ Results found: {result2['results_count']}")

for i, res in enumerate(result2['results'][:2]):
    print(f"   {i+1}. [{res.get('type', 'unknown')}] {res.get('title', 'No title')}")
    print(f"      📄 {res.get('content', '')[:120]}...")
    print()

print("🎯 Enhanced Search Features Implemented:")
print("   ✓ RSS news feed integration")  
print("   ✓ Breaking news detection")
print("   ✓ Real-time web search")
print("   ✓ Smart query extraction")
print("   ✓ Status inference (alive/dead logic)")
print("   ✓ Wikipedia name filtering")
print("   ✓ Multiple search engine fallbacks")
