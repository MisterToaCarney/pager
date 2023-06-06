import postprocess.flex_next as flex
import postprocess.pocsag as pocsag
import postprocess.date

def begin(line: bytes):
    print("----")
    text = line.decode()
    print("DEBUG", text, end='')

    date = postprocess.date.parse_date(text)
    if date is None: return

    parsed_pocsag = pocsag.parse(text, date)
    parsed_flex = flex.parse(text, date)
    print("FLEX RESULT", parsed_flex)
    print("POCSAG RESULT", parsed_pocsag)
    