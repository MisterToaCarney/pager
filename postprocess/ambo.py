import re
from dataclasses import dataclass

# Job assignment
# (\w+) *(PTS|GREEN|ORANGE|RED|PURPLE|NOTIFICATION|AIR TRANSFER|AIR|PRIVATE HIRE) *(\d?) *(\w+) *(.+) *; *Flat\/Unit:(.+?[A-Z ]{3,})(?=\W)

priority_codes = [
    "TRIAGE",
    "ON HOLD",
    "NOTIFICATION",
    "AIR TRANSFER",
    "AIR",
    "PRIVATE HIRE",
    "PTS",
    "GREY",
    "GREEN 2",
    "GREEN 1",
    "GREEN",
    "ORANGE 2",
    "ORANGE 1",
    "ORANGE",
    "RED 2",
    "RED 1",
    "RED",
    "PURPLE"
]

def generate_regex():
    codes_regex_str = ""
    for code in priority_codes:
        codes_regex_str += code
        codes_regex_str += "|"
    codes_regex_str = codes_regex_str[:-1]

    regex_str = f"([A-Z0-9]+) *({codes_regex_str}) *(\w+) *(.+) *[;:] *Flat\/Unit:(.+?[A-Z ]{{3,}})(?=\W|$)"
    return re.compile(regex_str)

@dataclass
class JobAssignment:
    message: str
    match: re.Match[str]
    unit: str
    priority: str
    type_code: str
    type_plaintext: str
    address: str

job_assignment_re = generate_regex()

def parse_job_assignment(message: str) -> JobAssignment | None:
    job_match = job_assignment_re.search(message)
    if job_match is None: return None

    return JobAssignment(
        message=message,
        match=job_match,
        unit=job_match[1],
        priority=job_match[2],
        type_code=job_match[3],
        type_plaintext=job_match[4],
        address=job_match[5]
    )
