"""Copyright 2016"""
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

def run_game():
    #intialize pygame, settings, and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    # Make a ship , a group of bullets, and group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens  = Group()
    
    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            # Update the ship based on movement flag.
            ship.update()
            # Update the bullets based on movement flag and remove bullets.        
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            # To see the number of bullets return to 0 after shooting.
            #print(len(bullets)) 
            # Update aliens to move.
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            # Redraw the screen during each pass through the loop. 
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)
            
            
        
run_game()
