import json
import pygame

from actor import Actor
from exits import Exit
from graph import Graph
from path_finding import get_path 


class GameMap:
    """Represents a map/level in the game with its own game loop."""

    def __init__(self):
        """Initialize the map."""

        self.screen = None
        self.clock = None
        self.fps = None
        self.int_game_data = None

        self.map_background = None 
        self.position_map = None

        # Character position
        self.actor = None
        self.actor_name = ""
        self.character_x = 0
        self.character_y = 0
        
        # X Position
        self.position_x = 0
        self.position_y = 0
        
        # Graph data structure
        # Dictionary to store graph nodes and edges
        self.graph = Graph() 

        # List of exits
        self.list_exits : list[Exit] = []
        
        # Flag to toggle grid display
        self.grid_visible = False  

        self.debug_mode = False


    def load_map_data(self, map_file_name: str) -> None:
        """Load map configuration from a JSON file.
        
        Args:
            json_file: Path to the JSON file containing map data.
        """
        # print(f"===== Loading map data from: {map_file_name}")

        try:
            with open(map_file_name, "r") as f:
                data = json.load(f)
            
                if "map_background" in data:
                    map_background_path = data["map_background"]
                    self.map_background = pygame.image.load(map_background_path)

                if "actor_name" in data:
                    self.actor_name = data["actor_name"]

                if "position_map" in data:
                    position_map_path = data["position_map"]
                    self.position_map = pygame.image.load(position_map_path)
                
                # Extract character initial position
                if "actor_position" in data:
                    char_data = data["actor_position"]
                    self.character_x = char_data.get("x", 0)
                    self.character_y = char_data.get("y", 0)
                
                # Extract position data
                if "position" in data:
                    pos_data = data["position"]
                    self.position_x = pos_data.get("x", 0)
                    self.position_y = pos_data.get("y", 0)
                
                # Extract graph data
                if "graph" in data:
                    graph_data = data["graph"]
                    self.graph.load(graph_data)

                # Extract list of exits
                if "exits" in data:
                    exits_data = data["exits"]
                    for exit_data in exits_data:
                        rectangle_data = exit_data.get("rectangle", [0, 0, 0, 0])
                        new_exit = Exit(name = exit_data.get("name", ""),
                                        room = exit_data.get("room", ""),
                                        rectangle = pygame.Rect(rectangle_data.get("x", 0), 
                                                    rectangle_data.get("y", 0), 
                                                    rectangle_data.get("width", 0), 
                                                    rectangle_data.get("height", 0)),
                                        actor_x=exit_data.get("actor_x", 0),
                                        actor_y=exit_data.get("actor_y", 0))
            
                        self.list_exits.append(new_exit)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading map data from {map_file_name}: {e}")
            return 

        # Create the actor  
        self.actor = Actor(self.actor_name, self.character_x, self.character_y)


    def process_inputs(self) -> bool:
        """Process user inputs.

        Returns:
            True if the map should exit, False otherwise.
        """

        self.int_game_data.mouse_x, self.int_game_data.mouse_y = pygame.mouse.get_pos()
        self.int_game_data.mouse_click_x = None
        self.int_game_data.mouse_click_y = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.debug_mode:
                        print(f"   Mouse click at: {event.pos}")
                    self.int_game_data.mouse_click_x, self.int_game_data.mouse_click_y = event.pos

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return True
                
                elif event.key == pygame.K_g:
                    # Toggle grid/graph overlay visibility
                    self.grid_visible = not self.grid_visible

                elif event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode
    
        return False


    def update(self, dt: float) -> bool:
        """Update all map items based on elapsed time.

        Args:
            dt: Delta time since last frame in seconds.
        """
        if self.int_game_data is None:
            return False
        
        # Update the actor 
        if self.actor is not None:
            # print(f"Actor state: {self.actor.state}, position: ({self.actor.x}, {self.actor.y})")
            self.actor.update(dt)

            if self.actor.is_idle():
                if self.int_game_data.mouse_click_x is not None and \
                   self.int_game_data.mouse_click_y is not None:
                    self.actor.stop()

                    list_positions = get_path(self.graph, self.actor.x, self.actor.y, 
                                                          self.int_game_data.mouse_click_x, self.int_game_data.mouse_click_y)

                    if self.int_game_data.debug_mode:
                        print(f"MAP Walking to: ({self.int_game_data.mouse_click_x}, {self.int_game_data.mouse_click_y})")
                    self.actor.walk_path(list_positions, self.int_game_data.mouse_click_x, self.int_game_data.mouse_click_y)

            # Check if actor is in a Exit 
            for current_exit in self.list_exits:
                if current_exit.rectangle and current_exit.rectangle.collidepoint(self.actor.x, self.actor.y):
                    # Update the current actor, not this actor 
                    self.int_game_data.change_room(current_exit.room, current_exit.actor_x, current_exit.actor_y)

                    self.int_game_data.show_map = False
                    return True 
                
        # Do not stop the loop 
        return False


    def show_grid(self) -> None:
        self.graph.show_grid(self.screen)

    
    def show_exits(self) -> None:
        """Overlay grid lines and graph edges on the screen."""

        font = pygame.font.Font(None, 24)
        for current_exit in self.list_exits:
            # Draw the rectangle 
            pygame.draw.rect(self.screen, (255, 0, 0), current_exit.rectangle, 3)

            # Draw the name 
            text_surface = font.render(current_exit.room, True, (255, 0, 0))
            self.screen.blit(text_surface, (current_exit.rectangle.x + 5, current_exit.rectangle.y - 15))


    def draw(self) -> None:
        """Draw the map and all its items."""
        self.screen.fill((0, 0, 0))  # Clear with black

        # Draw background if loaded
        if self.map_background is not None:
            self.screen.blit(self.map_background, (0, 0))   

        if self.actor is not None:
            self.actor.draw(self.screen)

        if self.position_map is not None:
            self.screen.blit(self.position_map, (self.position_x, self.position_y))

        if self.grid_visible:
            # Draw grid and graph overlay
            self.show_grid()

            self.show_exits()

        # Draw custom mouse pointer if loaded
        if self.int_game_data.mouse_pointer is not None:
            self.screen.blit(self.int_game_data.mouse_pointer, (self.int_game_data.mouse_x, self.int_game_data.mouse_y))

        pygame.display.flip()


    def run(self, screen, clock, fps, game_data) -> None:
        """Main loop for this map."""

        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.int_game_data = game_data

        running = True

        counter = 0 

        while running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds

            # Process inputs
            if self.process_inputs():
                running = False
                continue

            # Update items
            if self.update(dt):
                running = False
                continue

            # Draw everything
            self.draw()

            # Debug 
            if self.debug_mode:
                counter += 1
                if counter % 10 == 0:
                    print(f"Mouse X: {self.int_game_data.mouse_x}, Mouse Y: {self.int_game_data.mouse_y}")

