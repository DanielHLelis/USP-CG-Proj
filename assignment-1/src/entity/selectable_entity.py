from typing import Optional, Callable, Any

import glm
import glfw

from model import Model
from camera import Camera

from .entity import Entity


class SelectableEntity(Entity):
    name: str
    select_key: int
    selected: bool
    pressed_keys: set

    angle_x: float
    angle_y: float
    angle_z: float

    rotation_speed: float
    movement_speed: float
    scale_speed: float

    log_position: bool

    def __init__(
        self,
        key: int,
        name: str,
        model: Model,
        position=glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        angle_x: float = 0.0,
        angle_y: float = 0.0,
        angle_z: float = 0.0,
        rotation_speed: float = 180.0,
        movement_speed: float = 5.0,
        scale_speed: float = 0.5,
        log_position: bool = False,
        **kwargs,
    ):
        super().__init__(
            model,
            **kwargs,
        )

        self.position = position
        self.scale = scale
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z

        self.name = name
        self.select_key = key
        self.selected = False
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.scale_speed = scale_speed
        self.pressed_keys = set()
        self.log_position = log_position

    def update(self, dt: float, camera: Camera):
        if not self.selected:
            return

        # If ALT is pressed, change rotation
        if glfw.KEY_LEFT_ALT in self.pressed_keys:
            for key in self.pressed_keys:
                match key:
                    # Yaw
                    case glfw.KEY_I:
                        self.angle_x += self.rotation_speed * dt
                    case glfw.KEY_K:
                        self.angle_x -= self.rotation_speed * dt
                    # Pitch
                    case glfw.KEY_J:
                        self.angle_y += self.rotation_speed * dt
                    case glfw.KEY_L:
                        self.angle_y -= self.rotation_speed * dt
                    # Roll
                    case glfw.KEY_O:
                        self.angle_z += self.rotation_speed * dt
                    case glfw.KEY_U:
                        self.angle_z -= self.rotation_speed * dt
        else:
            for key in self.pressed_keys:
                match key:
                    # Use UIOP for moving and OU for vertical and YH for scale
                    case glfw.KEY_I:
                        self.position.z -= self.movement_speed * dt
                    case glfw.KEY_K:
                        self.position.z += self.movement_speed * dt
                    case glfw.KEY_J:
                        self.position.x -= self.movement_speed * dt
                    case glfw.KEY_L:
                        self.position.x += self.movement_speed * dt
                    case glfw.KEY_U:
                        self.position.y -= self.movement_speed * dt
                    case glfw.KEY_O:
                        self.position.y += self.movement_speed * dt
                    case glfw.KEY_Y:
                        self.scale = self.scale * (1.0 + (self.scale_speed * dt))
                    case glfw.KEY_H:
                        self.scale = self.scale / (1.0 + (self.scale_speed * dt))

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        def handler(win, key, scancode, action, mods):
            if key == self.select_key and action == glfw.PRESS:
                self.selected = not self.selected
                if self.selected:
                    print(f"{self.name} selected")
                else:
                    print(f"{self.name} de-selected")

            if key in (
                glfw.KEY_I,
                glfw.KEY_J,
                glfw.KEY_K,
                glfw.KEY_L,
                glfw.KEY_U,
                glfw.KEY_O,
                glfw.KEY_Y,
                glfw.KEY_H,
                glfw.KEY_LEFT_ALT,
            ):
                if action == glfw.PRESS:
                    self.pressed_keys.add(key)
                elif action == glfw.RELEASE:
                    self.pressed_keys.remove(key)

            if (
                self.selected
                and self.log_position
                and key == glfw.KEY_Z
                and action == glfw.PRESS
            ):
                print(
                    f"Entity ({self.name}): position({self.position}) scale({self.scale.x}, {self.scale.y}, {self.scale.z}) rotation({self.angle_x}, {self.angle_y}, {self.angle_z})"
                )

        return handler
