import postprocess.date
import postprocess.flex_next as flex
import postprocess.pocsag as pocsag
import postprocess.ambo as ambo
import postprocess.fire as fire

from postprocess.flex_next import ParsedFlexPage

import uplink

def parse_page(text):
    date = postprocess.date.parse(text)
    if date is None: return None

    parsed_pocsag = pocsag.parse(text, date)
    parsed_flex = flex.parse(text, date)

    if parsed_pocsag: return parsed_pocsag
    elif parsed_flex: return parsed_flex
    else: return None

async def begin(line: bytes):
    print("----")
    text = line.decode()
    print("RAW", text, end="")
    
    parsed_page = parse_page(text)
    if isinstance(parsed_page, ParsedFlexPage):
        parsed_page = fire.defrag_fire_page(parsed_page)

    if not parsed_page: return
    # print("PAGE", parsed_page)

    if (not parsed_page.message.startswith("This is a test periodic page")):
        page_ref = await uplink.add_page(parsed_page)

    fire_assignment = fire.parse_fire_assignment(parsed_page.message)
    if fire_assignment:
        print("FIRE_JOB", fire_assignment)
        # TODO fire uplink

    ambo_assignment = ambo.parse_job_assignment(parsed_page.message)
    if ambo_assignment:
        print("AMBO_JOB", ambo_assignment)
        job_ref = await uplink.add_job_assignment(parsed_page.date, page_ref, ambo_assignment)