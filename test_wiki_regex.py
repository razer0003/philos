#!/usr/bin/env python3
"""
Quick test for Wikipedia query extraction
"""
import re

def test_wiki_extraction():
    test_input = "can you search up the wikipedia page for charles darwin and tell me what the first line is?"
    
    print(f"Testing: {test_input}")
    
    if 'wikipedia' in test_input.lower():
        # Extract the subject name for wikipedia
        wiki_match = re.search(r'wikipedia.*?for\s+([a-zA-Z\s]+?)(?:\s+and\s|\s+tell\s|\s+what\s|$)', test_input.lower())
        if wiki_match:
            subject = wiki_match.group(1).strip()
            print(f"Raw match: '{subject}'")
            
            # Capitalize properly for names
            subject_words = []
            for word in subject.split():
                if len(word) > 2:  # Capitalize longer words (names)
                    subject_words.append(word.capitalize())
                else:
                    subject_words.append(word.lower())
            subject = ' '.join(subject_words)
            result = f"{subject} Wikipedia"
            print(f"Final result: '{result}'")
        else:
            print("No match found")
    else:
        print("No wikipedia keyword found")

if __name__ == "__main__":
    test_wiki_extraction()
