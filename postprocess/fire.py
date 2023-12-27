from postprocess.flex_next import ParsedFlexPage
import re
from dataclasses import dataclass

part_re = re.compile("\(Part (\d+) of (\d+)\)")
bracket_re = re.compile("\(.*?\)")
fire_assignment_re = re.compile("^ *(ADV|AIRH|AIRL|AMB2FIR|EXERCISE|FIREALM|FIRETEST|HAZ|HAZGAS|HAZFLAM|LINERESC|MCDEM|MED|MEDFR|MIN|MVC|MVCHEVY|MVCRESC|NAT1|NAT2|NAT3|NE|NOT|POL2FIR|RESC|SHIP|SPRNKLR|STNCALL|STRU|TEVAC|USAR|WATERESC|VEG) +(.*?)\. *(?:\.(.*)\.)? *#F(\d+)")
xstreet_re = re.compile("\(XStr *(.+)\)")
units_re = re.compile("^ *\(([\w\d, ]+)\)")

@dataclass(frozen=True)
class FireFragment:
  address: str
  part_num: int
  of_num: int
  message: str
  timestamp: float

@dataclass(frozen=True)
class FireAssignment:
  message: str
  units: list[str]
  type: str
  address: str
  xstreet: str
  details: str
  job_id: int

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
  
def parse_fire_assignment(message: str) -> FireAssignment | None:
  base_message = bracket_re.sub("", message)
  fire_assignment_match = fire_assignment_re.search(base_message)
  if fire_assignment_match is None: return None

  units_match = units_re.search(message)
  if units_match:
    units_str = units_match[1]
    units = [u.strip() for u in units_str.split(",")]
  else:
    units = []
  
  xstreet_match = xstreet_re.search(message)
  if xstreet_match: 
    xstreet = xstreet_match[1]
  else: 
    xstreet = ""

  return FireAssignment(
    message=message,
    units=units,
    type=fire_assignment_match[1],
    address=fire_assignment_match[2],
    details=fire_assignment_match[3],
    job_id=int(fire_assignment_match[4]),
    xstreet=xstreet
  )
   


  
