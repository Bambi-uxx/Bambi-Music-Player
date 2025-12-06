from pathlib import Path
from mutagen import File

class Playlist:
    def __init__(self):
        self.songs = []
        self.current_index = 0

    def load_from_folder(self, folder_path):
        folder = Path(folder_path)
        extensions = ['.mp3', '.wav', '.ogg', '.flac']

        for ext in extensions:
            for file in folder.glob(f'*{ext}'):
                metadata = self.get_metadata(file)
                self.songs.append({
                    'path': str(file),
                    'title': metadata.get('title', file.stem),
                    'artist': metadata.get('artist', 'Desconocido')
                })

    def get_metadata(self, file_path):
        try:
            audio = File(file_path)
            default_name = Path(file_path).stem
            return {
                'title': audio.get('TIT2', [file_path.stem])[0],
                'artist': audio.get('TPE1', ['Desconocido'])[0]
            }
        except:
            return {}




if __name__ == "__main__":
    from config import MUSIC_FOLDER

    print("Testing Playlist ₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ ")
    playlist = Playlist()
    playlist.load_from_folder(MUSIC_FOLDER)

    print(f"{len(playlist.songs)}  ‧₊˚♪ songs found 𝄞₊˚⊹:")
    for i, song in enumerate(playlist.songs):
        print(f" {i+1}. {song['artist']} - {song['title']}")
