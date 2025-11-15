import requests

def fetch_url_text(url: str, timeout=10):
    """
    Simple helper to fetch a URL and return text. Use carefully (rate limits).
    """
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text
