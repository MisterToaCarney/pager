import postprocess.flex_next as flex
import postprocess.date

def begin(line: bytes):
    print("----")
    text = line.decode()
    print("DEBUG", text, end='')

    date = postprocess.date.parse_date(text)
    if date is None: return

    parsed_flex = flex.parse(text, date)
    print(parsed_flex)
    