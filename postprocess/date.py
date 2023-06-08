import re
from datetime import datetime

date_re = re.compile(" (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):")

def parse(text) -> datetime | None:
    date_match = date_re.search(text)
    if date_match is None: return None
    date = datetime.strptime(date_match[1], "%Y-%m-%d %H:%M:%S")
    date = date.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return date
