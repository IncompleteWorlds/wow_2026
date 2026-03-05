import pygame
import sys

from game_map import GameMap
from game_data import GameData


# Constants
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
FPS = 30

game_data = GameData()  
game_map = GameMap()



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
        title_surf = font.render("ACME. Evil Town without a Residents", True, (255, 255, 255))
        prompt_surf = small_font.render("Press Any Key", True, (255, 128, 128))

        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(title_surf, title_rect)
        screen.blit(prompt_surf, prompt_rect)
        pygame.display.flip()


def load_assets() -> None:
    """Load all game assets (images, sounds, etc.)"""

    # Load assets defined in GameData
    game_data.load_assets() 

    # Load map data from the specified file
    game_map.load_map_data(game_data.map_file_name) 


def change_room(new_room_name: str) -> None:
    """Change the current room to a new one by name."""
    if new_room_name in game_data.list_rooms:
        game_data.current_room_name = new_room_name
        game_data.current_room = game_data.list_rooms[new_room_name]
        print(f"=== Changed to room: {new_room_name}")
    else:
        raise RuntimeError(f"Room '{new_room_name}' not found in game data.")


def change_actor(new_actor_name: str, x: int, y: int) -> None:
    """Change the current actor to a new one by name."""
    if new_actor_name in game_data.list_actors:
        game_data.current_actor_name = new_actor_name
        game_data.current_actor = game_data.list_actors[new_actor_name]

        game_data.current_actor.set_position(x, y)

        print(f"=== Changed to actor: {new_actor_name}")
    else:
        raise RuntimeError(f"Actor '{new_actor_name}' not found in game data.") 


def process_inputs(screen, clock) -> None:
    """Process user inputs and return relevant state (e.g., keys pressed)."""

    # Get current mouse position
    game_data.mouse_x, game_data.mouse_y = pygame.mouse.get_pos() 

    # Reset the mouse click coordinates     
    game_data.mouse_click_x = None
    game_data.mouse_click_y = None

    # Process all events in the queue 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_data.end_flag = True
            
        # handle left mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 = left mouse button
                if game_data.debug_mode:
                        print(f"   Mouse click at: {event.pos}")
                game_data.mouse_click_x, game_data.mouse_click_y = event.pos

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                # Show map 
                game_map.run(screen, clock, FPS, game_data)

            elif event.key == pygame.K_ESCAPE:
                game_data.end_flag = True

            elif event.key == pygame.K_g:
                # Toggle grid/graph overlay visibility
                game_data.grid_visible = not game_data.grid_visible

            elif event.key == pygame.K_d:
                game_data.debug_mode = not game_data.debug_mode
    
    # game_data.keys = pygame.key.get_pressed()

    return 


def update_objects(delta_time_secs) -> None:
    """Update all game objects based on time passed and current input."""
    # e.g., player.update(dt, keys)

    if game_data.current_room is not None:
        game_data.current_room.update(delta_time_secs, game_data)

    if game_data.current_actor is not None:
        game_data.current_actor.update(delta_time_secs)

        if game_data.mouse_click_x is not None and game_data.mouse_click_y is not None:
            print(f"Walking to: ({game_data.mouse_click_x}, {game_data.mouse_click_y})")
            game_data.current_actor.walk_to(game_data.mouse_click_x, game_data.mouse_click_y)


def redraw_screen(screen) -> None:
    """Redraw the entire screen and draw the mouse pointer."""

    screen.fill((0, 0, 0))  # Clear with black

    # draw objects here
    # Here you would draw your game objects, UI, etc.

    if game_data.current_room is not None:
        game_data.current_room.draw(screen, game_data)

    if game_data.current_actor is not None:
        game_data.current_actor.draw(screen)

    # draw custom pointer if loaded
    if game_data.mouse_pointer is not None:
        # center the pointer image on the mouse coordinates so it behaves like a normal cursor
        ptr_rect = game_data.mouse_pointer.get_rect()
        draw_x = game_data.mouse_x - ptr_rect.width // 2
        draw_y = game_data.mouse_y - ptr_rect.height // 2
        screen.blit(game_data.mouse_pointer, (draw_x, draw_y))

    # Update the full display
    pygame.display.flip()  



def main():
    # Init pygame 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Pygame Game")
    clock = pygame.time.Clock()

    # show intro scene before running the game
    show_intro(screen, clock)

    # Load any graphics/sounds/etc
    load_assets()

    change_room(game_data.current_room_name)
    change_actor(game_data.current_actor_name, game_data.initial_actor_x, game_data.initial_actor_y)

    # hide the default OS cursor so only our custom image is visible
    pygame.mouse.set_visible(False)

    # Game state / objects would go here
    running = True

    counter = 0

    while running:
        # Calculate time passed
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame

        # Read inputs
        process_inputs(screen, clock)
        if game_data.end_flag: 
            running = False
            continue

        # Update game objects
        update_objects(dt)

        # Redraw screen
        redraw_screen(screen)

        # Debug 
        if game_data.debug_mode:
            counter += 1
            if counter % 10 == 0 and game_data.mouse_click_x != 0 and game_data.mouse_click_y !=0:
                print(f"Mouse X: {game_data.mouse_click_x}, Mouse Y: {game_data.mouse_click_y}")
                game_data.mouse_click_x = None
                game_data.mouse_click_y = None



    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
