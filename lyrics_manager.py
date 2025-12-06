import re
from pathlib import Path

class LyricsManager:
    def __init__(self):
        self.lyrics = []
        self.metadata = {}
        self.current_line = -1

    def load_lrc(self, lrc_path):
        self.lyrics = []

        with open(lrc_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Metadataaa
                if line.startswith('[') and ':' in line[:10]:
                    match = re.match(r'\[([a-zA-Z]+):(.+)\]', line)
                    if match:
                        self.metadata[match.group(1)] = match.group(2)
                        continue

                # Lines with timestampp
                matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](.+)', line)
                for match in matches:
                    minutes, seconds, centiseconds, text = match
                    timestamp = int(minutes) * 60 + int(seconds) + int(centiseconds) / 100
                    self.lyrics.append((timestamp, text.strip()))

        self.lyrics.sort(key=lambda x: x[0])

    def get_current_line(self, current_time):
        for i, (timestamp, text) in enumerate(self.lyrics):
            if timestamp > current_time:
                return max(0, i - 1)
        return len(self.lyrics) - 1


if __name__ == "__main__":
    print("Ი︵𐑼 Testing LyricsManager Ი︵𐑼")

    lm = LyricsManager()

    lm.load_lrc("./lyrics/Cráneo x $kyhook - Ciencia.lrc")

    print(f" Metadata: {lm.metadata}")
    print(f" {len(lm.lyrics)} charged lines\n")

    for time in [0, 25, 50, 100, 150]:
        index = lm.get_current_line(time)
        if index >= 0:
            timestamp, text = lm.lyrics[index]
            print(f"[{time}s] -> {text}")
