import re
from dataclasses import dataclass
import datetime
import copy

flex_re = re.compile("FLEX_NEXT\|(\d+)\/(\d+)\|(\d+\.\d+\.\w)\|(\d+)\|(\w{2})\|(\d)\|(\w+)\|(\d)\.(\d)\.(K|F|C)\|(.*)")

@dataclass
class FragmentItem:
    text: str
    time: float

@dataclass
class ParsedFlexPage:
    flex_match: re.Match[str]
    date: datetime.datetime
    address: str
    message: str

class FlexDefragmenter:
    def __init__(self) -> None:
        self.fragment_messages = {}

    def _clean(self, current_timestamp) -> None:
        for addr, frag_item in list(self.fragment_messages.items()):
            if current_timestamp - frag_item.time > 10: del self.fragment_messages[addr]
        
    def defrag(self, address, message, flag, timestamp) -> str | None:
        self._clean(timestamp)
        if flag == "K": return message
        elif flag == "F":
            self.fragment_messages[address] = FragmentItem(text=message, time=timestamp)
            return None
        elif flag == "C":
            if not address in self.fragment_messages: return None
            else:
                self.fragment_messages[address].text += message
                output = copy.copy(self.fragment_messages[address].text)
                del self.fragment_messages[address]
                return output

defragger = FlexDefragmenter()

def parse(text: str, message_date: datetime.datetime) -> ParsedFlexPage | None:
    flex_match = flex_re.search(text)
    if flex_match is None: return None
   
    frag_flag = flex_match[10]
    address = flex_match[4]
    message = flex_match[11]

    defragged = defragger.defrag(address, message, frag_flag, message_date.timestamp())
    if defragged:
        return ParsedFlexPage(
            flex_match=flex_match,
            date=message_date,
            address=address,
            message=defragged
        )
    else: return None

