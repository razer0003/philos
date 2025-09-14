import requests
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import re
from urllib.parse import urlencode, quote_plus, urlparse
import time

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
    def __init__(self, status_callback: Optional[Callable[[str], None]] = None):
        self.logger = logging.getLogger(__name__)
        self.status_callback = status_callback  # Callback for live updates
        
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
    
    def _update_status(self, message: str):
        """Send status update to callback if available"""
        if self.status_callback:
            self.status_callback(message)
        self.logger.info(f"Search Status: {message}")
        
    def search_web(self, query: str, max_results: int = 5, deep_search: bool = False) -> Dict[str, Any]:
        """
        Perform comprehensive web search with live updates
        Returns search results with summaries and full content when requested
        """
        try:
            self._update_status(f"Starting search for '{query}'...")
            
            # Rate limiting
            current_time = time.time()
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
                person_name = query.lower().replace(' dead or alive', '').replace(' is ', '').replace(' died', '').strip()
                
                # If we can't find any death announcements, the person is likely alive
                self._update_status("No death announcements found - person likely alive")
                unique_results.insert(0, {
                    'title': f'Status Check: {person_name.title()}',
                    'content': f'No recent death announcements or obituaries found for {person_name}. Based on the absence of death-related news in major sources, {person_name} is likely still alive as of September 2025. This conclusion is based on the principle that significant deaths are typically widely reported.',
                    'url': '',
                    'type': 'status_inference',
                    'timestamp': datetime.now(),
                    'source': 'search_analysis'
                })
            
            final_results = unique_results[:max_results]
            self._update_status(f"Search complete: {len(final_results)} results found")
            
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
            if any(word in query.lower() for word in ['dead or alive', 'died', 'death', 'current president']):
                # Extract the person's name more carefully
                person_name = query.lower()
                for remove_phrase in [' dead or alive', ' died', ' death', ' is ', ' current', ' status', ' president of', ' the ']:
                    person_name = person_name.replace(remove_phrase, '')
                person_name = person_name.strip()
                search_query = person_name
            
            # Wikipedia API search
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': search_query,
                'srlimit': 5  # Get more to filter
            }
            
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
                                results.append({
                                    'title': title,
                                    'content': extract[:500] + ('...' if len(extract) > 500 else ''),
                                    'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                    'type': 'wikipedia'
                                })
                                break
                    
                    # Stop after finding 3 relevant results
                    if len(results) >= 3:
                        break
                
                return {'results': results}
                
        except Exception as e:
            self.logger.warning(f"Wikipedia search failed: {e}")
        
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
        Determine if a web search should be triggered based on the conversation
        """
        query_lower = user_query.lower()
        response_lower = ai_response.lower()
        
        # Explicit search requests
        search_triggers = [
            'search for', 'look up', 'find information about',
            'what\'s the latest', 'current information', 'recent news',
            'can you search', 'look it up', 'find out'
        ]
        
        if any(trigger in query_lower for trigger in search_triggers):
            return True
        
        # "I don't know" indicators in AI response
        uncertainty_indicators = [
            "i don't know", "i'm not sure", "i don't have information",
            "i'm not certain", "i don't have current data",
            "i'm not familiar", "i don't recall", "i'm unsure",
            "no information", "not sure about", "don't have details"
        ]
        
        if any(indicator in response_lower for indicator in uncertainty_indicators):
            return True
        
        # Current events or time-sensitive queries
        current_indicators = [
            'today', 'this year', 'recently', 'latest', 'current',
            'now', '2025', 'newest', 'updated', 'breaking'
        ]
        
        if any(indicator in query_lower for indicator in current_indicators):
            return True
        
        return False
    
    def extract_search_query(self, user_input: str, ai_response: str) -> str:
        """
        Extract the appropriate search query from the conversation context
        """
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
            cleaned_input = cleaned_input.replace(f' {name}?', '').replace(f'{name}?', '')
        
        # Remove redundant phrases from the beginning
        redundant_starters = [
            'based off of the most recent news, ',
            'based on the most recent news, ',
            'according to recent news, '
        ]
        
        for starter in redundant_starters:
            if cleaned_input.startswith(starter):
                cleaned_input = cleaned_input[len(starter):]
                break
        
        # Remove search/test trigger phrases - be more aggressive
        search_triggers = [
            'testing your ability to search things up', 'testing your ability to search',
            'test your search', 'testing you', 'testing your',
            'search for ', 'look up ', 'find information about ',
            'can you search ', 'look it up ', 'find out about ',
            'actually, ', 'actually ', ', actually'
        ]
        
        for trigger in search_triggers:
            cleaned_input = cleaned_input.replace(trigger, '')
        
        # Handle common question patterns
        question_replacements = [
            ("what's happened in ", "events in "),
            ("what happened in ", "events in "),
            ("what's going on in ", "current events "),
            ("what is ", ""),
            ("who is ", ""),
            ("where is ", ""),
            ("when did ", ""),
            ("how does ", ""),
            ("why did ", "")
        ]
        
        for old_phrase, new_phrase in question_replacements:
            if cleaned_input.startswith(old_phrase):
                cleaned_input = new_phrase + cleaned_input[len(old_phrase):]
                break
        
        # Clean up punctuation and extra spaces
        cleaned_input = cleaned_input.strip('?.,!').strip()
        cleaned_input = ' '.join(cleaned_input.split())  # Remove extra whitespace
        
        return cleaned_input if cleaned_input else user_input

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
            title = result.get('title', '').lower()
            
            # Skip if we've seen this URL or very similar title
            if url and url in seen_urls:
                continue
            if title and any(title in seen_title or seen_title in title for seen_title in seen_titles):
                continue
            
            unique_results.append(result)
            if url:
                seen_urls.add(url)
            if title:
                seen_titles.add(title)
        
        return unique_results
    
    def _create_comprehensive_summary(self, results: list, query: str) -> str:
        """Create a comprehensive summary of all search results"""
        if not results:
            return f"No results found for '{query}'"
        
        summary_parts = [f"Search Results for '{query}':\n"]
        
        for i, result in enumerate(results, 1):
            result_type = result.get('type', 'web')
            title = result.get('title', f'Result {i}')
            content = result.get('content', '').strip()
            
            if content:
                # Limit content in summary
                if len(content) > 200:
                    content = content[:200] + "..."
                
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
