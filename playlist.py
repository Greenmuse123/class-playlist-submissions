"""A small class playlist that saves song submissions between sessions."""

import json
from pathlib import Path


PLAYLIST_FILE = Path(__file__).with_name("playlist.json")


# Subsystem 1: creates a song entry.
def create_song(song):
    return song.strip() or "No song entered"


# Subsystem 2: creates an artist entry.
def create_artist(artist):
    return artist.strip() or "No artist entered"


# Subsystem 3: creates an album entry.
def create_album(album):
    return album.strip() or "No album entered"


# Combines the three subsystems into one entry.
def create_playlist_entry(song, artist, album):
    return {
        "Song": create_song(song),
        "Artist": create_artist(artist),
        "Album": create_album(album),
    }


def submit_song(playlist, song, artist, album=""):
    """Validate a submission, add it to the list, and return the new entry."""
    if not song.strip() or not artist.strip():
        raise ValueError("A song title and artist are required.")

    for entry in playlist:
        same_song = entry["Song"].casefold() == song.strip().casefold()
        same_artist = entry["Artist"].casefold() == artist.strip().casefold()
        if same_song and same_artist:
            raise ValueError("That song by that artist is already in the playlist.")

    entry = create_playlist_entry(song, artist, album)
    playlist.append(entry)
    return entry


def save_playlist(playlist, path=PLAYLIST_FILE):
    """Write a temporary file first to avoid partially replacing saved data."""
    path = Path(path)
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(playlist, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    temporary_path.replace(path)


def load_playlist(path=PLAYLIST_FILE):
    path = Path(path)
    if not path.exists():
        return []

    playlist = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(playlist, list):
        raise ValueError("The saved playlist must be a list.")
    for entry in playlist:
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(field), str)
            for field in ("Song", "Artist", "Album")
        ):
            raise ValueError("A saved entry is missing a valid song, artist, or album.")
    return playlist


def display_playlist(playlist):
    if not playlist:
        print("The playlist is empty. Submit the first song!")
        return

    print("\n--- Class Playlist ---")
    for number, entry in enumerate(playlist, start=1):
        print(f"{number}. {entry['Song']} by {entry['Artist']} | {entry['Album']}")


def music_system():
    try:
        playlist = load_playlist()
    except (OSError, ValueError) as error:
        print(f"Could not open the saved playlist: {error}")
        print("Check playlist.json before trying again. Your file was not changed.")
        return

    print("Welcome to the Class Playlist!")
    while True:
        print("\n1. Submit a song\n2. View the playlist\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            song = input("Song title: ")
            artist = input("Artist: ")
            album = input("Album (optional): ")
            # Save a candidate list before changing the active playlist.
            updated_playlist = playlist.copy()
            try:
                entry = submit_song(updated_playlist, song, artist, album)
                save_playlist(updated_playlist)
            except (ValueError, OSError) as error:
                print(f"Submission not saved: {error}")
            else:
                playlist = updated_playlist
                print(f"Added {entry['Song']} by {entry['Artist']} to the playlist!")
        elif choice == "2":
            display_playlist(playlist)
        elif choice == "3":
            print("Thanks for sharing your music!")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    music_system()
