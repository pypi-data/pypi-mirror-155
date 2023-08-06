import sys


def url_for(base_url, endpoint):
    # Urljoin doesn't actually work correctly
    return f"{base_url.strip().rstrip('/')}/{endpoint.strip().lstrip('/')}"
