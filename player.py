import pygame
from pygame import mixer

class MusicPlayer:
    def __init__(self):
        mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
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




if __name__ == "__main__":
    print("Testing MusicPlayer (˶˃ ᵕ ˂˶) ...")
    player = MusicPlayer()
    print(f"Player done. Volumen: {player.volume}")

    # Pon el nombre de tu canción aquí:
    player.load("./music/Cráneo x $kyhook - Ciencia.mp3")
    print("Song Loaded ❤︎")

    player.play()
    print("Playing ദ്ദി ˉ͈̀꒳ˉ͈́ )✧ ...")
    input("Press ENTER to stop... ◝(ᵔᗜᵔ)◜ ")
    player.stop()
