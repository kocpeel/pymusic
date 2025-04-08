import os
import random
import pygame
from mutagen.mp3 import MP3


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.music_folder = "music"
        self.playlist = []
        self.shuffled_playlist = []
        self.shuffle_enabled = False
        self.loop_enabled = False
        self.current_index = 0
        self.current_path = None
        self.paused = False
        self.is_playing = False
        self.volume = 0.5  # default

        self.load_songs(self.music_folder)
        pygame.mixer.music.set_volume(self.volume)

    def load_songs(self, folder):
        if not os.path.exists(folder):
            print(f"Folder '{folder}' nie istnieje.")
            return
        self.playlist = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(".mp3")
        ]
        self.shuffled_playlist = self.playlist.copy()
        random.shuffle(self.shuffled_playlist)

    def get_playlist(self):
        return self.shuffled_playlist if self.shuffle_enabled else self.playlist

    def play(self):
        playlist = self.get_playlist()
        if not playlist:
            return

        path = playlist[self.current_index]
        try:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                self.current_path = path
                self.is_playing = True
                self.paused = False
        except Exception as e:
            print(f"Error playing song: {e}")

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.paused = False

    def next_song(self):
        self.stop()
        playlist = self.get_playlist()
        self.current_index = (self.current_index + 1) % len(playlist)
        self.play()

    def prev_song(self):
        self.stop()
        playlist = self.get_playlist()
        self.current_index = (self.current_index - 1) % len(playlist)
        self.play()

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        if self.shuffle_enabled:
            current_song = self.get_playlist()[self.current_index]
            self.shuffled_playlist = self.playlist.copy()
            random.shuffle(self.shuffled_playlist)
            self.current_index = self.shuffled_playlist.index(current_song)
        else:
            current_song = self.get_playlist()[self.current_index]
            self.current_index = self.playlist.index(current_song)
        return self.shuffle_enabled

    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        return self.loop_enabled

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def get_current_song_info(self):
        path = self.get_playlist()[self.current_index]
        try:
            audio = MP3(path)
            bitrate = int(audio.info.bitrate / 1000)
            mixrate = int(audio.info.sample_rate / 1000)
            return {
                "title": os.path.basename(path),
                "bitrate": bitrate,
                "mixrate": mixrate
            }
        except Exception as e:
            print(f"Error getting song info: {e}")
            return {
                "title": "Unknown",
                "bitrate": 0,
                "mixrate": 0
            }

    def get_current_time_str(self):
        pos = pygame.mixer.music.get_pos()
        if pos == -1:
            return "00:00"
        seconds = pos // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
