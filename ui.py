from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from player import MusicPlayer
import os
import pygame


class MusicPlayerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        self.init_ui()
        self.update_song_info()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_song_info)
        self.timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.song_label = QLabel("No Song")
        self.bit_rate_label = QLabel("Bitrate: 0 kbps")
        self.mix_rate_label = QLabel("Mixrate: 0 kHz")

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        assets_path = "assets"

        self.play_button = QPushButton(QIcon(os.path.join(assets_path, "play.png")), "")
        self.pause_button = QPushButton(QIcon(os.path.join(assets_path, "pause.png")), "")
        self.stop_button = QPushButton(QIcon(os.path.join(assets_path, "stop.png")), "")
        self.next_button = QPushButton(QIcon(os.path.join(assets_path, "next.png")), "")
        self.prev_button = QPushButton(QIcon(os.path.join(assets_path, "prev.png")), "")
        self.shuffle_button = QPushButton(QIcon(os.path.join(assets_path, "shuffle.png")), "")
        self.loop_button = QPushButton(QIcon(os.path.join(assets_path, "loop.png")), "")

        # Podpięcie przycisków do metod interfejsu UI
        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)
        self.stop_button.clicked.connect(self.player.stop)
        self.next_button.clicked.connect(self.player.next_song)
        self.prev_button.clicked.connect(self.player.prev_song)
        self.shuffle_button.clicked.connect(self.toggle_shuffle)
        self.loop_button.clicked.connect(self.toggle_loop)

        layout.addWidget(self.song_label)
        layout.addWidget(self.bit_rate_label)
        layout.addWidget(self.mix_rate_label)
        layout.addWidget(self.volume_slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.loop_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_volume(self):
        volume = self.volume_slider.value() / 100.0
        self.player.set_volume(volume)

    def update_song_info(self):
        info = self.player.get_current_song_info()
        title = info["title"]
        bitrate = info["bitrate"]
        mixrate = info["mixrate"]
        self.song_label.setText(f"Song: {title}")
        self.bit_rate_label.setText(f"Bitrate: {bitrate}")
        self.mix_rate_label.setText(f"Mixrate: {mixrate}")

        # Automatyczne przejście do następnej piosenki, jeśli utwór się skończył,
        # a piosenka nie jest zatrzymana ani zapauzowana.
        if self.player.is_playing and not pygame.mixer.music.get_busy() and not self.player.paused:
            self.player.next_song()

    def toggle_shuffle(self):
        is_shuffle = self.player.toggle_shuffle()
        color = "green" if is_shuffle else ""
        self.shuffle_button.setStyleSheet(f"background-color: {color}")

    def toggle_loop(self):
        is_looping = self.player.toggle_loop()
        color = "green" if is_looping else ""
        self.loop_button.setStyleSheet(f"background-color: {color}")
