#!/usr/bin/env python3

import requests

def test_current_wikipedia():
    """Test current Wikipedia API to see exact content"""
    
    # Test the Wikipedia API directly
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': 'Charles Darwin'
    }
    
    headers = {
        'User-Agent': 'Philos AI Assistant/1.0 (educational purposes; contact: user@example.com)'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        
        for page_id, page_info in pages.items():
            extract = page_info.get('extract', '')
            if extract:
                print(f"Full Wikipedia extract for Charles Darwin:")
                print(f"First 500 characters:")
                print(extract[:500])
                print(f"\nFirst line:")
                first_line = extract.split('\n')[0] if '\n' in extract else extract
                print(first_line)
                
                # Check for different possible first sentences
                sentences = extract.split('. ')
                print(f"\nFirst sentence:")
                print(sentences[0])
                break
    else:
        print(f"Failed to fetch Wikipedia page: {response.status_code}")

if __name__ == "__main__":
    test_current_wikipedia()
