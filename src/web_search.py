import requests
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import re
from urllib.parse import urlencode, quote_plus, urlparse
import time

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

class WebSearchManager:
    def __init__(self, status_callback: Optional[Callable[[str], None]] = None, openai_client=None):
        self.logger = logging.getLogger(__name__)
        self.status_callback = status_callback  # Callback for live updates
        self.openai_client = openai_client  # OpenAI client for query restructuring
        self.browser_activity_window = None  # Reference to browser activity window
        
        # User agent to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Rate limiting
        self.last_search_time = 0
        self.min_search_interval = 1.0  # Minimum seconds between searches
        
        # News sources for real-time information
        self.news_feeds = [
            'https://feeds.bbci.co.uk/news/rss.xml',
            'https://rss.cnn.com/rss/edition.rss',
            'https://feeds.reuters.com/reuters/topNews'
        ]
        
        # Track recent searches for contextual follow-ups
        self.last_search_query = None
        self.last_search_results = None
        self.last_search_time = None
    
    def _update_status(self, message: str):
        """Send status update to callback if available"""
        if self.status_callback:
            self.status_callback(message)
        if self.browser_activity_window:
            self.browser_activity_window.update_search_status(message)
        self.logger.info(f"Search Status: {message}")
        
    def set_browser_activity_window(self, window):
        """Set reference to browser activity window for detailed logging"""
        self.browser_activity_window = window
        
    def _notify_source_access(self, source_type: str, url: str, description: str):
        """Notify browser activity window about source access"""
        if self.browser_activity_window:
            self.browser_activity_window.add_source_accessed(source_type, url, description)
            
    def _notify_result_found(self, result: dict):
        """Notify browser activity window about a search result"""
        if self.browser_activity_window:
            self.browser_activity_window.add_search_result(result)
            
    def _notify_ai_decision(self, decision_type: str, decision: str, reasoning: str = ""):
        """Notify browser activity window about AI decisions"""
        if self.browser_activity_window:
            self.browser_activity_window.add_ai_decision(decision_type, decision, reasoning)
    
    def clear_search_cache(self):
        """Clear the search cache to prevent cross-conversation contamination"""
        self.last_search_query = None
        self.last_search_results = None
        self.last_search_time = None
        self.logger.info("Search cache cleared")
        
    def search_web(self, query: str, max_results: int = 5, deep_search: bool = False) -> Dict[str, Any]:
        """
        Perform comprehensive web search with live updates
        Returns search results with summaries and full content when requested
        """
        try:
            self._update_status(f"Starting search for '{query}'...")
            
            # Rate limiting
            current_time = time.time()
            if self.last_search_time is not None:
                time_since_last = current_time - self.last_search_time
                if time_since_last < self.min_search_interval:
                    time.sleep(self.min_search_interval - time_since_last)
            
            all_results = []
            
            # 1. Try DuckDuckGo instant answers first
            self._update_status("Checking for instant answers...")
            ddg_results = self._search_duckduckgo(query, max_results)
            if ddg_results['results']:
                all_results.extend(ddg_results['results'])
                self._update_status(f"Found {len(ddg_results['results'])} instant answers")
            
            # 2. Search Wikipedia for comprehensive information
            self._update_status("Searching Wikipedia...")
            wiki_results = self._search_wikipedia_api(query)
            if wiki_results['results']:
                all_results.extend(wiki_results['results'])
                self._update_status(f"Found {len(wiki_results['results'])} Wikipedia articles")
            
            # 3. Check news feeds for current events if query seems time-sensitive
            if self._is_current_events_query(query):
                self._update_status("Checking current news...")
                news_results = self._search_news_feeds(query, 3)
                if news_results['results']:
                    all_results.extend(news_results['results'])
                    self._update_status(f"Found {len(news_results['results'])} recent news items")
                
                # 3.5 Check for breaking news if it's a death/alive query
                if any(word in query.lower() for word in ['dead', 'alive', 'died', 'death']):
                    self._update_status("Checking for breaking news announcements...")
                    breaking_results = self._search_breaking_news(query)
                    if breaking_results['results']:
                        all_results.extend(breaking_results['results'])
                        self._update_status(f"Found {len(breaking_results['results'])} breaking news items")
                
                # 3b. For political queries, try specific current search
                if any(word in query.lower() for word in ['president', 'prime minister', 'leader']):
                    self._update_status("Searching for current political information...")
                    political_results = self._search_current_politics(query)
                    if political_results['results']:
                        all_results.extend(political_results['results'])
                        self._update_status(f"Found {len(political_results['results'])} current political updates")
                    
                    # Political searches handled by other methods above
            
            # 3.5. Search Reddit for community discussions and opinions
            self._update_status("Searching Reddit for community insights...")
            reddit_results = self._search_reddit(query, 3)  # Get more Reddit results for death queries
            if reddit_results['results']:
                all_results.extend(reddit_results['results'])
                self._update_status(f"Found {len(reddit_results['results'])} Reddit discussions")
            
            # 3.6. Search Quora for Q&A content  
            self._update_status("Searching Quora for questions and answers...")
            quora_results = self._search_quora(query, 2)
            if quora_results['results']:
                all_results.extend(quora_results['results'])
                self._update_status(f"Found {len(quora_results['results'])} Quora answers")
            
            # 3.7. Use AI to generate better search queries and determine additional search strategies
            if len(all_results) < 3 and self.openai_client:
                self._update_status("Using AI to enhance search strategy...")
                enhanced_results = self._ai_enhanced_search(query, all_results)
                if enhanced_results['results']:
                    all_results.extend(enhanced_results['results'])
                    self._update_status(f"Found {len(enhanced_results['results'])} AI-enhanced results")
            
            # 4. If still insufficient results, try real-time web search
            if len(all_results) < 3:
                self._update_status("Searching real-time web sources...")
                web_results = self._search_real_time_web(query, 3)
                if web_results['results']:
                    all_results.extend(web_results['results'])
                    self._update_status(f"Found {len(web_results['results'])} web search results")

            # 5. If deep search requested or insufficient results, get full page content
            if deep_search or len(all_results) < 2:
                self._update_status("Performing deep content analysis...")
                enhanced_results = self._enhance_with_full_content(all_results[:3])
                all_results = enhanced_results
                self._update_status("Enhanced results with full page content")
            
            self.last_search_time = time.time()
            
            # Remove duplicates and rank by relevance
            unique_results = self._deduplicate_results(all_results)
            
            # Special handling for dead/alive queries with no definitive results
            if any(word in query.lower() for word in ['dead or alive', 'died', 'death']) and len(unique_results) < 2:
                person_name = query.lower().replace(' death', '').replace(' dead or alive', '').replace(' is ', '').replace(' died', '').replace(' news on ', '').replace(' consensus', '').strip()
                
                # Check if existing results already contain definitive death information
                has_death_info = False
                for result in unique_results:
                    content = result.get('content', '').lower()
                    title = result.get('title', '').lower()
                    # Look for clear death indicators in the content
                    death_indicators = ['died', 'death', 'killed', 'fatally', 'obituary', 'passed away', '– september', '– october', '– november', '– december', '– january', '– february', '– march', '– april', '– may', '– june', '– july', '– august']
                    if any(indicator in content or indicator in title for indicator in death_indicators):
                        # Also check for birth-death date patterns like "(1993 – 2025)"
                        if '–' in content or '—' in content:
                            has_death_info = True
                            break
                
                # Only add status inference if we don't already have definitive death information
                if not has_death_info:
                    self._update_status("Insufficient search results - recommend trying different sources")
                    unique_results.insert(0, {
                        'title': f'Search Status: {person_name.title()}',
                        'content': f'Limited information found in current search for {person_name}. This could indicate either that the person is alive or that the information is not easily accessible through the searched sources. For definitive status information, recommend checking official sources, recent news, or biographical resources directly.',
                        'url': '',
                        'type': 'search_status',
                        'timestamp': datetime.now(),
                        'source': 'search_analysis'
                    })
                else:
                    self._update_status("Found definitive biographical information")
            
            final_results = unique_results[:max_results]
            self._update_status(f"Search complete: {len(final_results)} results found")
            
            # Track this search for potential follow-up queries
            self.last_search_query = query
            self.last_search_results = final_results
            self.last_search_time = time.time()
            
            return {
                'success': True,
                'query': query,
                'timestamp': datetime.now(),
                'results_count': len(final_results),
                'results': final_results,
                'summary': self._create_comprehensive_summary(final_results, query),
                'search_method': 'comprehensive' if deep_search else 'standard'
            }
            
        except Exception as e:
            self.logger.error(f"Web search failed: {e}")
            self._update_status(f"Search failed: {str(e)}")
            return {
                'success': False,
                'query': query,
                'timestamp': datetime.now(),
                'error': str(e),
                'results': []
            }
    
    def _search_duckduckgo(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search using DuckDuckGo instant answer API"""
        try:
            # DuckDuckGo instant answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            url = f"https://api.duckduckgo.com/?{urlencode(params)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                results = []
                
                # Check for instant answer
                if data.get('Answer'):
                    results.append({
                        'title': 'Direct Answer',
                        'content': data['Answer'],
                        'url': data.get('AnswerURL', ''),
                        'type': 'instant_answer'
                    })
                
                # Check for abstract
                if data.get('Abstract'):
                    results.append({
                        'title': data.get('Heading', 'Information'),
                        'content': data['Abstract'],
                        'url': data.get('AbstractURL', ''),
                        'type': 'abstract'
                    })
                
                # Add related topics if available
                for topic in data.get('RelatedTopics', [])[:3]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        results.append({
                            'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                            'content': topic['Text'],
                            'url': topic.get('FirstURL', ''),
                            'type': 'related'
                        })
                
                return {'results': results}
            
        except Exception as e:
            self.logger.warning(f"DuckDuckGo API search failed: {e}")
        
        return {'results': []}
    
    def _search_wikipedia_api(self, query: str) -> Dict[str, Any]:
        """Search Wikipedia API with better name matching for people"""
        try:
            # For person queries, extract just the name
            search_query = query
            
            # Clean up query for better Wikipedia searching
            if 'wikipedia' in query.lower():
                # Remove "Wikipedia" from the search query
                search_query = query.lower().replace(' wikipedia', '').replace('wikipedia ', '').strip()
            
            if any(word in query.lower() for word in ['dead or alive', 'died', 'death', 'current president']):
                # Extract the person's name more carefully using regex to avoid breaking text
                import re
                person_name = query.lower()
                
                # Use regex to extract person's name more accurately
                # Look for patterns like "charlie kirk's death" -> "charlie kirk"
                name_patterns = [
                    r"news\s+on\s+(.+?)'s\s+death",  # "news on charlie kirk's death"
                    r"(.+?)'s\s+death",  # "charlie kirk's death" 
                    r"(.+?)\s+died",     # "charlie kirk died"
                    r"(.+?)\s+death",    # "charlie kirk death"
                    r"(.+?)\s+dead\s+or\s+alive",  # "charlie kirk dead or alive"
                    r"(.+?)\s+is\s+dead",  # "charlie kirk is dead"
                    r"news\s+about\s+(.+?)'s\s+death",  # "news about charlie kirk's death"
                    r"(.+?)\s+current\s+president",  # "who is current president"
                ]
                
                extracted_name = None
                for pattern in name_patterns:
                    match = re.search(pattern, person_name)
                    if match:
                        extracted_name = match.group(1).strip()
                        # Clean up extracted name from common prefixes
                        extracted_name = re.sub(r'^(news|on|about)\s+', '', extracted_name)
                        break
                
                if extracted_name:
                    search_query = extracted_name
                else:
                    # Fallback: remove common phrases but preserve apostrophes
                    remove_phrases = [' dead or alive', ' died', ' death', ' is dead', ' current', ' status', ' president of', 'news on ', 'news about ', ' the consensus']
                    for phrase in remove_phrases:
                        person_name = person_name.replace(phrase, '')
                    search_query = person_name.strip()
            
            self.logger.info(f"Wikipedia API search for: '{query}' -> cleaned: '{search_query}'")
            
            # Wikipedia API search
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_query,
                'srlimit': 5  # Get more to filter
            }
            
            # Notify browser activity about accessing Wikipedia
            self._notify_source_access("Wikipedia API", search_url, f"Searching for '{search_query}'")
            
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                search_terms = search_query.lower().split()
                
                for item in data.get('query', {}).get('search', []):
                    title = item['title']
                    title_lower = title.lower()
                    
                    # For multi-word names like "charlie kirk", ensure we get the right person
                    if len(search_terms) >= 2:
                        # Check if title contains all the search terms (for specific people)
                        if not all(term in title_lower for term in search_terms):
                            continue  # Skip irrelevant results like "Charlie X" when searching for "Charlie Kirk"
                    
                    # Get page content
                    page_url = f"https://en.wikipedia.org/w/api.php"
                    page_params = {
                        'action': 'query',
                        'format': 'json',
                        'prop': 'extracts',
                        'exintro': True,
                        'explaintext': True,
                        'titles': title
                    }
                    
                    page_response = requests.get(page_url, params=page_params, headers=self.headers, timeout=10)
                    if page_response.status_code == 200:
                        page_data = page_response.json()
                        pages = page_data.get('query', {}).get('pages', {})
                        
                        for page_id, page_info in pages.items():
                            extract = page_info.get('extract', '')
                            if extract and len(extract) > 50:
                                # Log the first 200 characters to see what we're getting
                                self.logger.info(f"Wikipedia extract for '{title}': {extract[:200]}...")
                                result = {
                                    'title': title,
                                    'content': extract[:500] + ('...' if len(extract) > 500 else ''),
                                    'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                    'type': 'wikipedia',
                                    'source': 'Wikipedia'
                                }
                                results.append(result)
                                # Notify browser activity about this result
                                self._notify_result_found(result)
                                break
                    
                    # Stop after finding 3 relevant results
                    if len(results) >= 3:
                        break
                
                self.logger.info(f"Wikipedia search completed: {len(results)} results found")
                return {'results': results}
                
        except Exception as e:
            self.logger.warning(f"Wikipedia search failed: {e}")
            import traceback
            self.logger.warning(f"Wikipedia search traceback: {traceback.format_exc()}")
        
        return {'results': []}
    
    def _create_search_summary(self, results: List[Dict[str, Any]], query: str) -> str:
        """Create a concise summary of search results"""
        if not results:
            return f"No reliable information found for '{query}'"
        
        # Combine information from multiple sources
        combined_info = []
        
        for result in results:
            content = result.get('content', '').strip()
            if content and len(content) > 20:  # Filter out very short snippets
                # Clean up the content
                content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
                combined_info.append(content)
        
        if not combined_info:
            return f"Found {len(results)} results for '{query}' but content was not accessible"
        
        # Create summary
        if len(combined_info) == 1:
            return combined_info[0]
        else:
            # Combine multiple sources
            summary = combined_info[0]
            
            # Add additional info from other sources if they provide new information
            for info in combined_info[1:]:
                # Simple check to avoid repeating the same info
                if not any(word in summary.lower() for word in info.lower().split()[:5]):
                    summary += f" Additionally, {info}"
                    if len(summary) > 500:  # Keep summaries reasonable
                        break
            
            return summary
    
    def should_search(self, user_query: str, ai_response: str) -> bool:
        """
        Determine if a web search should be triggered using AI analysis + pattern fallback
        """
        # First try AI analysis for intelligent decision making
        if self.openai_client:
            try:
                analysis_prompt = f"""
Analyze this conversation and determine if a web search would be helpful.

User: "{user_query}"
AI Response: "{ai_response}"

A web search should be triggered if:
- User explicitly asks for search/information lookup
- User asks about current events, recent news, or factual information
- User asks "who is", "what is", "when did", etc. about specific people/events
- AI response indicates uncertainty or lack of current information
- User asks for "more information" about a specific topic

A web search should NOT be triggered for:
- Casual conversation or personal opinions  
- Philosophical discussions or abstract concepts
- Personal questions about the user
- Creative writing or hypothetical scenarios
- Simple acknowledgments or thank you messages

Should a web search be triggered?

YES or NO:"""

                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini", 
                    messages=[{"role": "user", "content": analysis_prompt}],
                    max_completion_tokens=5
                )
                
                ai_decision = response.choices[0].message.content.strip().upper()
                
                if ai_decision in ["YES", "NO"]:
                    self.logger.info(f"AI search decision: '{user_query}' -> {ai_decision}")
                    # Notify browser activity about AI decision
                    self._notify_ai_decision("Search Decision", ai_decision, f"AI analyzed: '{user_query}' and decided {ai_decision}")
                    return ai_decision == "YES"
                else:
                    self.logger.warning(f"AI returned unexpected response: '{ai_decision}', using fallback")
                    self._notify_ai_decision("Search Decision", f"FALLBACK (AI said: {ai_decision})", "AI gave unexpected response, using pattern matching fallback")
                    
            except Exception as e:
                self.logger.warning(f"AI search decision failed: {e}, using pattern fallback")
        
        # Fallback to pattern matching if AI fails
        query_lower = user_query.lower()
        
        # High-confidence search triggers (explicit requests)
        explicit_triggers = [
            'search for', 'search up', 'look up', 'google', 'find information about',
            'can you search', 'look it up', 'search it up', 'check online'
        ]
        
        if any(trigger in query_lower for trigger in explicit_triggers):
            self.logger.info(f"Pattern fallback: '{user_query}' -> YES (explicit trigger)")
            return True
        
        # Check AI response for uncertainty indicators
        response_lower = ai_response.lower()
        uncertainty_indicators = [
            "i don't know", "i'm not sure", "i don't have information",
            "i'm not certain", "i don't have current data",
            "i'm not familiar", "i don't recall", "i'm unsure"
        ]
        
        if any(indicator in response_lower for indicator in uncertainty_indicators):
            self.logger.info(f"Pattern fallback: '{user_query}' -> YES (AI uncertainty detected)")
            return True
        
        # Check for contextual follow-up queries (if we recently did a search)
        if self._is_contextual_followup(user_query, ai_response):
            self.logger.info(f"Pattern fallback: '{user_query}' -> YES (contextual follow-up)")
            return True
        
        # Default: no search needed
        self.logger.info(f"Pattern fallback: '{user_query}' -> NO")
        return False
        
        return False
    
    def _is_contextual_followup(self, user_query: str, ai_response: str = "") -> bool:
        """
        Detect if this is a follow-up query to a recent search using AI + pattern matching fallback
        """
        # No recent search to follow up on
        if not self.last_search_query or not self.last_search_time:
            return False
        
        # Only consider VERY recent searches (within last 2 minutes) to prevent cross-conversation contamination
        time_since_search = time.time() - self.last_search_time
        if time_since_search > 120:  # 2 minutes instead of 10 minutes
            self.logger.info(f"Search cache expired: {time_since_search:.1f}s > 120s, clearing cache")
            self.clear_search_cache()
            return False
        
        # First try AI detection if available
        if OPENAI_AVAILABLE and self.openai_client:
            try:
                client = self.openai_client
                
                # Include conversation context with better validation
                context_prompt = f"""CONVERSATION CONTEXT:
Previous search (from {time_since_search:.0f} seconds ago): {self.last_search_query}
Philos just said: {ai_response}
User replied: {user_query}

CRITICAL: Only answer YES if:
1. The user is clearly asking for MORE of the SAME topic
2. Philos's response mentioned the previous search topic
3. The conversation is clearly connected to the previous search

EXAMPLES:
- Previous search: "Darwin Wikipedia" + Philos: "Here's Darwin info" + User: "tell me more" → YES
- Previous search: "Darwin Wikipedia" + Philos: "I like franchises" + User: "i haven't watched them" → NO
- Previous search: "Darwin Wikipedia" + Philos: "About Blade Runner..." + User: "never heard of it" → NO

Does the user want MORE info about "{self.last_search_query}"? Consider if this makes sense in context.

YES or NO:"""

                response = client.chat.completions.create(
                    model="gpt-5-nano",
                    messages=[{"role": "user", "content": context_prompt}],
                    max_completion_tokens=10,  # Increased from 1 to 10 tokens for proper analysis
                    # Note: GPT-5 nano only supports default temperature (1), not custom values
                )
                
                ai_decision = response.choices[0].message.content.strip().upper()
                
                if ai_decision in ["YES", "NO"]:
                    self.logger.info(f"AI contextual analysis: '{user_query}' -> {ai_decision}")
                    return ai_decision == "YES"
                else:
                    self.logger.warning(f"AI returned: '{ai_decision}', using pattern fallback")
                    
            except Exception as e:
                self.logger.error(f"AI analysis failed: {e}, using pattern fallback")
        
        # Fallback to pattern matching
        query_lower = user_query.lower().strip()
        
        # Check if AI offered to continue and user agreed
        ai_lower = ai_response.lower()
        query_lower = user_query.lower().strip()
        
        # If Philos asked about continuing and user said yes/sure/ok
        if any(phrase in ai_lower for phrase in ['next line', 'continue', 'read more', 'more info']) and \
           any(response in query_lower for response in ['yes', 'sure', 'ok', 'yeah', 'yep', 'please']):
            self.logger.info(f"Pattern detected: Philos offered continuation, user agreed")
            return True
        
        # Simple patterns that clearly indicate NEW search requests (not reading existing content)
        followup_patterns = [
            'tell me more about', 'more info about', 'what else about',
            'more about this', 'search for more', 'look up more',
            'find more about', 'get more info', 'more details on'
        ]
        
        # Patterns that suggest reading/processing existing content (NOT new searches)
        reading_patterns = [
            'read me the', 'read the next', 'next line', 'continue reading',
            'keep reading', 'read on', 'show me the next'
        ]
        
        # If user is asking to read existing content, DON'T search
        if any(pattern in query_lower for pattern in reading_patterns):
            self.logger.info(f"Pattern fallback: '{user_query}' -> NO (reading request, not search)")
            return False
        
        # Only trigger search if explicitly asking for MORE information 
        is_followup = any(pattern in query_lower for pattern in followup_patterns)
        self.logger.info(f"Pattern fallback: '{user_query}' -> {'YES' if is_followup else 'NO'}")
        
        return is_followup
    
    def extract_search_query(self, user_input: str, ai_response: str) -> str:
        """
        Use GPT-5 nano to intelligently extract and restructure search queries
        """
        # First, check if this is just casual conversation that mentions searching
        casual_patterns = [
            'nothing much',
            'not much',
            'just wanted to',
            'i\'ve updated you',
            'you can search it up if',
            'if you need to see',
            'if you want to know'
        ]
        
        user_lower = user_input.lower()
        if any(pattern in user_lower for pattern in casual_patterns):
            return ""  # Skip casual conversation
        
        # Check if this is a contextual follow-up query
        if self._is_contextual_followup(user_input, ai_response):
            # Reuse the previous search query for follow-up requests
            self.logger.info(f"Using previous search query for follow-up: '{self.last_search_query}'")
            return self.last_search_query or ""
        
        # Use GPT-5 nano to intelligently restructure the query
        return self._ai_restructure_query(user_input, ai_response)
    
    def _ai_restructure_query(self, user_input: str, ai_response: str) -> str:
        """
        Use GPT-5 nano to intelligently extract and clean search queries
        """
        try:
            # Check if OpenAI is available and we have a client
            if not OPENAI_AVAILABLE or not self.openai_client:
                return self._basic_extract_query(user_input)
            
            client = self.openai_client
            
            restructure_prompt = f"""Extract search terms from: "{user_input}"

Return only the main topic to search for. Remove filler words like "search", "up", "for me", "can you".

Examples:
- "search up the consensus of charlie kirk's death for me" → "Charlie Kirk death"
- "look up who the current king of england is" → "current king england"
- "can you search charles darwin wikipedia" → "Charles Darwin"
- "find out about climate change effects" → "climate change effects"

If there's nothing clear to search for, return "SKIP".

Search terms:"""

            # Use GPT-5 nano for query restructuring
            response = client.chat.completions.create(
                model="gpt-5-nano",
                messages=[{"role": "user", "content": restructure_prompt}],
                max_completion_tokens=50,
                temperature=1  # GPT-5 models only support temperature=1
            )
            
            cleaned_query = response.choices[0].message.content.strip()
            
            # Debug logging (avoid unicode issues)
            self.logger.info(f"AI query restructuring: '{user_input}' -> '{cleaned_query}'")
            # Notify browser activity about query extraction
            self._notify_ai_decision("Query Extraction", cleaned_query, f"GPT-5-nano extracted from: '{user_input}'")
            
            # Handle the response
            if cleaned_query.upper() == "SKIP":
                self.logger.info("AI returned SKIP - no search needed")
                return ""
            
            if not cleaned_query or len(cleaned_query.strip()) < 2:
                self.logger.warning("AI returned empty/short response, using fallback extraction")
                fallback_query = self._basic_extract_query(user_input)
                self.logger.info(f"Fallback extraction: '{user_input}' -> '{fallback_query}'")
                return fallback_query
            
            # Final validation - ensure it's reasonable
            if len(cleaned_query) > 100:
                self.logger.warning(f"AI query too long ({len(cleaned_query)} chars), using fallback")
                return self._basic_extract_query(user_input)
            
            return cleaned_query
            
        except Exception as e:
            self.logger.warning(f"AI query restructuring failed: {e}")
            # Fall back to basic extraction
            return self._basic_extract_query(user_input)
    
    def _basic_extract_query(self, user_input: str) -> str:
        """
        Fallback basic query extraction when AI restructuring fails
        """
        import re
        
        # Special patterns for death/status queries
        death_patterns = [
            (r'search up.*?news.*?on\s+(.+?)\'s\s+death.*?consensus', r'\1 death'),
            (r'search up.*?consensus.*?of\s+(.+?)\'s\s+death', r'\1 death'),
            (r'news.*?on\s+(.+?)\'s\s+death', r'\1 death'),
            (r'(.+?)\'s\s+death.*?consensus', r'\1 death'),
            (r'(.+?)\s+death.*?news', r'\1 death'),
        ]
        
        # Try death-specific patterns first
        for pattern, replacement in death_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                name = match.group(1).strip()
                # Proper case the name
                name_parts = name.split()
                proper_name = ' '.join([part.capitalize() for part in name_parts if part])
                return f"{proper_name} death"
        
        # Split into sentences and find the one with the actual question
        sentences = user_input.split('.')
        main_question = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in ['who', 'what', 'when', 'where', 'why', 'how', 'which']):
                main_question = sentence
                break
        
        # If no clear question found, use the whole input but clean it
        if not main_question:
            main_question = user_input
        
        # Remove common conversational elements
        cleaned_input = main_question.lower()
        
        # Remove AI name references
        ai_names = ['philos', 'ai', 'assistant']
        for name in ai_names:
            cleaned_input = cleaned_input.replace(f' {name}', '').replace(f'{name} ', '')
        
        # Remove search trigger phrases - enhanced list
        search_triggers = [
            'look up ', 'search up ', 'search for ', 'google ', 'bing ',
            'find information about ', 'find out about ',
            'can you search ', 'look it up ', 'search it up ',
            'google it ', 'check online ', 'find online ',
            'search online ', 'look this up ', 'can you ',
            'and tell me what', 'and tell me', 'tell me what',
            'tell me', 'what the first line is', 'what is'
        ]
        
        for trigger in search_triggers:
            cleaned_input = cleaned_input.replace(trigger, '')
        
        # Handle specific patterns
        specific_patterns = [
            ("wikipedia page for ", ""),
            ("information about ", ""),
            ("details about ", ""),
            ("who is the ", "current "),
            ("what is the ", ""),
            ("when did ", ""),
            ("how does ", "")
        ]
        
        for old_phrase, new_phrase in specific_patterns:
            if old_phrase in cleaned_input:
                cleaned_input = cleaned_input.replace(old_phrase, new_phrase)
                break
        
        # Clean up punctuation and extra spaces
        cleaned_input = cleaned_input.strip('?.,!').strip()
        cleaned_input = ' '.join(cleaned_input.split())
        
        # Special handling for Wikipedia requests
        if 'wikipedia' in user_input.lower():
            # Extract the subject name for wikipedia
            import re
            # Look for "wikipedia page for X" and extract just X (stopping at common words)
            wiki_match = re.search(r'wikipedia.*?for\s+([a-zA-Z\s]+?)(?:\s+and\s|\s+tell\s|\s+what\s|$)', user_input.lower())
            if wiki_match:
                subject = wiki_match.group(1).strip()
                # Capitalize properly for names
                subject_words = []
                for word in subject.split():
                    if len(word) > 2:  # Capitalize longer words (names)
                        subject_words.append(word.capitalize())
                    else:
                        subject_words.append(word.lower())
                subject = ' '.join(subject_words)
                return f"{subject} Wikipedia"
        
        # If too short or meaningless, return empty
        if len(cleaned_input) < 3:
            return ""
        
        return cleaned_input

    def _is_current_events_query(self, query: str) -> bool:
        """Determine if query is asking for current/recent events"""
        current_indicators = [
            'today', 'yesterday', 'this week', 'this month', 'recent', 'latest', 
            'current', 'now', 'happening', 'breaking', 'news', '2024', '2025'
        ]
        
        # Political/leadership queries are inherently current events
        political_indicators = [
            'president', 'prime minister', 'leader', 'governor', 'mayor',
            'who is', 'who\'s the', 'current president', 'current pm'
        ]
        
        query_lower = query.lower()
        
        # Check for political queries
        if any(indicator in query_lower for indicator in political_indicators):
            return True
            
        # Check for other current event indicators
        return any(indicator in query_lower for indicator in current_indicators)
    
    def _search_news_feeds(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search multiple real-time news sources for current information"""
        try:
            results = []
            
            # Create targeted search queries for different scenarios
            if any(word in query.lower() for word in ['president', 'election', 'government', 'political']):
                search_queries = [
                    f"{query} 2025 September current",
                    f"{query} latest news today"
                ]
            elif any(word in query.lower() for word in ['dead', 'alive', 'died', 'death', 'obituary']):
                search_queries = [
                    f'"{query}" 2025',
                    f"{query} September 2025 news"
                ]
            else:
                search_queries = [
                    f"{query} news recent 2025",
                    f"{query} latest updates"
                ]
            
            self._update_status("Searching real-time news sources...")
            
            # Strategy 1: Try RSS news feeds from major outlets
            if FEEDPARSER_AVAILABLE:
                news_feeds = [
                    'https://rss.cnn.com/rss/edition.rss',
                    'https://feeds.bbci.co.uk/news/rss.xml',
                    'https://www.reuters.com/rssFeed/topNews',
                    'https://rss.politico.com/politics-news.xml',
                    'https://feeds.npr.org/1001/rss.xml'
                ]
                
                for feed_url in news_feeds[:3]:  # Try first 3 feeds
                    try:
                        self._update_status(f"Checking {feed_url.split('/')[2]} news feed...")
                        feed = feedparser.parse(feed_url)
                        
                        for entry in feed.entries[:5]:  # Check recent entries
                            title = entry.get('title', '')
                            description = entry.get('description', '') or entry.get('summary', '')
                            
                            # Check if this news item relates to our query
                            query_words = query.lower().split()
                            content_text = f"{title} {description}".lower()
                            
                            if any(word in content_text for word in query_words if len(word) > 3):
                                results.append({
                                    'title': title,
                                    'content': description[:300] if description else f"News about {query}",
                                    'url': entry.get('link', ''),
                                    'type': 'rss_news',
                                    'timestamp': datetime.now(),
                                    'source': feed_url.split('/')[2],
                                    'published': entry.get('published', '')
                                })
                                
                        if len(results) >= max_results:
                            break
                            
                    except Exception as e:
                        self.logger.debug(f"RSS feed {feed_url} failed: {e}")
                        continue
            
            # Strategy 2: Direct news site search with better scraping
            if len(results) < max_results:
                self._update_status("Searching news websites directly...")
                
                news_sites = [
                    f"https://www.google.com/search?q={quote_plus(search_queries[0])}+site:cnn.com+OR+site:bbc.com+OR+site:reuters.com&tbm=nws",
                    f"https://www.bing.com/news/search?q={quote_plus(search_queries[0])}"
                ]
                
                for site_url in news_sites[:1]:  # Try Google News search
                    try:
                        response = requests.get(site_url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }, timeout=15)
                        
                        if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Look for news results in Google News format
                            news_results = soup.find_all(['div', 'article', 'h3'], class_=lambda x: x and any(cls in str(x).lower() for cls in ['news', 'result', 'article', 'headline']))
                            
                            for result in news_results[:5]:
                                title = result.get_text().strip()
                                if title and len(title) > 20 and not title.startswith('http'):
                                    # Try to find the link
                                    link_elem = result.find('a') or result.find_parent('a')
                                    url = link_elem.get('href', '') if link_elem else ''
                                    
                                    results.append({
                                        'title': title,
                                        'content': f"Current news: {title}",
                                        'url': url,
                                        'type': 'web_news',
                                        'timestamp': datetime.now(),
                                        'source': 'google_news'
                                    })
                                    
                    except Exception as e:
                        self.logger.debug(f"News site search failed: {e}")
            
            # Strategy 3: Try alternative search engines with news focus
            if len(results) < 2:
                self._update_status("Searching alternative news sources...")
                
                alt_queries = [
                    f"{query} news today",
                    f'"{query}" breaking news 2025'
                ]
                
                for alt_query in alt_queries[:1]:
                    try:
                        # Try Bing News API approach
                        bing_url = f"https://www.bing.com/search?q={quote_plus(alt_query)}&setmkt=en-US&first=1"
                        
                        response = requests.get(bing_url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }, timeout=10)
                        
                        if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Look for search results
                            search_results = soup.find_all(['h2', 'h3'], class_=lambda x: x and 'result' in str(x).lower())
                            
                            for result in search_results[:3]:
                                title = result.get_text().strip()
                                if title and len(title) > 15:
                                    # Try to get the snippet/description
                                    parent = result.find_parent('div') or result.find_parent('li')
                                    description = ""
                                    if parent:
                                        desc_elem = parent.find('p') or parent.find('div', class_=lambda x: x and 'desc' in str(x).lower())
                                        if desc_elem:
                                            description = desc_elem.get_text().strip()[:200]
                                    
                                    results.append({
                                        'title': title,
                                        'content': description or f"Search result about {query}",
                                        'url': '',
                                        'type': 'search_result',
                                        'timestamp': datetime.now(),
                                        'source': 'bing_search'
                                    })
                                    
                    except Exception as e:
                        self.logger.debug(f"Alternative search failed: {e}")
            
            # If still no results, try one more direct approach
            if len(results) == 0:
                self._update_status("Trying direct content search...")
                
                # Try to search for the person/topic directly on news aggregators
                try:
                    direct_query = query.replace(' dead or alive', '').replace(' current', '').strip()
                    search_url = f"https://duckduckgo.com/?q={quote_plus(direct_query + ' news 2025')}&iar=news&ia=news"
                    
                    response = requests.get(search_url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        # Add at least a basic search attempt result
                        results.append({
                            'title': f'Search Results for {direct_query}',
                            'content': f'Searched for recent news about {direct_query}. Results may vary based on current news availability.',
                            'url': search_url,
                            'type': 'search_attempt',
                            'timestamp': datetime.now(),
                            'source': 'direct_search'
                        })
                        
                except Exception as e:
                    self.logger.debug(f"Direct search failed: {e}")
            
            # If absolutely no results, provide informative response
            if len(results) == 0:
                results.append({
                    'title': 'News Search Attempted',
                    'content': f'Searched multiple news sources for current information about {query}. No recent news found in available feeds, which could indicate either no recent developments or limited access to real-time news data.',
                    'url': '',
                    'type': 'search_summary',
                    'timestamp': datetime.now(),
                    'source': 'system'
                })
            
            return {'results': results[:max_results]}
            
        except Exception as e:
            self.logger.error(f"News search failed: {e}")
            return {'results': []}

    def _search_breaking_news(self, query: str) -> Dict[str, Any]:
        """Specialized search for breaking news and major announcements"""
        try:
            results = []
            
            # For death/alive queries, check specific sources
            if any(word in query.lower() for word in ['dead', 'alive', 'died', 'death']):
                self._update_status("Checking for recent announcements...")
                
                # Check Twitter/X feeds (via web scraping)
                person_name = query.lower().replace(' dead or alive', '').replace(' died', '').replace(' death', '').strip()
                
                # Try to search for recent social media or news announcements
                breaking_queries = [
                    f'"{person_name}" died 2025',
                    f'"{person_name}" death announcement',
                    f'"{person_name}" obituary September 2025'
                ]
                
                for breaking_query in breaking_queries[:2]:
                    try:
                        # Search for very specific news
                        params = {
                            'q': breaking_query,
                            'format': 'json',
                            'no_html': '1'
                        }
                        
                        url = f"https://api.duckduckgo.com/?{urlencode(params)}"
                        response = requests.get(url, headers=self.headers, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Look for instant answers about death/status
                            if data.get('Answer'):
                                results.append({
                                    'title': 'Status Information',
                                    'content': data['Answer'],
                                    'url': data.get('AnswerURL', ''),
                                    'type': 'breaking_news',
                                    'timestamp': datetime.now(),
                                    'source': 'instant_answer'
                                })
                            
                            # Check related topics for death announcements
                            if data.get('RelatedTopics'):
                                for topic in data['RelatedTopics'][:3]:
                                    if isinstance(topic, dict) and topic.get('Text'):
                                        text = topic['Text'].lower()
                                        # Look for death-related keywords
                                        if any(death_word in text for death_word in ['died', 'death', 'obituary', 'passed away', 'funeral']):
                                            results.append({
                                                'title': f'Breaking: {person_name}',
                                                'content': topic['Text'],
                                                'url': topic.get('FirstURL', ''),
                                                'type': 'death_announcement',
                                                'timestamp': datetime.now(),
                                                'source': 'breaking_news'
                                            })
                                            
                    except Exception as e:
                        self.logger.debug(f"Breaking news search failed: {e}")
            
            return {'results': results}
            
        except Exception as e:
            self.logger.error(f"Breaking news search failed: {e}")
            return {'results': []}

    def _search_real_time_web(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search multiple search engines for the most current information"""
        try:
            results = []
            
            self._update_status("Searching multiple engines for current information...")
            
            # Try different search engines with current date emphasis
            search_engines = [
                {
                    'name': 'DuckDuckGo HTML',
                    'url': f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' 2025')}",
                    'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                },
                {
                    'name': 'StartPage',
                    'url': f"https://www.startpage.com/sp/search?query={quote_plus(query + ' recent news')}",
                    'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                }
            ]
            
            for engine in search_engines[:1]:  # Try first engine
                try:
                    self._update_status(f"Checking {engine['name']}...")
                    
                    response = requests.get(
                        engine['url'], 
                        headers=engine['headers'],
                        timeout=12
                    )
                    
                    if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for search result titles and snippets
                        result_selectors = [
                            'h2 a', 'h3 a', '.result-title', '.web-result h3', 
                            '.result__title a', '.organic-result h3'
                        ]
                        
                        found_results = []
                        for selector in result_selectors:
                            elements = soup.select(selector)
                            if elements:
                                found_results.extend(elements[:5])
                                break
                        
                        for element in found_results[:3]:
                            title = element.get_text().strip()
                            url = element.get('href', '')
                            
                            # Try to find description/snippet
                            parent = element.find_parent(['div', 'li', 'article'])
                            description = ""
                            
                            if parent:
                                # Look for snippet text
                                snippet_elem = parent.find(['p', 'span', 'div'], class_=lambda x: x and any(
                                    cls in str(x).lower() for cls in ['snippet', 'desc', 'summary', 'content']
                                ))
                                if snippet_elem:
                                    description = snippet_elem.get_text().strip()[:300]
                            
                            if title and len(title) > 10:
                                results.append({
                                    'title': title,
                                    'content': description or f"Search result about {query}",
                                    'url': url if url.startswith('http') else f"https:{url}" if url.startswith('//') else '',
                                    'type': 'web_search_result',
                                    'timestamp': datetime.now(),
                                    'source': engine['name'].lower().replace(' ', '_')
                                })
                                
                except Exception as e:
                    self.logger.debug(f"{engine['name']} search failed: {e}")
                    continue
            
            # Try one more direct approach - search for very specific terms
            if len(results) == 0:
                self._update_status("Trying direct fact checking...")
                
                # Create very specific queries
                specific_queries = []
                if 'dead or alive' in query.lower():
                    person = query.lower().replace(' dead or alive', '').replace(' is ', '').strip()
                    specific_queries = [
                        f'"{person}" "died" 2025',
                        f'"{person}" "death" September 2025',
                        f'"{person}" alive status current'
                    ]
                
                for specific_query in specific_queries[:1]:
                    try:
                        params = {
                            'q': specific_query,
                            'format': 'json',
                            'no_html': '1'
                        }
                        
                        url = f"https://api.duckduckgo.com/?{urlencode(params)}"
                        response = requests.get(url, headers=self.headers, timeout=8)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Check for any relevant information
                            if data.get('Answer'):
                                results.append({
                                    'title': 'Direct Answer',
                                    'content': data['Answer'],
                                    'url': data.get('AnswerURL', ''),
                                    'type': 'fact_check',
                                    'timestamp': datetime.now(),
                                    'source': 'direct_query'
                                })
                            
                            # Check abstract for biographical info
                            if data.get('Abstract'):
                                results.append({
                                    'title': 'Biographical Information',
                                    'content': data['Abstract'],
                                    'url': data.get('AbstractURL', ''),
                                    'type': 'biography',
                                    'timestamp': datetime.now(),
                                    'source': 'direct_query'
                                })
                                
                    except Exception as e:
                        self.logger.debug(f"Direct fact check failed: {e}")
            
            return {'results': results}
            
        except Exception as e:
            self.logger.error(f"Real-time web search failed: {e}")
            return {'results': []}
    
    def _search_current_politics(self, query: str) -> Dict[str, Any]:
        """Search for current political information with 2025-specific queries"""
        try:
            results = []
            
            # Try specific current political searches
            political_queries = [
                f"Joe Biden president 2025 September",
                f"US president September 2025",
                f"current US president September 13 2025",
                f"who is president united states september 2025"
            ]
            
            for political_query in political_queries:
                self._update_status(f"Trying political search: {political_query}")
                
                # Try DuckDuckGo search
                params = {
                    'q': political_query,
                    'format': 'json',
                    'no_html': '1'
                }
                
                url = f"https://api.duckduckgo.com/?{urlencode(params)}"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check for direct answers
                    if data.get('Answer'):
                        results.append({
                            'title': 'Current Political Information',
                            'content': data['Answer'],
                            'url': data.get('AnswerURL', ''),
                            'type': 'current_political',
                            'timestamp': datetime.now()
                        })
                    
                    # Check abstract for political info
                    if data.get('Abstract') and '2025' in data['Abstract']:
                        results.append({
                            'title': 'Political Update 2025',
                            'content': data['Abstract'],
                            'url': data.get('AbstractURL', ''),
                            'type': 'political_abstract',
                            'timestamp': datetime.now()
                        })
                
                if results:
                    break  # Stop on first successful result
            
            return {'results': results}
            
        except Exception as e:
            self.logger.error(f"Current politics search failed: {e}")
            return {'results': []}
    
    def _enhance_with_full_content(self, results: list) -> list:
        """Extract full content from web pages for deeper analysis"""
        enhanced_results = []
        
        for result in results:
            if not result.get('url') or result.get('type') == 'full_content':
                enhanced_results.append(result)
                continue
            
            # For Wikipedia results, we already have clean content from the API - don't scrape HTML
            if result.get('type') == 'wikipedia' and result.get('content'):
                enhanced_result = result.copy()
                enhanced_result['type'] = 'full_content'
                enhanced_results.append(enhanced_result)
                continue
            
            try:
                self._update_status(f"Reading full content from {result.get('title', 'page')}...")
                
                response = requests.get(
                    result['url'], 
                    headers=self.headers, 
                    timeout=15,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    # Parse HTML and extract main content
                    if not BEAUTIFULSOUP_AVAILABLE:
                        # Fallback: simple text extraction
                        text = response.text
                        # Remove common HTML tags
                        import re
                        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
                        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
                        text = re.sub(r'<[^>]+>', '', text)
                        # Clean up whitespace
                        lines = (line.strip() for line in text.splitlines())
                        clean_text = ' '.join(line for line in lines if line)
                        if len(clean_text) > 2000:
                            clean_text = clean_text[:2000] + "..."
                        
                        enhanced_result = result.copy()
                        enhanced_result['content'] = clean_text
                        enhanced_result['type'] = 'full_content'
                        enhanced_results.append(enhanced_result)
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Try to find main content areas
                    main_content = None
                    for selector in ['main', 'article', '.content', '#content', '.post-content']:
                        main_content = soup.select_one(selector)
                        if main_content:
                            break
                    
                    if not main_content:
                        main_content = soup.body
                    
                    if main_content:
                        # Extract text and clean it
                        text = main_content.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        clean_text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        # Limit content length
                        if len(clean_text) > 2000:
                            clean_text = clean_text[:2000] + "..."
                        
                        enhanced_result = result.copy()
                        enhanced_result['content'] = clean_text
                        enhanced_result['type'] = 'full_content'
                        enhanced_results.append(enhanced_result)
                        self.logger.info(f"Enhanced content for {result.get('title', 'page')} - first 200 chars: {clean_text[:200]}")
                    else:
                        enhanced_results.append(result)
                else:
                    enhanced_results.append(result)
                    
            except Exception as e:
                self.logger.error(f"Failed to enhance result {result.get('url', '')}: {e}")
                enhanced_results.append(result)
        
        return enhanced_results
    
    def _deduplicate_results(self, results: list) -> list:
        """Remove duplicate results based on content similarity"""
        unique_results = []
        seen_urls = set()
        seen_titles = set()
        
        for result in results:
            url = result.get('url', '')
            title = result.get('title', '').lower().strip()
            
            # Skip if we've seen this exact URL
            if url and url in seen_urls:
                continue
            
            # For titles, only consider them duplicates if they are very similar (not just contained)
            is_duplicate_title = False
            if title:
                for seen_title in seen_titles:
                    # Only consider duplicate if titles are nearly identical (>80% similar length)
                    # or if they are exactly the same after removing common words
                    title_clean = title.replace('killing of ', '').replace('death of ', '').replace('the ', '')
                    seen_clean = seen_title.replace('killing of ', '').replace('death of ', '').replace('the ', '')
                    
                    # Exact match after cleaning
                    if title_clean == seen_clean and len(title_clean) > 5:
                        # But allow if one is specifically about death/killing and other is general
                        if ('killing' in title or 'death' in title) and ('killing' not in seen_title and 'death' not in seen_title):
                            continue  # Allow this as it's more specific
                        elif ('killing' in seen_title or 'death' in seen_title) and ('killing' not in title and 'death' not in title):
                            continue  # Allow this as it's more specific
                        else:
                            is_duplicate_title = True
                            break
            
            if is_duplicate_title:
                continue
            
            unique_results.append(result)
            if url:
                seen_urls.add(url)
            if title:
                seen_titles.add(title)
        
        return unique_results
    
    def _chunk_content(self, content: str, max_chunk_size: int = 1500) -> list:
        """
        Intelligently chunk content into manageable pieces for AI processing.
        Similar to how ChatGPT handles long content.
        """
        if len(content) <= max_chunk_size:
            return [content]
        
        chunks = []
        sentences = content.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            # Add sentence to current chunk if it fits
            test_chunk = current_chunk + sentence + '. '
            if len(test_chunk) <= max_chunk_size:
                current_chunk = test_chunk
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        
        # Add remaining content
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def _create_comprehensive_summary(self, results: list, query: str) -> str:
        """Create a comprehensive summary of all search results with intelligent chunking"""
        if not results:
            return f"No results found for '{query}'"
        
        summary_parts = [f"Search Results for '{query}':\n"]
        
        for i, result in enumerate(results, 1):
            result_type = result.get('type', 'web')
            title = result.get('title', f'Result {i}')
            content = result.get('content', '').strip()
            
            if content:
                # For Wikipedia and detailed sources, use chunking instead of truncation
                if result_type == 'wikipedia' or len(content) > 1000:
                    chunks = self._chunk_content(content, max_chunk_size=1500)
                    
                    summary_parts.append(f"{i}. [{result_type.upper()}] {title}")
                    if len(chunks) == 1:
                        summary_parts.append(f"   {chunks[0]}\n")
                    else:
                        for j, chunk in enumerate(chunks[:3], 1):  # Limit to first 3 chunks
                            summary_parts.append(f"   [Part {j}/{min(len(chunks), 3)}] {chunk}")
                            if j < min(len(chunks), 3):
                                summary_parts.append("")  # Add spacing between chunks
                        if len(chunks) > 3:
                            summary_parts.append(f"   [... {len(chunks) - 3} more sections available]")
                        summary_parts.append("")
                else:
                    # For shorter content, use as-is
                    summary_parts.append(f"{i}. [{result_type.upper()}] {title}")
                    summary_parts.append(f"   {content}\n")
        
        return '\n'.join(summary_parts)

    def search_with_refinement(self, query: str, max_results: int = 5, deep_search: bool = False) -> Dict[str, Any]:
        """
        Intelligent search that can refine the query if results don't match user intent
        """
        # First attempt
        results = self.search_web(query, max_results, deep_search)
        
        if not results['success'] or len(results['results']) < 2:
            self._update_status("Initial search had limited results, trying refined approach...")
            
            # Try different search strategies
            refined_queries = self._generate_refined_queries(query)
            
            for refined_query in refined_queries:
                self._update_status(f"Trying refined search: '{refined_query}'")
                refined_results = self.search_web(refined_query, max_results, deep_search)
                
                if refined_results['success'] and len(refined_results['results']) >= 2:
                    # Combine original and refined results
                    all_results = results['results'] + refined_results['results']
                    unique_results = self._deduplicate_results(all_results)
                    
                    return {
                        'success': True,
                        'query': query,
                        'refined_query': refined_query,
                        'timestamp': datetime.now(),
                        'results_count': len(unique_results[:max_results]),
                        'results': unique_results[:max_results],
                        'summary': self._create_comprehensive_summary(unique_results[:max_results], query),
                        'search_method': 'refined'
                    }
        
        return results
    
    def _generate_refined_queries(self, original_query: str) -> List[str]:
        """Generate alternative search queries when initial search fails"""
        refined_queries = []
        
        # Special handling for political/current events queries
        if any(word in original_query.lower() for word in ['president', 'current president', 'who is president']):
            refined_queries.extend([
                "current US president 2025",
                "United States president September 2025", 
                "who is president now 2025"
            ])
            return refined_queries[:3]
        
        # Add more specific terms
        if len(original_query.split()) <= 2:
            refined_queries.append(f"{original_query} definition explanation")
            refined_queries.append(f"{original_query} information facts")
        
        # Add synonyms for common words
        word_synonyms = {
            'how': 'method way process',
            'what': 'definition meaning explanation',
            'why': 'reason cause purpose',
            'where': 'location place position',
            'when': 'time date period'
        }
        
        words = original_query.lower().split()
        for word, synonyms in word_synonyms.items():
            if word in words:
                for synonym in synonyms.split():
                    new_query = original_query.lower().replace(word, synonym)
                    refined_queries.append(new_query)
        
        # Try removing question words
        question_words = ['what', 'how', 'why', 'where', 'when', 'who', 'which']
        words = original_query.lower().split()
        filtered_words = [w for w in words if w not in question_words]
        if len(filtered_words) > 0 and len(filtered_words) < len(words):
            refined_queries.append(' '.join(filtered_words))
        
        # Try adding context terms
        context_terms = ['latest', 'recent', '2024', 'current', 'today']
        for term in context_terms:
            if term not in original_query.lower():
                refined_queries.append(f"{original_query} {term}")
        
        return refined_queries[:3]  # Limit to 3 refined attempts
    
    def _ai_enhanced_search(self, original_query: str, existing_results: List[Dict]) -> Dict[str, Any]:
        """Use AI to analyze query intent and generate better search strategies"""
        try:
            if not self.openai_client:
                return {'results': []}
            
            # Analyze what we've found so far
            results_summary = ""
            if existing_results:
                results_summary = f"Current results found: {', '.join([r.get('title', 'Untitled')[:50] for r in existing_results[:3]])}"
            else:
                results_summary = "No relevant results found yet"
            
            # Ask AI to analyze the query and suggest better search strategies
            analysis_prompt = f"""
Analyze this search query and suggest 3 better, more specific search terms that would find current, relevant information:

Original Query: "{original_query}"
Current Results: {results_summary}

Based on the query, determine:
1. What type of information is being sought (news, status, facts, opinions, etc.)
2. What are 3 specific, targeted search terms that would find this information?
3. What time period is most relevant (recent news, historical, current status)?

Respond in this exact format:
QUERY_TYPE: [news/status/facts/opinions/how-to/etc]
SEARCH_TERMS: 
- [specific search term 1]
- [specific search term 2] 
- [specific search term 3]
TIME_FOCUS: [recent/current/historical/any]
"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_completion_tokens=200
            )
            
            ai_analysis = response.choices[0].message.content.strip()
            self.logger.info(f"AI search analysis: {ai_analysis}")
            
            # Parse the AI response
            search_terms = []
            query_type = "general"
            time_focus = "any"
            
            lines = ai_analysis.split('\n')
            for line in lines:
                if line.startswith('QUERY_TYPE:'):
                    query_type = line.split(':', 1)[1].strip()
                elif line.startswith('- '):
                    search_terms.append(line[2:].strip())
                elif line.startswith('TIME_FOCUS:'):
                    time_focus = line.split(':', 1)[1].strip()
            
            # Use the AI-generated search terms
            results = []
            for search_term in search_terms[:2]:  # Use top 2 AI-suggested terms
                if search_term and search_term != original_query:
                    self._update_status(f"Trying AI-suggested search: '{search_term}'")
                    
                    # Add time context if needed
                    if time_focus == "recent" and "2025" not in search_term:
                        search_term += " 2025 recent"
                    elif time_focus == "current" and "current" not in search_term:
                        search_term += " current latest"
                    
                    # Try multiple search methods with the AI-improved query
                    search_methods = [
                        lambda q: self._search_duckduckgo(q, 2),
                        lambda q: self._search_real_time_web(q, 2),
                    ]
                    
                    # If it's a news-type query, prioritize news sources
                    if query_type in ["news", "status", "current"]:
                        search_methods.insert(0, lambda q: self._search_news_feeds(q, 2))
                    
                    for search_method in search_methods:
                        method_results = search_method(search_term)
                        if method_results.get('results'):
                            results.extend(method_results['results'][:1])  # Take best result from each method
                            break  # Found results, move to next search term
            
            return {'results': results}
            
        except Exception as e:
            self.logger.warning(f"AI-enhanced search failed: {e}")
            return {'results': []}
    
    def _search_reddit(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Reddit for community discussions and opinions"""
        try:
            results = []
            
            # Reddit search URL - using old.reddit.com for better parsing
            search_url = f"https://old.reddit.com/search?q={quote_plus(query)}&sort=relevance&t=all"
            
            self._update_status("Searching Reddit discussions...")
            # Notify browser activity about Reddit access
            self._notify_source_access("Reddit", search_url, f"Searching Reddit for '{query}'")
            
            response = requests.get(search_url, headers=self.headers, timeout=12)
            
            if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find Reddit post entries
                posts = soup.find_all('div', class_='thing')
                
                for post in posts[:max_results]:
                    try:
                        # Extract title
                        title_elem = post.find('a', class_='title')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text().strip()
                        post_url = title_elem.get('href', '')
                        
                        # Make sure URL is absolute
                        if post_url.startswith('/'):
                            post_url = f"https://old.reddit.com{post_url}"
                        
                        # Extract subreddit
                        subreddit_elem = post.find('a', class_='subreddit')
                        subreddit = subreddit_elem.get_text() if subreddit_elem else "Unknown"
                        
                        # Extract score/upvotes
                        score_elem = post.find('div', class_='score')
                        score = score_elem.get_text() if score_elem else "0"
                        
                        # Extract preview text if available
                        content_elem = post.find('div', class_='usertext-body')
                        content = ""
                        if content_elem:
                            content = content_elem.get_text().strip()[:200] + "..."
                        else:
                            content = f"Reddit discussion about {query}"
                        
                        result = {
                            'title': f"[{subreddit}] {title}",
                            'content': content,
                            'url': post_url,
                            'type': 'reddit_post',
                            'score': score,
                            'source': 'Reddit'
                        }
                        results.append(result)
                        # Notify browser activity about this result
                        self._notify_result_found(result)
                        
                    except Exception as e:
                        self.logger.debug(f"Error parsing Reddit post: {e}")
                        continue
            
            return {'results': results}
            
        except Exception as e:
            self.logger.warning(f"Reddit search failed: {e}")
            return {'results': []}
    
    def _search_quora(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Quora for Q&A content"""
        try:
            results = []
            
            # Quora search URL
            search_url = f"https://www.quora.com/search?q={quote_plus(query)}"
            
            self._update_status("Searching Quora for Q&A content...")
            
            # Use different headers for Quora to avoid blocking
            quora_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(search_url, headers=quora_headers, timeout=15)
            
            if response.status_code == 200 and BEAUTIFULSOUP_AVAILABLE:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try different selectors for Quora questions
                question_selectors = [
                    'a[data-testid="QuestionTitle"]',
                    '.question_link',
                    '.question_text a',
                    'a.question_link',
                    'h2 a'
                ]
                
                questions = []
                for selector in question_selectors:
                    questions = soup.select(selector)
                    if questions:
                        break
                
                for question in questions[:max_results]:
                    try:
                        title = question.get_text().strip()
                        question_url = question.get('href', '')
                        
                        # Make URL absolute
                        if question_url.startswith('/'):
                            question_url = f"https://www.quora.com{question_url}"
                        
                        # Try to find answer preview
                        parent = question.find_parent(['div', 'article', 'section'])
                        answer_preview = ""
                        
                        if parent:
                            # Look for answer text in parent container
                            answer_elem = parent.find(['p', 'div', 'span'], class_=lambda x: x and any(
                                word in str(x).lower() for word in ['answer', 'content', 'text', 'description']
                            ))
                            
                            if answer_elem:
                                answer_text = answer_elem.get_text().strip()
                                if answer_text and len(answer_text) > 20:
                                    answer_preview = answer_text[:250] + "..."
                        
                        if not answer_preview:
                            answer_preview = f"Quora discussion: {title[:100]}..."
                        
                        results.append({
                            'title': title,
                            'content': answer_preview,
                            'url': question_url,
                            'type': 'quora_qa',
                            'source': 'Quora'
                        })
                        
                    except Exception as e:
                        self.logger.debug(f"Error parsing Quora question: {e}")
                        continue
            
            return {'results': results}
            
        except Exception as e:
            self.logger.warning(f"Quora search failed: {e}")
            return {'results': []}
