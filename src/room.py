import json

import pygame

from exits import Exit
from actor import Actor
from graph import Graph
from path_finding import get_path


class Room:
    def __init__(self, name : str, description : str):
        self.name = name
        self.description = description

        # Sprite surface and rect
        self.background = pygame.Surface((150, 150))
        self.background.fill((0, 0, 0))
        self.rect = self.background.get_rect(midbottom=(0, 0))

        self.list_actors : list[Actor] = []

        self.list_exits : list[Exit] = []

        self.graph= Graph()

        self._load_assets()


    def _load_assets(self) -> None:
        """Load room-specific assets from JSON file."""
        try:           
            json_file = f"assets/rooms/room_{self.name}.json"
            with open(json_file, "r") as f:
                data = json.load(f)

            if "background" in data:
                map_background_path = data["background"]
                self.background = pygame.image.load(map_background_path)
                        
            if "graph" in data:
                graph_data = data["graph"]
                self.graph.load(graph_data)

            if "exits" in data:
                for exit_data in data["exits"]:
                    rect_data = exit_data.get("rectangle", {})
                    new_exit = Exit(
                        name=exit_data.get("name", ""),
                        room=exit_data.get("room", ""),
                        rectangle=pygame.Rect(
                            rect_data.get("x", 0),
                            rect_data.get("y", 0),
                            rect_data.get("width", 0),
                            rect_data.get("height", 0)
                        ),
                        actor_x=exit_data.get("actor_x", 0),
                        actor_y=exit_data.get("actor_y", 0)
                    )
                    self.list_exits.append(new_exit)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading room data from room_{self.name}.json: {e}")
            return


    def update(self, delta_time_secs: float, int_game_data) -> None:
        """Update all map items based on elapsed time.

        Args:
            delta_time_secs: Delta time since last frame in seconds.
        """
        # Update the actors 
        if self.list_actors is not None:
            for actor in self.list_actors:
                # print(f"Actor state: {self.actor.state}, position: ({self.actor.x}, {self.actor.y})")
                actor.update(delta_time_secs)

                if actor == int_game_data.current_actor:
                    # If the actor is colliding with an exit, change room
                    for current_exit in self.list_exits:
                        if current_exit.rectangle and current_exit.rectangle.collidepoint(actor.x, actor.y):
                            int_game_data.change_room(current_exit.room, current_exit.actor_x, current_exit.actor_y)

                            if current_exit.room == "map":
                                int_game_data.show_map = True

                            return  # Exit early to avoid multiple room changes in one frame

                    if int_game_data.mouse_click_x is not None and int_game_data.mouse_click_y is not None:
                        # Stop any current movement before starting a new one
                        int_game_data.current_actor.stop()  

                        print(f"Room Walking to: ({int_game_data.mouse_click_x}, {int_game_data.mouse_click_y})")

                        # int_game_data.current_actor.walk_to(int_game_data.mouse_click_x, int_game_data.mouse_click_y)

                        list_positions = get_path(self.graph, int_game_data.current_actor.x, int_game_data.current_actor.y, 
                                                              int_game_data.mouse_click_x, int_game_data.mouse_click_y)
                        
                        # self.actor.walk_to(self.int_game_data.mouse_click_x, self.int_game_data.mouse_click_y)
                        int_game_data.current_actor.walk_path(list_positions, int_game_data.mouse_click_x, int_game_data.mouse_click_y)

    def draw(self, screen, int_game_data) -> None:
        """Draw the map and all its items."""
        screen.fill((0, 0, 0))  # Clear with black

        # Draw background if loaded
        if self.background is not None:
            screen.blit(self.background, (0, 0))   

        for actor in self.list_actors:
            actor.draw(screen)

        if int_game_data.grid_visible:
            # Draw grid and graph overlay
            self.show_grid(screen)

            self.show_exits(screen)


    def show_exits(self, screen) -> None:
        """Draw exit rectangles for debugging."""
        font = pygame.font.Font(None, 24)

        for exit in self.list_exits:
            if exit.rectangle is not None:
                pygame.draw.rect(screen, (255, 0, 0), exit.rectangle, 2)

            # Draw the name 
            text_surface = font.render(exit.room, True, (255, 0, 0))
            screen.blit(text_surface, (exit.rectangle.x + 5, exit.rectangle.y - 15))


    def show_grid(self, screen) -> None:
        self.graph.show_grid(screen)


    def add_actor(self, actor: Actor) -> None:
        """Add an actor to the room."""
        self.list_actors.append(actor)


    def remove_actor(self, actor: Actor) -> None:
        """Remove an actor from the room."""
        if actor in self.list_actors:
            self.list_actors.remove(actor)

