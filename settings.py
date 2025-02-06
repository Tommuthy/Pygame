class Settings():
    """A class to store all settings in Alien Invasion."""
    
    def __init__(self):
        """Initialize game settings."""
        self.screen_width = 1600 
        self.screen_height = 900
        self.bg_color = (230, 230, 230) 
        
        # Ship Settings.
        self.ship_speed_factor = 1.5
        self.ship_limit = 2

        # Bullet settings. 
        self.bullet_speed_factor = 3 # per pixel
        self.bullet_width = 3 # per pixel
        self.bullet_height = 15 # per pixel
        self.bullet_color = 60, 60, 60 # RBG gray scale
        self.bullets_allowed = 3
        
        # Alien settings.
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 1
        # Fleet_direction of 1 represents right: -1 represents left.
        self.fleet_direction = 1
        