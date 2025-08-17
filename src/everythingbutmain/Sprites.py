"""
This file holds the code for the player (Avatar) and the AnimationSequence.
The Avatar class controls the position and movement of the player. It sets the players action and grabs the sprite. It
also draws the player on the screen and creates a non-visible rectangle around the player to detect collisions.
The AnimationSequence class runs through the sprite. It grabs the current image and updates it based on the sprite
until the animation is compleat.
"""

# Separate definition of the Player class (could be in another module)
import pygame


class Avatar:
    def __init__(self, maingame, avatar_type, position, size, gesture=None):
        """Player class definition. Controls the movements of the player and finds its position in the game."""
        self.maingame = maingame  # Reference to the Game instance
        self.avatar_type = avatar_type  # Set the type of the player entity
        self.position = list(position)  # Initialize the player's position as a list
        self.size = size  # Set the player's size
        self.avatar_velocity = [0, 0]  # Initialize the player's velocity
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  # Collision status

        self.gesture = gesture
        try:
            if self.gesture != None:
                self.sprite = self.maingame.resources[self.avatar_type + '/' + self.gesture]
            else:
                self.sprite = self.maingame.resources[self.avatar_type]
        except KeyError:
            if self.avatar_type == 'seaMonster':
                self.sprite = None
            else:
                self.sprite = self.maingame.resources[self.avatar_type]

        # Current action of the player
        self.distance = (-2, -2)  # Offset for the animation rendering
        self.rotate = False  # Whether to flip the sprite horizontally

        self.airBourne = 0  # Counter for the time spent in the air

    def rect(self):
        """Function to get the player's collision rectangle."""
        return pygame.Rect(self.position[0], self.position[1], self.size[0],
                           self.size[1])  # Return a Pygame rectangle representing the player's position and size

    def set_gesture(self, gesture):
        """Function to set the player's action (animation state)."""
        if gesture != self.gesture:  # If the new action is different from the current action
            self.gesture = gesture  # Update the current action
            self.sprite = self.maingame.resources[
                self.avatar_type + '/' + self.gesture].duplicate()  # Copy the animation for the new action

    def update_avatar(self, tilemap, movement=(0, 0)):
        """Function to update the player's state."""
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  # Reset collision status

        # Calculate movement based on user input and velocity
        frame_movement = (movement[0] + self.avatar_velocity[0], movement[1] + self.avatar_velocity[1])

        self.position[0] += frame_movement[0]  # Update the player's horizontal position
        entity_rect = self.rect()  # Get the player's collision rectangle
        for rect in self.maingame.physics_rectangles(
                self.position):  # Check for collisions with surrounding physics rectangles
            if entity_rect.colliderect(rect):  # If a collision is detected
                if frame_movement[0] > 0:  # If moving right
                    entity_rect.right = rect.left  # Move the player to the left edge of the collision rectangle
                    self.collisions['right'] = True  # Set right collision status
                if frame_movement[0] < 0:  # If moving left
                    entity_rect.left = rect.right  # Move the player to the right edge of the collision rectangle
                    self.collisions['left'] = True  # Set left collision status
                self.position[0] = entity_rect.x  # Update the player's position

        self.position[1] += frame_movement[1]  # Update the player's vertical position
        entity_rect = self.rect()  # Get the player's collision rectangle
        for rect in self.maingame.physics_rectangles(
                self.position):  # Check for collisions with surrounding physics rectangles
            if entity_rect.colliderect(rect):  # If a collision is detected
                if frame_movement[1] > 0:  # If moving down
                    entity_rect.bottom = rect.top  # Move the player to the top edge of the collision rectangle
                    self.collisions['down'] = True  # Set down collision status
                if frame_movement[1] < 0:  # If moving up
                    entity_rect.top = rect.bottom  # Move the player to the bottom edge of the collision rectangle
                    self.collisions['up'] = True  # Set up collision status
                self.position[1] = entity_rect.y  # Update the player's position

        # Update the player's facing direction based on movement
        if movement[0] > 0:
            self.rotate = False  # Not flipped when moving right
        if movement[0] < 0:
            self.rotate = True  # Flipped when moving left

        self.avatar_velocity[1] = min(4, self.avatar_velocity[1] + 0.1)  # Increase downward velocity, capping at 4

        # Reset vertical velocity when colliding with ground or ceiling
        if self.collisions['down'] or self.collisions['up']:
            self.avatar_velocity[1] = 0
        self.airBourne += 1  # Increment air time
        if self.collisions['down']:  # Reset air time if on the ground
            self.airBourne = 0

        # Set player's action based on state
        if self.airBourne > 4:  # If in the air for too long, set action to jump
            self.set_gesture('jump')
        elif movement[0] != 0:  # If moving horizontally, set action to run
            self.set_gesture('run')

        else:  # Otherwise, set action to idle
            self.set_gesture('idle')

        self.sprite.advance()  # Update the current animation frame

    def update_NPC(self):
        """Function to go through the sprite of the NPC."""
        self.sprite.advance()

    def render(self, surf, offset=(0, 0)):
        """Function to render the player on a given surface with an offset"""
        surf.blit(pygame.transform.flip(self.sprite.current_image(), self.rotate, False),
                  (self.position[0] - offset[0] + self.distance[0],
                   self.position[1] - offset[1] + self.distance[1]))  # Position the image with the offset


class AnimationSequence:
    def __init__(self, frames, duration_per_frame=5, is_looping=True):
        """Allows us to have animation in our game."""
        self.frames = frames  # Store the list of images for the animation
        self.is_looping = is_looping  # Whether the animation should loop
        self.duration_per_frame = duration_per_frame  # Duration of each image frame in the animation
        self.is_complete = False  # Whether the animation has finished
        self.current_frame_index = 0  # Current frame index in the animation

    def duplicate(self):
        """Function to copy the animation (for state management)"""
        return AnimationSequence(self.frames, self.duration_per_frame,
                                 self.is_looping)  # Return a new instance of the Animation class

    def advance(self):
        """Function to update the animation frame."""
        if self.is_looping:  # If the animation should loop
            self.current_frame_index = (self.current_frame_index + 1) % (
                        self.duration_per_frame * len(self.frames))  # Loop through frames
        else:  # If the animation should not loop
            self.current_frame_index = min(self.current_frame_index + 1, self.duration_per_frame * len(
                self.frames) - 1)  # Advance frame but cap at the last frame
            if self.current_frame_index >= self.duration_per_frame * len(
                    self.frames) - 1:  # If the last frame is reached
                self.is_complete = True  # Mark the animation as done

    def current_image(self):
        """Function to get the current image frame for rendering."""
        return self.frames[
            int(self.current_frame_index / self.duration_per_frame)]  # Return the current image frame based on the current frame index and image duration
