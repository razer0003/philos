#!/usr/bin/env python3
"""
Test Wikipedia API directly to see if it's working
"""

import requests

def test_wikipedia_api():
    """Test Wikipedia API for Charles Darwin"""
    
    print("Testing Wikipedia API for 'Charles Darwin'...")
    
    # Wikipedia API search
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': 'Charles Darwin',
        'srlimit': 3
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Searching Wikipedia...")
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('query', {}).get('search', [])
            print(f"Found {len(results)} search results:")
            
            for item in results:
                title = item['title']
                print(f"- {title}")
                
                # Get page content for the first result
                if title.lower() == 'charles darwin':
                    print(f"\nGetting content for: {title}")
                    
                    page_url = "https://en.wikipedia.org/w/api.php"
                    page_params = {
                        'action': 'query',
                        'format': 'json',
                        'prop': 'extracts',
                        'exintro': True,
                        'explaintext': True,
                        'titles': title
                    }
                    
                    page_response = requests.get(page_url, params=page_params, headers=headers, timeout=10)
                    if page_response.status_code == 200:
                        page_data = page_response.json()
                        pages = page_data.get('query', {}).get('pages', {})
                        
                        for page_id, page_info in pages.items():
                            extract = page_info.get('extract', '')
                            if extract:
                                # Get first line
                                first_line = extract.split('\n')[0]
                                print(f"First line: {first_line}")
                                print(f"Full extract length: {len(extract)} chars")
                                print(f"First 200 chars: {extract[:200]}...")
                                return True
                    else:
                        print(f"Failed to get page content: {page_response.status_code}")
        else:
            print(f"Search failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return False

if __name__ == "__main__":
    test_wikipedia_api()
