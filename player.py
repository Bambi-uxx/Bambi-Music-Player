import pygame
from pygame import mixer

class MusicPlayer:
    def __init__(self):
        mixer.init()
        self.current_song = None
        self.is_playing = False
        self.volume = 0.7

    def load(self, song_path):
        mixer.music.load(song_path)
        self.current_song = song_path

    def play(self):
        mixer.music.play()
        self.is_playing = True

    def pause(self):
        mixer.music.pause()
        self.is_playing = False

    def unpause(self):
        mixer.music.unpause()
        self.is_playing = True

    def stop(self):
        mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        mixer.music.set_volume(self.volume)

    def get_pos(self):
        return mixer.music.get_pos() / 1000.0
