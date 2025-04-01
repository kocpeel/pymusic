from pydub import AudioSegment
from pydub.playback import play
import os
import random
import threading

class MusicPlayer:
    def __init__(self, music_folder="music"):
        self.music_folder = music_folder
        self.playlist = [os.path.join(self.music_folder, f) for f in os.listdir(self.music_folder) if f.endswith(".mp3")]
        self.current_index = 0
        self.shuffle_mode = False
        self.loop_mode = False
        self.current_song = None
        self.is_playing = False

    def play(self):
        try:
            if self.playlist:
                song_path = self.playlist[self.current_index]
                self.current_song = AudioSegment.from_file(song_path, format="mp3")
                self.is_playing = True
                threading.Thread(target=play, args=(self.current_song,), daemon=True).start()
        except Exception as e:
            print(f"Error playing song: {e}")

    def stop(self):
        self.is_playing = False
        self.current_song = None

    def next_song(self):
        self.current_index = (self.current_index + 1) % len(self.playlist) if not self.shuffle_mode else random.randint(0, len(self.playlist) - 1)
        self.play()

    def prev_song(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode

    def toggle_loop(self):
        self.loop_mode = not self.loop_mode

    def get_song_info(self):
        if self.playlist:
            filename = os.path.basename(self.playlist[self.current_index])
            return filename, "128 kbps", "44 kHz"
        return "No Song", "0 kbps", "0 kHz"
