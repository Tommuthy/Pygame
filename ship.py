import pygame

class Ship():
    
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
       
        # Store decimal value for ship's center.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Store value of the bottom of the ships image and the bottom of the screen.
        self.bottom = float(self.centery)
        
        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update ship's center value not rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0: 
            self.centerx -= self.ai_settings.ship_speed_factor
        # To move up and down from the center of y.
        elif self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom: 
            self.centery += self.ai_settings.ship_speed_factor
       
        # Update coordinates from x and y
        self.rect.centery = self.centery 
        self.rect.centerx = self.centerx
                 
    def center_ship(self):
        """Center the ship on the screen."""
        self.centerx = self.screen_rect.centerx
        # Alignment of the bottom of the ship image to the bottom of the screen.
        self.centery = self.bottom
        
        
    def blitme(self):
        """Draw ship at its current location."""
        self.screen.blit(self.image, self.rect)