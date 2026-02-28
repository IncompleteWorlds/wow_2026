import pygame
import sys

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30

# Global variables for input state
mouse_pointer = None  
mouse_x = 0
mouse_y = 0
keys = None
mouse_click_x = None
mouse_click_y = None


def show_intro(screen, clock):
    """Display an intro scene with title and wait for a key press."""
    font = pygame.font.Font(None, 100)
    small_font = pygame.font.Font(None, 50)

    waiting = True
    while waiting:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

        screen.fill((0, 0, 0))
        title_surf = font.render("ACME", True, (255, 255, 255))
        prompt_surf = small_font.render("Press Any Key", True, (255, 128, 128))

        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(title_surf, title_rect)
        screen.blit(prompt_surf, prompt_rect)
        pygame.display.flip()


def process_inputs():
    """Process user inputs and return relevant state (e.g., keys pressed)."""
    global keys
    global mouse_click_x, mouse_click_y
    global mouse_x, mouse_y

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get current mouse position
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # handle left mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 = left mouse button
                mouse_click_x, mouse_click_y = event.pos

    keys = pygame.key.get_pressed()

    # ESC key
    end_flag = False
    if keys[pygame.K_ESCAPE]: 
        end_flag = True

    return end_flag


def update_objects(dt, mouse_click_x, mouse_click_y, mouse_x, mouse_y):
    """Update all game objects based on time passed and current input."""
    # e.g., player.update(dt, keys)
    pass



def redraw_screen(screen):
    """Redraw the entire screen and draw the mouse pointer."""
    screen.fill((0, 0, 0))  # Clear with black

    # draw objects here
    # Here you would draw your game objects, UI, etc.

    # draw custom pointer if loaded
    if mouse_pointer is not None:
        # center the pointer image on the mouse coordinates so it behaves like a normal cursor
        ptr_rect = mouse_pointer.get_rect()
        draw_x = mouse_x - ptr_rect.width // 2
        draw_y = mouse_y - ptr_rect.height // 2
        screen.blit(mouse_pointer, (draw_x, draw_y))

    # Update the full display
    pygame.display.flip()  

def load_assets():
    """Load all game assets (images, sounds, etc.)"""
    global mouse_pointer
    # e.g., player_image = pygame.image.load('assets/player.png')

    mouse_pointer = pygame.image.load('assets/mouse_pointer.png')


def main():
    # Init pygame 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Pygame Game")
    clock = pygame.time.Clock()

    # show intro scene before running the game
    show_intro(screen, clock)

    # load any graphics/sounds/etc
    load_assets()

    # hide the default OS cursor so only our custom image is visible
    pygame.mouse.set_visible(False)

    # Game state / objects would go here
    running = True

    while running:
        # Calculate time passed
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame

        # Read inputs
        end_flag = process_inputs()
        if end_flag: 
            running = False
            continue

        # Update game objects
        update_objects(dt, mouse_click_x, mouse_click_y, mouse_x, mouse_y)

        # Redraw screen
        redraw_screen(screen)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
