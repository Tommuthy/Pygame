import pygame

class Character():
    
    def __init__(self, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start easch new ship at the bottom center of the screen.
        self.rect.center = self.screen_rect.center
        
    def blitme(self):
        """Draw ship at its current location."""
        self.screen.blit(self.image, self.rect)
        
        #dkjashdlkasdh