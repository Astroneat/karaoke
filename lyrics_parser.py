import pylrc
import re

enhanced_lrc_pattern = re.compile(r'\<(\d{2}):(\d{2}\.\d{2,3})\> ([^\s+]+|[ ])')

def is_enhanced_lrc(lrc_content):
    lines = pylrc.parse(lrc_content)
    for line in lines:
        matches = enhanced_lrc_pattern.findall(line.text)
        if len(matches) > 1:
            return True
    return False


def parse(lrc_file): 
    lrc_content = lrc_file.read()
    if is_enhanced_lrc(lrc_content):
        return enhanced_parse(lrc_content)
    return basic_parse(lrc_content)

def basic_parse(lrc_content):
    timestamps = []
    lrc_content = pylrc.parse(lrc_content)
    for line in lrc_content:
        timestamps.append((line.time, [(line.time, line.text.strip())]))
    return timestamps

def enhanced_parse(lrc_content):
    timestamps = []
    lrc_content = pylrc.parse(lrc_content)
    for line in lrc_content:
        line_timestamps = []
        matches = enhanced_lrc_pattern.findall(line.text)
        for match in matches:
            minutes = int(match[0])
            seconds = float(match[1])
            timestamp = minutes * 60 + seconds
            word = match[2]
            line_timestamps.append((timestamp, word))
        timestamps.append((line.time, line_timestamps))
    return timestamps