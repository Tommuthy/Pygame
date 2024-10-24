import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
#from character import Character

def run_game():
    #intialize pygame, settings, and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make a ship and character
    ship = Ship(ai_settings, screen)
    #character = Character(screen) 

    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ship)
        # Update the ship based on movement flag.
        ship.update()       
        # Redraw the screen during each pass through the loop. 
        gf.update_screen(ai_settings, screen, ship)
        # character.blitme()
        
run_game()
 