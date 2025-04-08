import os
import pygame
import random

class MusicPlayer:
    def __init__(self, music_folder="music"):
        self.music_folder = os.path.abspath(music_folder)
        self.playlist = [os.path.join(self.music_folder, f) for f in os.listdir(self.music_folder) if f.endswith(".mp3")]
        self.current_index = 0
        self.is_playing = False
        self.is_looping = False
        self.shuffle = False
        self.paused = False

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

    def play(self):
        try:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                return

            if self.playlist:
                song_path = self.playlist[self.current_index]
                print(f"Playing: {song_path}")
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(-1 if self.is_looping else 0)
                self.is_playing = True
                self.paused = False
        except Exception as e:
            print(f"Error playing song: {e}")

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.paused = False

    def next_song(self):
        self.stop()
        if self.shuffle:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_song(self):
        self.stop()
        if self.shuffle:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def restart_song(self):
        self.stop()
        self.play()

    def set_volume(self, volume):  # volume: 0.0 to 1.0
        pygame.mixer.music.set_volume(volume)

    def get_current_song_info(self):
        if self.playlist:
            song = os.path.basename(self.playlist[self.current_index])
            return {
                "title": song,
                "bitrate": "128 kbps",
                "mixrate": "44 kHz"
            }
        return {
            "title": "No Song",
            "bitrate": "0 kbps",
            "mixrate": "0 kHz"
        }

    def toggle_loop(self):
        self.is_looping = not self.is_looping
        return self.is_looping

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        return self.shuffle
