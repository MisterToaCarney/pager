import re
from dataclasses import dataclass
import datetime

pocsag_re = re.compile("(POCSAG\d+): +Address: +(\d+) +Function: +(\d+) +(\w+): +(.+)")

# ch1: 2023-06-06 15:19:43: POCSAG1200: Address:  725237  Function: 3  Alpha:   TAIH1 ORANGERESP4 F2F AMBULANCE ; Flat/Unit:21 /2 MASONIC DR WHANGANUI EAST<ETX><ETX>

@dataclass
class ParsedPocsagPage():
    match: re.Match[str]
    message: str
    date: datetime.datetime



def parse(text, date) -> ParsedPocsagPage | None:
    pocsag_match = pocsag_re.search(text)
    if pocsag_match is None: return None

    message = pocsag_match[5]

    return ParsedPocsagPage(match=pocsag_match, message=message, date=date)