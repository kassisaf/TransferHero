from secrets import GOOGLE_API_KEY as KEY  # See secrets.example.py for setup steps
from secrets import GOOGLE_CSE_ID as CSE
from googleapiclient.discovery import build
from urllib.parse import urlparse


def search(query_string, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query_string, cx=cse_id, **kwargs).execute()
    return res['items']


# Searches google for a school's class schedule and returns the first link on a
def find_class_schedule_page(school_name, other_keywords=''):
    query_string = f'{school_name} class schedule {other_keywords}'
    results = search(query_string, KEY, CSE, num=10)
    for result in results:
        # Since Selenium brings in urllib anyway, we might as well use it here to check the TLD
        url = urlparse(result.link)
        if url.netloc.endswith('.edu'):
            return result.link
    return results[0].link  # If none of the top 10 results were on a .edu domain just get the first one
