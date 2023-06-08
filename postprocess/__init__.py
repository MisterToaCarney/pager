import postprocess.date
import postprocess.flex_next as flex
import postprocess.pocsag as pocsag
import postprocess.ambo as ambo

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
    print("RAW", text)
    
    parsed_page = parse_page(text)
    if not parsed_page: return
    print("PAGE", parsed_page)
    page_ref = await uplink.add_page(parsed_page)
   
    job = ambo.parse_job_assignment(parsed_page.message)
    if not job: return 
    print("JOB", job)
    job_ref = await uplink.add_job_assignment(parsed_page.date, page_ref, job)