import pygame
from pathlib import Path
from config import *
from player import MusicPlayer
from playlist import Playlist
from lyrics_manager import LyricsManager

#Pygame setupp
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = pygame.display.set_caption("Bambi Music Player ૮₍ ˃ ⤙ ˂ ₎ა")
clock = pygame.time.Clock()
running = True

player = MusicPlayer()
lyrics_manager = LyricsManager()
playlist = Playlist()

playlist.load_from_folder(MUSIC_FOLDER)

if len(playlist.songs) > 0:
    first_song = playlist.songs[0]
    player.load(first_song['path'])
    player.play()

    lrc_path = LYRICS_FOLDER + "/" + Path(first_song['path']).stem + ".lrc"
    lyrics_manager.load_lrc(lrc_path)

font_lyrics = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

current_line_index = -1
current_pos = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if (player.is_playing):
        current_pos = player.get_pos()
        print(f"Pos: {current_pos:.2f}s")
        current_line_index = lyrics_manager.get_current_line(current_pos)

    screen.fill(BG_COLOR)

    if len(lyrics_manager.lyrics) > 0 and current_line_index >= 0:
        timestamp, text = lyrics_manager.lyrics[current_line_index]
        text_surface = font_lyrics.render(text, True, HIGHLIGHT_COLOR)

        pos_x = WINDOW_WIDTH // 2 - text_surface.get_width() // 2
        pos_y = WINDOW_HEIGHT // 2

        screen.blit(text_surface, (pos_x, pos_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
