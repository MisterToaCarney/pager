from postprocess.regex_parsers import date_re
from datetime import datetime

def parse_date(text) -> datetime | None:
    date_match = date_re.search(text)
    if date_match is None: return None
    date = datetime.strptime(date_match[1], "%Y-%m-%d %H:%M:%S")
    return date
