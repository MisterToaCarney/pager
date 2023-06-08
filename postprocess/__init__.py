import postprocess.date
import postprocess.flex_next as flex
import postprocess.pocsag as pocsag
import postprocess.ambo as ambo

def begin(line: bytes):
    print("----")
    text = line.decode()
    print("DEBUG", text, end='')

    date = postprocess.date.parse(text)
    if date is None: return

    parsed_pocsag = pocsag.parse(text, date)
    parsed_flex = flex.parse(text, date)
    print("FLEX RESULT", parsed_flex)
    print("POCSAG RESULT", parsed_pocsag)

    if parsed_pocsag: job = ambo.parse_job_assignment(parsed_pocsag.message)
    elif parsed_flex: job = ambo.parse_job_assignment(parsed_flex.message)
    else: job = None

    print("JOB", job)
