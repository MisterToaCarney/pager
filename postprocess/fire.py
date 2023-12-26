from postprocess.flex_next import ParsedFlexPage
import re
from dataclasses import dataclass

part_re = re.compile("\(Part (\d+) of (\d+)\)")

@dataclass(frozen=True)
class FireFragment:
  address: str
  part_num: int
  of_num: int
  message: str
  timestamp: float

class FireDefragmenter:
  def __init__(self, disable_garbage_collection=False):
    self.fragments: dict[str, dict[int, FireFragment]] = {}
    self.disable_garbage_collection = disable_garbage_collection

  def _clean(self, current_timestamp: float):
    for address in list(self.fragments.keys()):
      for part_num in list(self.fragments[address].keys()):
        if current_timestamp - self.fragments[address][part_num].timestamp > 60:
          del self.fragments[address][part_num]
          if len(self.fragments[address]) == 0: del self.fragments[address]

  def all_fragments(self, address: str, of_num: int) -> list[FireFragment]:
    fragments = self.fragments[address]
    parts = []
    for fragment in fragments.values():
      if fragment.of_num != of_num: continue
      parts.append(fragment)
    return sorted(parts, key=lambda fragment: fragment.part_num)

  def defrag(self, message: str, address: str, current_timestamp: float) -> str | None:
    part_match = part_re.search(message)
    if not part_match: return message

    if not self.disable_garbage_collection:
      self._clean(current_timestamp)

    part_num = int(part_match[1])
    of_num = int(part_match[2])

    cleaned_message = part_re.sub("", message)
    fragment = FireFragment(address=address, part_num=part_num, of_num=of_num, message=cleaned_message, timestamp=current_timestamp)

    try: self.fragments[address][part_num] = fragment
    except KeyError: self.fragments[address] = {part_num: fragment}

    all_part_nums = list(range(1, of_num + 1))
    all_fragments = self.all_fragments(address, of_num)
    current_part_nums = [f.part_num for f in all_fragments]
    
    if all_part_nums == current_part_nums:
      defragmented_message = ''.join([f.message for f in all_fragments])
      del self.fragments[address]
      return defragmented_message
    else:
      return None

defragger = FireDefragmenter()

def defrag_fire_page(flex_page: ParsedFlexPage) -> ParsedFlexPage | None:
  defragmented_message = defragger.defrag(flex_page.message, flex_page.address, flex_page.date.timestamp())
  if defragmented_message is None:
    return None
  else:
    return ParsedFlexPage(
      flex_match=flex_page.flex_match,
      date=flex_page.date,
      address=flex_page.address,
      message=defragmented_message
    )
  
  

  
