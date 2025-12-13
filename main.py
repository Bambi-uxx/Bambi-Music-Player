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

#Fonts
font_lyrics_current = pygame.font.Font(FONT_QUICKSAND, FONT_SIZE_LYRICS_CURRENT)
font_lyrics_context = pygame.font.Font(FONT_QUICKSAND, FONT_SIZE_LYRICS_CONTEXT)
font_title = pygame.font.Font(FONT_RALEWAY, FONT_SIZE_TITLE)
font_artist = pygame.font.Font(FONT_QUICKSAND, FONT_SIZE_ARTIST)
font_playlist = pygame.font.Font(FONT_QUICKSAND, FONT_SIZE_PLAYLIST_ITEM)
font_volume = pygame.font.Font(FONT_QUICKSAND, FONT_SIZE_VOLUME)

current_line_index = -1
current_pos = 0
show_playlist = False


#Buttons
play_button_rect = pygame.Rect(CIRCLE_CENTER_X - 50, CIRCLE_CENTER_Y - 50, 100, 100)
prev_button_rect = pygame.Rect(CIRCLE_CENTER_X - 115, CIRCLE_CENTER_Y - 25, 50, 50)
next_button_rect = pygame.Rect(CIRCLE_CENTER_X + 65, CIRCLE_CENTER_Y - 25, 50, 50)
vol_up_rect = pygame.Rect(CIRCLE_CENTER_X - 25, CIRCLE_CENTER_Y - 125, 50, 35)
vol_down_rect = pygame.Rect(CIRCLE_CENTER_X - 25, CIRCLE_CENTER_Y + 75, 50, 35)

#Draw buttons
def draw_play_icon(surface, center_x, center_y, size, color):
    points = [
        (center_x - size//2, center_y - size),
        (center_x - size//2, center_y + size),
        (center_x + size, center_y)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_pause_icon(surface, center_x, center_y, size, color):
    bar_width = size // 3
    bar_height = size * 2
    gap = size // 2
    
  
    pygame.draw.rect(surface, color, (center_x - gap - bar_width, center_y - bar_height//2, bar_width, bar_height))
  
    pygame.draw.rect(surface, color, (center_x + gap, center_y - bar_height//2, bar_width, bar_height))

def draw_prev_icon(surface, center_x, center_y, size, color):
    pygame.draw.rect(surface, color, (center_x - size, center_y - size, 3, size * 2))
    
    points = [
        (center_x + size, center_y),
        (center_x - size + 5, center_y - size),
        (center_x - size + 5, center_y + size)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_next_icon(surface, center_x, center_y, size, color):
    points = [
        (center_x - size, center_y),
        (center_x + size - 5, center_y - size),
        (center_x + size - 5, center_y + size)
    ]
    pygame.draw.polygon(surface, color, points)
    
    pygame.draw.rect(surface, color, (center_x + size - 3, center_y - size, 3, size * 2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.is_playing:
                    player.pause()
                else:
                    player.unpause()
        
            elif event.key == pygame.K_RIGHT:
                next_song = playlist.next_song()
                player.load(next_song['path'])
                player.play()
            
                lrc_path = LYRICS_FOLDER + "/" + Path(next_song['path']).stem + ".lrc"
                lyrics_manager.load_lrc(lrc_path)
        
            elif event.key == pygame.K_LEFT:
                prev_song = playlist.previous_song()
                player.load(prev_song['path'])
                player.play()
            
                lrc_path = LYRICS_FOLDER + "/" + Path(prev_song['path']).stem + ".lrc"
                lyrics_manager.load_lrc(lrc_path)
        
            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_TAB:
                show_playlist = not show_playlist

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if play_button_rect.collidepoint(mouse_pos):
                if player.is_playing:
                    player.pause()
                else:
                    player.unpause()
            
            elif prev_button_rect.collidepoint(mouse_pos):
                prev_song = playlist.previous_song()
                player.load(prev_song['path'])
                player.play()
                lrc_path = LYRICS_FOLDER + "/" + Path(prev_song['path']).stem + ".lrc"
                lyrics_manager.load_lrc(lrc_path)
            
            elif next_button_rect.collidepoint(mouse_pos):
                next_song = playlist.next_song()
                player.load(next_song['path'])
                player.play()
                lrc_path = LYRICS_FOLDER + "/" + Path(next_song['path']).stem + ".lrc"
                lyrics_manager.load_lrc(lrc_path)
            
            elif vol_up_rect.collidepoint(mouse_pos):
                current_vol = player.volume
                player.set_volume(current_vol + 0.1)
            
            elif vol_down_rect.collidepoint(mouse_pos):
                current_vol = player.volume
                player.set_volume(current_vol - 0.1)
            
            # Click on playlist
            elif show_playlist and mouse_pos[0] < SCREEN_AREA_WIDTH:
                click_y = mouse_pos[1]

                if click_y > PLAYLIST_START_Y:
                    song_index = (click_y - PLAYLIST_START_Y) // PLAYLIST_ITEM_HEIGHT

                    if 0 <= song_index < len(playlist.songs):
                        playlist.current_index = song_index
                        selected_song = playlist.songs[song_index]

                        player.load(selected_song['path'])
                        player.play()
                        lrc_path = LYRICS_FOLDER + "/" + Path(selected_song['path']).stem + ".lrc"
                        lyrics_manager.load_lrc(lrc_path)

    if (player.is_playing):
        current_pos = player.get_pos()
        current_line_index = lyrics_manager.get_current_line(current_pos)
    
    #Visuals
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, SCREEN_AREA_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, ACCENT_COLOR, (SCREEN_AREA_WIDTH, 0), (SCREEN_AREA_WIDTH, WINDOW_HEIGHT), 3)
    pygame.draw.circle(screen, ACCENT_COLOR, (CIRCLE_CENTER_X, CIRCLE_CENTER_Y), CIRCLE_RADIUS, 3)
    pygame.draw.circle(screen, PANEL_COLOR, (CIRCLE_CENTER_X, CIRCLE_CENTER_Y), CIRCLE_RADIUS - 3)

    # Central button
    center_button_rect = pygame.draw.circle(screen, HIGHLIGHT_COLOR, (CIRCLE_CENTER_X, CIRCLE_CENTER_Y), 50)
    if player.is_playing:
        draw_pause_icon(screen, CIRCLE_CENTER_X, CIRCLE_CENTER_Y, ICON_SIZE_CENTER, TEXT_COLOR)
    else:
        draw_play_icon(screen, CIRCLE_CENTER_X, CIRCLE_CENTER_Y, ICON_SIZE_CENTER, TEXT_COLOR)
    
    # Previous
    prev_x = CIRCLE_CENTER_X - 100
    draw_prev_icon(screen, prev_x, CIRCLE_CENTER_Y, ICON_SIZE_SIDE, TEXT_COLOR)
    
    # Next
    next_x = CIRCLE_CENTER_X + 100
    draw_next_icon(screen, next_x, CIRCLE_CENTER_Y, ICON_SIZE_SIDE, TEXT_COLOR)
    
    # Volume
    vol_up_text = font_volume.render("+", True, TEXT_COLOR)
    screen.blit(vol_up_text, (CIRCLE_CENTER_X - 15, CIRCLE_CENTER_Y - 115))
    
    vol_down_text = font_volume.render("-", True, TEXT_COLOR)
    screen.blit(vol_down_text, (CIRCLE_CENTER_X - 15, CIRCLE_CENTER_Y + 85))

    #Title and artist
    if len(playlist.songs) > 0:
        current_song = playlist.get_current_song()
        if current_song:
            # Title
            title_display = font_title.render(current_song['title'], True, TEXT_COLOR)
            screen.blit(title_display, (SONG_INFO_X, SONG_TITLE_Y))
            
            # Artist
            artist_display = font_artist.render(f"by {current_song['artist']}", True, (150, 150, 150))
            screen.blit(artist_display, (SONG_INFO_X, SONG_ARTIST_Y))

    # Progress bar
    if len(playlist.songs) > 0:
        duration = player.get_duration()
        if duration > 0:
           
            progress = min(current_pos / duration, 1.0)
            
            
            bar_x = 20
            bar_width = SCREEN_AREA_WIDTH - 40
            pygame.draw.rect(screen, PROGRESS_BAR_COLOR, 
                           (bar_x, PROGRESS_BAR_Y, bar_width, PROGRESS_BAR_HEIGHT), 
                           border_radius=3)
            
            
            fill_width = int(bar_width * progress)
            if fill_width > 0:
                pygame.draw.rect(screen, PROGRESS_FILL_COLOR, 
                               (bar_x, PROGRESS_BAR_Y, fill_width, PROGRESS_BAR_HEIGHT), 
                               border_radius=3)
            
            
            current_time_str = f"{int(current_pos//60)}:{int(current_pos%60):02d}"
            total_time_str = f"{int(duration//60)}:{int(duration%60):02d}"
            time_text = font_artist.render(f"{current_time_str} / {total_time_str}", True, (150, 150, 150))
            screen.blit(time_text, (bar_x, PROGRESS_BAR_Y + 15))


    # Alternate between playlist and lyrics
    if show_playlist:
    
        title_text = font_playlist.render("PLAYLIST", True, TEXT_COLOR)
        screen.blit(title_text, (SONG_INFO_X, PLAYLIST_TITLE_Y))
    
        y_offset = PLAYLIST_START_Y
        for i, song in enumerate(playlist.songs):
        
            if i == playlist.current_index:
                color = HIGHLIGHT_COLOR
                prefix = "► "
            else:
                color = TEXT_COLOR
                prefix = "  "
        
            song_text = font_playlist.render(f"{prefix}{song['title']}", True, color)
            screen.blit(song_text, (PLAYLIST_ITEM_X, y_offset))
        
            y_offset += PLAYLIST_ITEM_HEIGHT
        
        
            if y_offset > WINDOW_HEIGHT - 50:
                break
    else:
        if len(lyrics_manager.lyrics) > 0 and current_line_index >= 0:
            center_y = WINDOW_HEIGHT // 2
            
            
            if current_line_index > 0:
                _, prev_text = lyrics_manager.lyrics[current_line_index - 1]
                prev_surface = font_lyrics_context.render(prev_text, True, LYRICS_CONTEXT_COLOR)
                prev_x = SCREEN_AREA_WIDTH // 2 - prev_surface.get_width() // 2
                screen.blit(prev_surface, (prev_x, center_y - LYRICS_LINE_SPACING))
            
            #Actual line
            _, current_text = lyrics_manager.lyrics[current_line_index]
            current_surface = font_lyrics_current.render(current_text, True, HIGHLIGHT_COLOR)
            current_x = SCREEN_AREA_WIDTH // 2 - current_surface.get_width() // 2
            screen.blit(current_surface, (current_x, center_y))
            
            if current_line_index < len(lyrics_manager.lyrics) - 1:
                _, next_text = lyrics_manager.lyrics[current_line_index + 1]
                next_surface = font_lyrics_context.render(next_text, True, LYRICS_CONTEXT_COLOR)
                next_x = SCREEN_AREA_WIDTH // 2 - next_surface.get_width() // 2
                screen.blit(next_surface, (next_x, center_y + LYRICS_LINE_SPACING))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
