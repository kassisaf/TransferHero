import requests
from urllib.parse import urlparse
from main import APP_NAME


# Simple attempt at returning a school's class schedule
# Not elegant, but no google API key required so we're not subject to a limited number of calls per day
def find_class_schedule_link(school_name, other_keywords=''):
    query_string = ','.join(f'class schedule {school_name} california {other_keywords}'.split())
    # Get "I'm Feeling Lucky" results from google
    google = requests.get(f'https://www.google.com/search?q={query_string}&btnI', allow_redirects='false')
    # If it's not a .edu page, try DuckDuckGo instead
    if not urlparse(google.url).netloc.endswith('.edu'):
        duckduckgo = requests.get(f'https://duckduckgo.com/?t={APP_NAME}?q=!{query_string}')
        if urlparse(duckduckgo.url).netloc.endswith('.edu'):
            return duckduckgo.url
    # Still no .edu so just return the google result
    return google.url
