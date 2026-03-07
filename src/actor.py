import json

import pygame
from enum import Enum
from typing import List, Dict, Optional

SPEED_INCREMENT = 5


class ActorState(Enum):
    """Enumeration of possible actor states."""
    STANDING = "standing"
    WALKING_LEFT = "walking_left"
    WALKING_RIGHT = "walking_right"


class Actor(pygame.sprite.Sprite):
    """Represents a game actor with sprite animation and state management.
    
    An actor can be in different states (Standing, Walking) and displays
    appropriate animated frames for each state.
    """

    def __init__(self, actor_name: str, x: int, y: int):
        """Initialize the actor.

        Args:
            actor_name: The name of the actor.
            x: Initial x position.
            y: Initial y position.
        """
        super().__init__()

        self.actor_name = actor_name

        # Position
        self.x = x
        self.y = y
        self.speed = 0  # pixels per second, can be adjusted as needed
        self.target_x = 0
        self.target_y = 0

        # State management
        self.state = ActorState.STANDING
        self.previous_state = None

        # Animation
        self.frames: Dict[ActorState, List[pygame.Surface]] = {
            ActorState.STANDING: [],
            ActorState.WALKING_LEFT: [],
            ActorState.WALKING_RIGHT: [],
        }
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.1  # Duration per frame in seconds

        # Sprite surface and rect
        self.image = pygame.Surface((150, 150))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        self._load_assets()


    def _load_assets(self) -> None:
        """Load actor assets (e.g., sprite frames) from JSON configuration.

        The JSON is expected to contain a `sprite` section with keys matching
        each ``ActorState`` value.  For example::

            {
                "name": "actor_name",
                "speed": 1,
                "sprite": {
                    "standing": ["path1.png", "path2.png", ...],
                    "walking": ["pathA.png", "pathB.png", ...]
                }
            }

        The file is read and the lists of file paths are used to populate the
        ``self.frames`` dictionary.  This makes it easy to tweak animation data
        without changing code.
        """
        # print(f"**** Loading assets for actor: {self.actor_name}")

        json_file = f"assets/actors/actor_{self.actor_name}.json"
        with open(json_file, "r") as f:
            actor_data = json.load(f)

        if "speed" in actor_data:
            self.speed = actor_data["speed"]

        # load sprite paths from JSON, falling back to empty lists if keys
        # are missing or the structure is unexpected.
        sprite_data = actor_data.get("sprite", {})
        for state in ActorState:
            paths = sprite_data.get(state.value, [])
            # convert any non-list values to list just to be safe
            if not isinstance(paths, list):
                paths = [paths]

            self.frames[state] = [pygame.image.load(p) for p in paths]

        # initialize the current image from standing frames if available
        if self.frames.get(ActorState.STANDING):
            self.image = self.frames[ActorState.STANDING][0]

            # draw_x = self.x - self.image.get_width() // 2
            # draw_y = self.y - self.image.get_height()
            # self.rect = self.image.get_rect(topleft=(draw_x, draw_y))
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))


    def move_towards1(self,  delta_time):
        # Calculate the direction vector
        direction_x = self.target_x - self.x
        direction_y = self.target_y - self.y

        # Calculate distance
        distance = (direction_x**2 + direction_y**2) ** 0.5

        if distance > 0:
            # Normalize direction vector
            direction_x /= distance
            direction_y /= distance
            
            # Calculate movement based on speed and delta time
            movement = self.speed * delta_time
            
            # Move the actor
            if movement < distance:
                # self.x += direction_x * movement
                # self.y += direction_y * movement
                self.move(direction_x * movement, direction_y * movement)
            else:
                # Snap to the target if within movement distance
                self.x = self.target_x
                self.y = self.target_y
        else:
            self.stop()


    def set_frames(self, state: ActorState, frames: List[pygame.Surface]) -> None:
        """Set animation frames for a given state.

        Args:
            state: The actor state.
            frames: List of pygame.Surface objects for animation.
        """
        self.frames[state] = frames
        if state == self.state and len(frames) > 0:
            self.current_frame_index = 0
            self.image = frames[0]


    def set_state(self, new_state: ActorState) -> None:
        """Change the actor state.

        Args:
            new_state: The new state to transition to.
        """
        if new_state != self.state:
            self.previous_state = self.state
            self.state = new_state
            self.current_frame_index = 0
            self.frame_timer = 0.0


    def update(self, dt: float) -> None:
        """Update the actor, including animation and position.

        Args:
            dt: Delta time since last frame in seconds.
        """
        if self.state == ActorState.WALKING_LEFT or self.state == ActorState.WALKING_RIGHT:
            self.move_towards1(dt)

        # Update animation frame
        if len(self.frames[self.state]) > 0:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames[self.state])
                self.image = self.frames[self.state][self.current_frame_index]

        # Update rect position
        self.rect.midbottom = (int(self.x), int(self.y))


    def draw(self, surface: pygame.Surface) -> None:
        """Draw the actor on the given surface.

        Args:
            surface: The pygame Surface to draw on.
        """
        surface.blit(self.image, self.rect)

        # draw_x = self.x - self.rect.width // 2
        # draw_y = self.y - self.rect.height

        # surface.blit(self.image, (draw_x, draw_y))
        

    def run(self, dt: float) -> None:
        """Execute actor logic for the current frame.

        This method can be overridden in subclasses for custom behavior.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Default implementation: just update animation
        self.update(dt)


    def move(self, dx: float, dy: float) -> None:
        """Move the actor by a relative offset.

        Args:
            dx: Change in x position.
            dy: Change in y position.
        """
        self.x += dx
        self.y += dy
        self.rect.midbottom = (int(self.x), int(self.y))


    def set_position(self, x: int, y: int) -> None:
        """Set the actor's absolute position.

        Args:
            x: New x position.
            y: New y position.
        """
        self.x = x
        self.y = y
        self.rect.midbottom = (self.x, self.y)


    def get_position(self) -> tuple:
        """Get the actor's current position.

        Returns:
            Tuple of (x, y) coordinates.
        """
        return (self.x, self.y)


    def get_state(self) -> ActorState:
        """Get the actor's current state.

        Returns:
            The current ActorState.
        """
        return self.state


    def walk_to(self, new_target_x: int, new_target_y: int) -> None:
        """Set the actor's target position to walk towards.

        Args:
            new_target_x: New target x coordinate.
            new_target_y: New target y coordinate.
        """
        self.target_x = new_target_x
        self.target_y = new_target_y

        if self.x < new_target_x:
            self.set_state(ActorState.WALKING_RIGHT)
        else:
            self.set_state(ActorState.WALKING_LEFT)


    def stop(self) -> None:
        """Stop the actor's movement and set state to standing."""
        self.set_state(ActorState.STANDING)
        self.target_x = self.x
        self.target_y = self.y


    def is_idle(self) -> bool:
        """Check if the actor is currently idle (not walking).

        Returns:
            True if the actor is standing, False otherwise.
        """
        return self.state == ActorState.STANDING
    

    def is_walking(self) -> bool:
        """Check if the actor is currently walking.

        Returns:
            True if the actor is walking, False otherwise.
        """
        return self.state in (ActorState.WALKING_LEFT, ActorState.WALKING_RIGHT)
    
    def increase_speed(self) -> None:
        self.speed += SPEED_INCREMENT

    def decrease_speed(self) -> None:
        self.speed -= SPEED_INCREMENT
