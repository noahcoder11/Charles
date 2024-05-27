import pygame
import time

pygame.mixer.init()

def perform_audio_output_setup():
    print('Performing audio output setup:')
    success = False
    while not success:
        try:
            pygame.mixer.music.load('sounds/Charles_Startup.m4a')
            pygame.mixer.music.play()

            uinput = input('Did you hear sound? [y/n] ')
            if uinput.lower() == 'y':
                success = True
                break
        except Exception as e:
            print('Error:', e)
        print('Retrying...')
        time.sleep(1)

def playsound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
