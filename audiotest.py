import pygame
from pathlib import Path

pygame.mixer.init()

def playaudio():
    arquivo = Path("audio.wav")

    pygame.mixer.music.load(str(arquivo))
    pygame.mixer.music.set_volume(0.5)

    pygame.time.wait(200)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)
        