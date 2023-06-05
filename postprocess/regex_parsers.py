import re

job_re = re.compile("(\w+) *(PTS|GREEN|ORANGE|RED|PURPLE|NOTIFICATION|AIR TRANSFER|PRIVATE HIRE) *(\d?) *(\w+) *(.+) *; *Flat\/Unit:([\w&\/\- ]+[A-Z]{2,})")
flex_re = re.compile("FLEX_NEXT\|(\d+)\/(\d+)\|(\d+\.\d+\.\w)\|(\d+)\|(\w{2})\|(\d)\|(\w+)\|(\d)\.(\d)\.(K|F|C)\|(.*)")
date_re = re.compile(" (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):")