from dataclasses import dataclass, field
import json
from typing import Any, Optional

import pygame

from actor import Actor
from room import Room

GAME_DATA_FILE = "assets/game_data.json"


@dataclass
class GameData:
    """Container for input-related global state.

    This replaces the previous module-level globals and can be
    instantiated and passed around as needed.
    """

    # Game state flags
    end_flag: bool = False

    # Keyboard state
    keys: Optional[pygame.key.ScancodeWrapper] = None

    # Mouse state
    mouse_x: int = 0
    mouse_y: int = 0
    mouse_click_x: Optional[int] = None
    mouse_click_y: Optional[int] = None
    mouse_pointer: Optional[pygame.Surface] = None  

    grid_visible = False
    debug_mode = False

    show_map = False

    map_file_name: str = ""

    # list of rooms
    list_rooms: dict[str, Room] = field(default_factory=dict)

    current_room_name: str = ""
    current_room : Optional[Room] = None

    # list of actors
    list_actors: dict[str, Actor] = field(default_factory=dict)

    current_actor_name: str = ""
    current_actor : Optional[Actor] = None
    initial_actor_x = 0
    initial_actor_y = 0
    
    # list of objects


    def load_assets(self) -> None:
        """Load all game assets (images, sounds, etc.)"""

        # global game_data
        try:
            with open(GAME_DATA_FILE, "r") as f:
                data = json.load(f)

            if "mouse_pointer" in data:
                mouse_pointer_path = data["mouse_pointer"]  
                self.mouse_pointer = pygame.image.load(mouse_pointer_path)

                # Optimize mouse pointer for faster blitting
                self.mouse_pointer.convert()

            # Load the list of actors 
            if "actors" in data:
                actors_data = data["actors"]
                for current_actor_name in actors_data:
                    # Process actor data
                    new_actor = Actor(actor_name=current_actor_name,
                        x=0, y=0)          

                    self.list_actors[current_actor_name] = new_actor

            # Load rooms
            if "rooms" in data:
                rooms_data = data["rooms"]
                for current_room_name in rooms_data:
                    new_room = Room(
                        name=current_room_name,
                        description=""
                    )

                    self.list_rooms[current_room_name] = new_room

            # Game map 
            if "map" in data:
                self.map_file_name = data["map"]

            if "starting_room" in data:
                self.current_room_name = data["starting_room"]

            if "starting_actor" in data:
                self.current_actor_name = data["starting_actor"]

            # Extract character initial position
            if "actor_position" in data:
                char_data = data["actor_position"]
                self.initial_actor_x = char_data.get("x", 0)
                self.initial_actor_y = char_data.get("y", 0)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading game data from {GAME_DATA_FILE}: {e}")


    def change_room(self, new_room_name: str, new_actor_x : int, new_actor_y : int) -> None:
        """Change the current room to a new one by name and move the current actor to it."""
        if new_room_name == self.current_room_name:
            return

        if new_room_name in self.list_rooms:
            # Move the actor from the current room to new room 
            if self.current_room is not None:
                self.current_room.remove_actor(self.current_actor)

            self.current_room_name = new_room_name
            self.current_room = self.list_rooms[new_room_name]

            if self.current_actor is not None:
                if self.current_actor is not self.current_room.list_actors:
                    self.current_room.add_actor(self.current_actor)

                # Stop and update the position 
                self.current_actor.set_position(new_actor_x, new_actor_y)
                self.current_actor.stop()

            print(f"=== Changed to room: {new_room_name}")

        elif new_room_name == "map":
            self.current_room_name = ""
            self.current_room = None
            
        else:
            raise RuntimeError(f"Room '{new_room_name}' not found in game data.")


    def change_actor(self, new_actor_name: str, x: int, y: int) -> None:
        """Change the current actor to a new one by name."""
        if new_actor_name in self.list_actors:
            self.current_actor_name = new_actor_name
            self.current_actor = self.list_actors[new_actor_name]

            self.current_actor.set_position(x, y)

            print(f"=== Changed to actor: {new_actor_name}")
        else:
            raise RuntimeError(f"Actor '{new_actor_name}' not found in game data.") 
