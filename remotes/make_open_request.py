import logging
import requests

log = logging.getLogger("core")


url = ''

r = requests.get(url)

print(f"r.status_code: {r.status_code}")
print(f"r.text: {r.text}")
print(f"r.headers['content-type']: {r.headers['content-type']}")
