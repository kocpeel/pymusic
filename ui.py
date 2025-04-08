from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from player import MusicPlayer
import os


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
        self.setFixedSize(420, 180)
        self.setStyleSheet("background-color: black; color: lime;")

        font = QFont("Courier", 10, QFont.Bold)

        layout = QVBoxLayout()

        # --- Display Time ---
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Courier", 16, QFont.Bold))
        self.time_label.setStyleSheet("color: lime; background-color: black;")
        layout.addWidget(self.time_label)

        # --- Info labels ---
        self.song_label = QLabel("SONG: ---")
        self.song_label.setFont(font)

        self.bit_rate_label = QLabel("BITRATE: 0 kbps")
        self.bit_rate_label.setFont(font)

        self.mix_rate_label = QLabel("MIXRATE: 0 kHz")
        self.mix_rate_label.setFont(font)

        info_layout = QHBoxLayout()
        info_layout.addWidget(self.song_label)
        info_layout.addWidget(self.bit_rate_label)
        info_layout.addWidget(self.mix_rate_label)

        layout.addLayout(info_layout)

        # --- Volume slider ---
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: gray;
            }
            QSlider::handle:horizontal {
                background: lime;
                width: 10px;
            }
        """)
        layout.addWidget(self.volume_slider)

        # --- Buttons ---
        assets_path = "assets"
        self.play_button = QPushButton(QIcon(os.path.join(assets_path, "play.png")), "")
        self.pause_button = QPushButton(QIcon(os.path.join(assets_path, "pause.png")), "")
        self.stop_button = QPushButton(QIcon(os.path.join(assets_path, "stop.png")), "")
        self.next_button = QPushButton(QIcon(os.path.join(assets_path, "next.png")), "")
        self.prev_button = QPushButton(QIcon(os.path.join(assets_path, "prev.png")), "")
        self.shuffle_button = QPushButton(QIcon(os.path.join(assets_path, "shuffle.png")), "")
        self.loop_button = QPushButton(QIcon(os.path.join(assets_path, "loop.png")), "")

        buttons = [
            self.prev_button, self.play_button, self.pause_button,
            self.stop_button, self.next_button, self.shuffle_button, self.loop_button
        ]
        for btn in buttons:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("background-color: #222; color: white;")

        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)
        self.stop_button.clicked.connect(self.player.stop)
        self.next_button.clicked.connect(self.player.next_song)
        self.prev_button.clicked.connect(self.player.prev_song)
        self.shuffle_button.clicked.connect(self.toggle_shuffle)
        self.loop_button.clicked.connect(self.toggle_loop)

        btn_layout = QHBoxLayout()
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def set_volume(self):
        volume = self.volume_slider.value() / 100
        self.player.set_volume(volume)

    def update_song_info(self):
        info = self.player.get_current_song_info()
        self.song_label.setText(f"SONG: {info['title']}")
        self.bit_rate_label.setText(f"BITRATE: {info['bitrate']} kbps")
        self.mix_rate_label.setText(f"MIXRATE: {info['mixrate']} kHz")
        self.time_label.setText(self.player.get_current_time_str())

        # Auto-play next song when finished
        if not self.player.paused and self.player.is_playing and not self.is_song_playing():
            if self.player.loop_enabled:
                self.player.play()
            else:
                self.player.next_song()

    def is_song_playing(self):
        from pygame import mixer
        return mixer.music.get_busy()

    def toggle_shuffle(self):
        is_shuffle = self.player.toggle_shuffle()
        color = "green" if is_shuffle else "#222"
        self.shuffle_button.setStyleSheet(f"background-color: {color}; color: white;")

    def toggle_loop(self):
        is_looping = self.player.toggle_loop()
        color = "green" if is_looping else "#222"
        self.loop_button.setStyleSheet(f"background-color: {color}; color: white;")
