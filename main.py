from just_playback import Playback
from rich import print
import pytubefix
import syncedlyrics

import lyrics_parser

import os
import subprocess

# ----- Custom configs ----- #
SONG_NAME = ""

SEARCH_SONG = False
SONG_FILE = ""
SEARCH_LYRICS = False
LYRICS_FILE = ""

SEARCH_QUERY_DISPLAY = 5 # how many results to display (if SEARCH_SONG is True)

PAST_DISPLAY_LINES = 4 # how many lines will be displayed before the current one
FUTURE_DISPLAY_LINES = 1 # how many lines will be displayed after the current one

PAST_STYLE = "bold blue" # style of past lines
ACTIVE_STYLE = "bold blue" # current line: sung words
INACTIVE_STYLE = "dim cyan" # current line: unsung words
FUTURE_STYLE = "dim cyan" # future lines

# ----- Actual code ----- #

def refresh():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("\033[2J")

## ----- Preprocessing ----- ##

# Search for songs using pytubefix
if SEARCH_SONG:
    print(f"[bold]Displaying {SEARCH_QUERY_DISPLAY} results for \"{SONG_NAME}\":[/bold]")
    search_results = pytubefix.Search(SONG_NAME).videos

    # Display first few results
    for i in range(min(len(search_results), SEARCH_QUERY_DISPLAY)):
        yt = search_results[i]
        print(yt.title)

    print(f"[bold]Pick a song from the list (1-{SEARCH_QUERY_DISPLAY}): [bold]", end='')
    pick_idx = int(input()) - 1

    # Download user-selected song

    yt_obj = search_results[pick_idx]
    yts_obj = yt_obj.streams.get_audio_only()

    audio_name = yt_obj.title
    audio_file = ""

    if not os.path.isfile(os.path.join("sounds", audio_name + ".mp3")):
        print("[bold]Downloading...[/bold]")
        audio_file_m4a = yts_obj.download(output_path="sounds", skip_existing=True)
        base, ext = os.path.splitext(audio_file_m4a)
        audio_file = base + ".mp3"

        print("[bold]Converting...[/bold]")
        subprocess.run([
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-n', '-i', audio_file_m4a, audio_file
        ])
        print(f"Audio downloaded to \"{os.path.relpath(audio_file)}\"")
        if os.path.isfile(audio_file_m4a): 
            os.remove(audio_file_m4a)
    else:
        audio_file = os.path.join("sounds", audio_name + ".mp3")
        print(f"Found \"{audio_file}\" in sounds")
else:
    print(f"Skipped searching for \"{SONG_NAME}\"")
    if os.path.isfile(SONG_FILE):
        print(f"\"{SONG_FILE}\"'s existence verified")
        audio_file = SONG_FILE
    else:
        raise Exception(f"\"{SONG_FILE}\" not found")

# Download lyrics as .lrc file
if SEARCH_LYRICS:
    lrc_path = os.path.join('lyrics', f"{audio_name}.lrc")
    if not os.path.isfile(lrc_path):
        print(f"Searching for lyrics of \"{audio_name}\"...")
        syncedlyrics.search(audio_name, save_path=lrc_path, enhanced=True)
    else:
        print(f"Lyrics for \"{lrc_path}\" already exists in ./lyrics")

    lrc_file = open(lrc_path)
else:
    print(f"Skipped searching lyrics for \"{SONG_NAME}\"")
    if os.path.isfile(LYRICS_FILE):
        print(f"\"{LYRICS_FILE}\"'s existence verified")
        lrc_file = open(LYRICS_FILE)
    else:
        raise Exception(f"\"{LYRICS_FILE}\" not found")
    
lyrics_timestamps = lyrics_parser.parse(lrc_file) # do not underappreciate this line

# It's go time
input("Press any key to continue.")
refresh()

## ----- Display ----- ##
cur_line, cur_word = 0, -1
need_update = True
manual_offset = 0 # debug purposes

# Start playback and lyrics display loop
playback = Playback()
playback.load_file(audio_file)
playback.play()
while playback.playing:

    if cur_line < len(lyrics_timestamps):
        if cur_word + 1 < len(lyrics_timestamps[cur_line][1]):
            nxt_timestamp = lyrics_timestamps[cur_line][1][cur_word + 1][0]
        elif cur_line + 1 < len(lyrics_timestamps):
            nxt_timestamp = lyrics_timestamps[cur_line + 1][1][0][0]
        else:
            nxt_timestamp = float('inf')
        next_word = (playback.curr_pos + manual_offset) > nxt_timestamp

        if next_word:
            need_update = True
            if cur_word == len(lyrics_timestamps[cur_line][1]) - 1:
                cur_word = 0
                cur_line += 1
            else:
                cur_word += 1

    if need_update:
        refresh()
        need_update = False

        # Display past lines
        for l in range(max(0, cur_line - PAST_DISPLAY_LINES), cur_line):
            cur = ''.join([t[1] for t in lyrics_timestamps[l][1]])
            print(f"[{PAST_STYLE}]{cur}[/{PAST_STYLE}]")

        # Display current line
        for w in range(cur_word + 1):
            print(f"[{ACTIVE_STYLE}]{lyrics_timestamps[cur_line][1][w][1]}[/{ACTIVE_STYLE}]", end='')
        for w in range(cur_word + 1, len(lyrics_timestamps[cur_line][1])):
            print(f"[{INACTIVE_STYLE}]{lyrics_timestamps[cur_line][1][w][1]}[/{INACTIVE_STYLE}]", end='')
        print("")

        # Display future lines
        for l in range(cur_line + 1, min(len(lyrics_timestamps), cur_line + FUTURE_DISPLAY_LINES + 1)):
            cur = ''.join([t[1] for t in lyrics_timestamps[l][1]])
            print(f"[{FUTURE_STYLE}]{cur}[/{FUTURE_STYLE}]")
