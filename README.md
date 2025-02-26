# Karaoke

## Installations

- Install the required packages:
```py
pip install -r requirements.txt
```

## Usage

- Grab yourself a file of the song you want to play and put it in `sounds` folder.

- Create/Edit `sounds-config.json` in the same directory as `main.py`. Each song is structured as follows:
```jsonc
{
    // Capitalised w/ whitespace is recommended
    // E.g. "As The World Caves In"
    "<song-name>": {
        "artist": "<artist-name>",
        "file_name": "<audio-file-name>.<whatever-ext-ur-audio-is>"
    }
}
```

- Change `SONG_NAME` in `main.py` to whatever song you want to play, and enjoy!

## Issues

- Some songs have really badly synced lyrics, I can't really fix this since it's the lyric providers' fault, not mine.
- Please don't use songs with no lyrics, I haven't tested this yet...
- Please report any issues you see with the program, I will *try my best* to fix it.