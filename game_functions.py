import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to key press movements."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                 sys.exit()
        # Checks for keypresses up or down.
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)    
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship) 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                              bullets, mouse_y, mouse_x) 
            

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_y, mouse_x)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:    
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:    
        ship.moving_left = True
    elif event.key == pygame.K_UP:    
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:    
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False    
    elif event.key == pygame.K_LEFT:    
        ship.moving_left = False   
    elif event.key == pygame.K_UP:    
        ship.moving_up = False   
    elif event.key == pygame.K_DOWN:    
        ship.moving_down= False
           
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    # Redraw the screen during each pass through the loop. 
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ships and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Make the most recently drawn screen visible.
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Response to bullet and collisions"""
    # Removes any bullets and aliens that have collided.
    collisons = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Destroy existing bullets, spped up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

     
def fire_bullets(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit the row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - 
                          (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row."""
    # Create an alien and place it in the row.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        # Create the first row of aliens.
        for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number)

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
        
def check_fleet_edges(ai_settings, aliens):
    """Responds appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Responds to ship being hit by alien.""" 
    # Decrement ships left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
    
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
    
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens) 
        ship.center_ship()
    
        # Pause
        sleep(.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
         """Check if any aliens have reached the bottom of the screen."""
         screen_rect = screen.get_rect()
         for alien in aliens.sprites():
             if alien.rect.bottom >= screen_rect.bottom:
                 # Treat this the same as if the ship got hit.
                 ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                 break
             
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Checks if the fleet is at an edge and then updates all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print("Ship hit!!!")
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


    