import sys
import pygame, mutagen.mp3
song_file = 'sfx/ichwill.mp3'
mp3 = mutagen.mp3.MP3(song_file)
pygame.mixer.init(frequency=mp3.info.sample_rate)
pygame.mixer.music.load(song_file)
pygame.mixer.music.play()
sys.path.insert(0, 'modules')
import menu

menu.menu()
