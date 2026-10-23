# Class Playlist Submissions

A Python class project that lets people contribute song suggestions to a class playlist. A user can submit a song, view all submissions, and return later without losing the playlist.

This is a terminal application. People using the same copy of the program share its local playlist. Separate computers have separate playlists; GitHub hosts the source code, not a live submission form. The program stores song information and does not upload audio, play music, or connect to Spotify.

## Features

- Submit a song title, artist, and optional album.
- Reject missing song titles or artist names, including whitespace-only input.
- Prevent duplicate song-and-artist pairs regardless of capitalization.
- View a numbered playlist.
- Save submissions to `playlist.json` beside the program.
- Test the original subsystems and the complete submission workflow with `unittest`.

## Run the project

Requires Python 3. No third-party packages are needed.

```sh
git clone https://github.com/Greenmuse123/class-playlist-submissions.git
cd class-playlist-submissions
python playlist.py
```

On Windows, use `py` if `python` is unavailable. On macOS or Linux, you may need `python3`.

Example interaction:

```text
Welcome to the Class Playlist!

1. Submit a song
2. View the playlist
3. Exit
Choose an option: 1
Song title: Blinding Lights
Artist: The Weeknd
Album (optional): After Hours
Added Blinding Lights by The Weeknd to the playlist!
```

Choose option 2 to view submissions and option 3 to exit. Submissions save immediately. The local data file is ignored by Git so personal submissions are not published with the code.

## How the original code fits

| Function | Responsibility |
| --- | --- |
| `create_song` | Clean the song title or return the original empty-field message. |
| `create_artist` | Clean the artist name or return the original empty-field message. |
| `create_album` | Clean the album name or return the original empty-field message. |
| `create_playlist_entry` | Combine the three subsystems into a dictionary. |
| `submit_song` | Validate required fields, check for duplicates, and add an entry. |
| `save_playlist` / `load_playlist` | Keep submissions between sessions using JSON. |
| `display_playlist` | Print the entries in a readable format. |
| `music_system` | Run the menu and handle user input. |

The original empty-field messages are preserved. The submission function validates required fields before calling the original subsystems, so an empty title or artist cannot become a submitted entry. A missing album is allowed.

## Run the tests

```sh
python -m unittest -v
```

Tests run separately from the application so testing does not open interactive prompts. File tests use temporary directories and do not change your saved playlist.

## Partner branch assignment

The initial project uses `master` to match the assignment. Each partner must independently implement a change on their own branch and merge it into `master`. These partner contributions are still to be completed.

Before starting, the repository owner should invite the other partner through GitHub's repository **Settings > Collaborators**. Each partner should clone the repository on their own machine and configure Git with their own name and email.

Possible independent contributions:

- Partner 1: add `search_playlist(playlist, query)` and a menu option that searches titles and artist names.
- Partner 2: add `playlist_summary(playlist)` and a menu option that reports the number of songs and unique artists.

Each partner can use this workflow, replacing `partner-1-search` with their own descriptive branch name:

```sh
git switch master
git pull origin master
git switch -c partner-1-search
# Make your function change and add a test for its behavior.
python -m unittest -v
git add playlist.py test_playlist.py
git commit -m "Add playlist search"
git push -u origin partner-1-search
```

Open a pull request on GitHub with `master` as the base branch. Review the change and choose **Create a merge commit** to retain the branch history. Both partners may touch the menu, so resolve any merge conflict and rerun tests before merging. Each partner must finish and merge their own contribution.

After merging, update your local copy:

```sh
git switch master
git pull origin master
```

Before submission, confirm that both partners' changes are merged, the tests pass on `master`, and the README describes the final behavior. Submit this repository link:

https://github.com/Greenmuse123/class-playlist-submissions
