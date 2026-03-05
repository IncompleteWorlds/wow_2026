import json

import pygame

from exits import Exit
from actor import Actor


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
                self.graph = data["graph"]

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
                        )
                    )
                    self.list_exits.append(new_exit)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading room data from room_{self.name}.json: {e}")
            return


    def update(self, dt: float, int_game_data) -> None:
        """Update all map items based on elapsed time.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update the actor 
        if self.list_actors is not None:
            for actor in self.list_actors:
                if actor.is_idle():
                    if int_game_data.mouse_click_x is not None and \
                       int_game_data.mouse_click_y is not None:
                        # print(f"Walking to: ({int_game_data.mouse_click_x}, {int_game_data.mouse_click_y})")
                        actor.walk_to(int_game_data.mouse_click_x, int_game_data.mouse_click_y)

                else:
                    # print(f"Actor state: {self.actor.state}, position: ({self.actor.x}, {self.actor.y})")
                    actor.update(dt)


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
        for exit in self.list_exits:
            if exit.rectangle is not None:
                pygame.draw.rect(screen, (255, 0, 0), exit.rectangle, 2)


    def show_grid(self,screen) -> None:
        """Draw grid and graph overlay for debugging."""
        # if hasattr(self, "graph") and self.graph is not None:
        #     for node in self.graph.get("nodes", []):
        #         x = node.get("x", 0)
        #         y = node.get("y", 0)
        #         pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)

        #     for edge in self.graph.get("edges", []):
        #         start_node_id = edge.get("start")
        #         end_node_id = edge.get("end")
        #         start_node = next((n for n in self.graph.get("nodes", []) if n.get("id") == start_node_id), None)
        #         end_node = next((n for n in self.graph.get("nodes", []) if n.get("id") == end_node_id), None)
        #         if start_node and end_node:
        #             pygame.draw.line(screen, (0, 255, 0), (start_node["x"], start_node["y"]), (end_node["x"], end_node["y"]), 2)
                    
        # draw graph edges if graph data is available
        if not self.graph:
            return

        # print(f"Graph data: {self.graph}")

        # create a mapping from node id -> (x, y) coordinates
        node_positions = {
            node["id"]: (node.get("x", 0), node.get("y", 0))
            for node in self.graph.get("nodes", [])
        }
        
        edges = self.graph.get("edges", {})
        # iterate through edges: src -> [child_ids]
        for src_key, children in edges.items():
            try:
                # JSON keys might be strings
                src_id = int(src_key)
            except (ValueError, TypeError):
                src_id = src_key

            src_pos = node_positions.get(src_id)
            if not src_pos:
                continue

            for child_id in children:
                child_pos = node_positions.get(child_id)
                if child_pos:
                    # draw line from source to child
                    pygame.draw.line(screen, (0, 255, 0), src_pos, child_pos, 3)


