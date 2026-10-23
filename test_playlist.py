"""Run with: python -m unittest -v"""

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from playlist import (
    create_song, create_artist, create_album, create_playlist_entry,
    submit_song, save_playlist, load_playlist, music_system,
)


class TestMusicPlaylist(unittest.TestCase):
    def test_create_song(self):
        self.assertEqual(create_song("Blinding Lights"), "Blinding Lights")

    def test_empty_song(self):
        self.assertEqual(create_song(""), "No song entered")

    def test_create_artist(self):
        self.assertEqual(create_artist("The Weeknd"), "The Weeknd")

    def test_empty_artist(self):
        self.assertEqual(create_artist(""), "No artist entered")

    def test_create_album(self):
        self.assertEqual(create_album("After Hours"), "After Hours")

    def test_empty_album(self):
        self.assertEqual(create_album(""), "No album entered")

    def test_complete_playlist_entry(self):
        self.assertEqual(
            create_playlist_entry("Blinding Lights", "The Weeknd", "After Hours"),
            {"Song": "Blinding Lights", "Artist": "The Weeknd", "Album": "After Hours"},
        )

    def test_submission_trims_spaces_and_allows_missing_album(self):
        playlist = []
        entry = submit_song(playlist, "  Blinding Lights  ", " The Weeknd ", "  ")
        self.assertEqual(playlist, [entry])
        self.assertEqual(entry["Song"], "Blinding Lights")
        self.assertEqual(entry["Artist"], "The Weeknd")
        self.assertEqual(entry["Album"], "No album entered")

    def test_required_fields_do_not_add_invalid_entries(self):
        for song, artist in [("", "Artist"), ("Song", ""), ("   ", "Artist")]:
            with self.subTest(song=song, artist=artist):
                playlist = []
                with self.assertRaises(ValueError):
                    submit_song(playlist, song, artist)
                self.assertEqual(playlist, [])

    def test_duplicate_is_rejected_regardless_of_case_or_outer_spaces(self):
        playlist = []
        submit_song(playlist, "Blinding Lights", "The Weeknd")
        with self.assertRaises(ValueError):
            submit_song(playlist, " blinding lights ", "THE WEEKND")
        self.assertEqual(len(playlist), 1)

    def test_same_title_by_different_artists_is_allowed(self):
        playlist = []
        submit_song(playlist, "Hello", "Adele")
        submit_song(playlist, "Hello", "Lionel Richie")
        self.assertEqual(len(playlist), 2)

    def test_save_and_load(self):
        playlist = []
        submit_song(playlist, "Déjà Vu", "Example Artist")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "playlist.json"
            self.assertEqual(load_playlist(path), [])
            save_playlist(playlist, path)
            self.assertEqual(load_playlist(path), playlist)
            submit_song(playlist, "Another Song", "Another Artist")
            save_playlist(playlist, path)
            self.assertEqual(load_playlist(path), playlist)

    def test_invalid_saved_data_is_rejected_and_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "playlist.json"
            for content in ["broken json", "{}", '[{"Song": "Hello"}]', "[1]"]:
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_playlist(path)
                    self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_menu_submit_view_and_exit(self):
        output = StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "playlist.json"
            with patch("playlist.load_playlist", side_effect=lambda: load_playlist(path)), \
                 patch("playlist.save_playlist", side_effect=lambda data: save_playlist(data, path)), \
                 patch("builtins.input", side_effect=["1", "Hello", "Adele", "25", "2", "3"]), \
                 redirect_stdout(output):
                music_system()
            self.assertEqual(load_playlist(path)[0]["Song"], "Hello")
        self.assertIn("Added Hello by Adele", output.getvalue())
        self.assertIn("1. Hello by Adele | 25", output.getvalue())

    def test_failed_save_does_not_report_success_or_change_playlist(self):
        playlist = []
        output = StringIO()
        with patch("playlist.load_playlist", return_value=playlist), \
             patch("playlist.save_playlist", side_effect=OSError("Disk is full")), \
             patch("builtins.input", side_effect=["1", "Hello", "Adele", "", "2", "3"]), \
             redirect_stdout(output):
            music_system()
        self.assertEqual(playlist, [])
        self.assertIn("Submission not saved", output.getvalue())
        self.assertIn("The playlist is empty", output.getvalue())


if __name__ == "__main__":
    unittest.main()
