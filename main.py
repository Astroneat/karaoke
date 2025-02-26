from just_playback import Playback
import syncedlyrics

import lyrics_parser

import json
import os

SONG_NAME = "Life" # case sensitive!
OBJ_CONFIG_LEN = 2

with open('sounds-config.json') as f:
    configs = json.load(f)
if len(configs[SONG_NAME]) != OBJ_CONFIG_LEN:
    raise Exception(f"Configs for ${SONG_NAME} not found or incomplete!")

SONG_ARTIST = configs[SONG_NAME]["artist"]
SOUNDS_FOLDER = "sounds"
SONG_DIR = os.path.join(SOUNDS_FOLDER, configs[SONG_NAME]["file_name"])
SONG_BPM = configs[SONG_NAME]["bpm"]
SONG_OFFSET = configs[SONG_NAME]["offset"]

print(SONG_NAME, SONG_DIR, SONG_BPM, SONG_OFFSET)

LYRICS_FOLDER = "lyrics"
search_term = f"{SONG_NAME} {SONG_ARTIST}"
save_path = f'{os.path.join(LYRICS_FOLDER, SONG_NAME)}.lrc'

if not os.path.isfile(save_path):
    try:
        syncedlyrics.search(search_term, save_path=save_path, enhanced=True)
    except:
        print(f"Searching for ${search_term} failed!")

lrc_file = open(save_path)

lyric_timestamps = lyrics_parser.parse(lrc_file)
# print(lyric_timestamps)

# exit(0)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

seconds_per_beat = 60 / SONG_BPM
beat = -1
lyric_line, lyric_word = 0, 0

lyric_display = [[]]
max_display_lines = 6
is_update = True

playback = Playback()
playback.load_file(SONG_DIR)
playback.play()
while playback.active == True:
    if lyric_line < len(lyric_timestamps):
        curr_timestamp = lyric_timestamps[lyric_line][1][lyric_word]
        next_word = playback.curr_pos > curr_timestamp[0]
        if next_word:
            lyric_display[-1].append(curr_timestamp[1])
            is_update = True

            if lyric_word == len(lyric_timestamps[lyric_line][1]) - 1:
                lyric_word = 0
                lyric_line += 1
                lyric_display.append([])
            else:
                lyric_word += 1

    if is_update:
        os.system('clear')
        is_update = False
        if len(lyric_display[-1]) > 0 and len(lyric_display) > max_display_lines:
            lyric_display.pop(0)

        for lines in lyric_display:
            if len(lines) == 0:
                continue
            for word in lines:
                print(word, end='')
            print('')