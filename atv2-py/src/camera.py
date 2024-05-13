from typing import Any, Optional

import glm
import glfw
import numpy as np

class Camera:
    position: glm.vec3
    yaw: float
    pitch: float
    fov: float
    up: glm.vec3

    aspect_ratio: float
    near: float
    far: float

    sensitivity_x: float
    sensitivity_y: float
    _previous_x: Optional[float]
    _previous_y: Optional[float]


    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 0.0),
        yaw=180.0,
        pitch=0.0,
        up=glm.vec3(0.0, 1.0, 0.0),
        fov=90.0,
        aspect_ratio = 1.0,
        near=0.1,
        far=100.0,
        sensitivity_x=0.1,
        sensitivity_y=0.1,
    ):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.fov = fov
        self.up = up
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        self.sensitivity_x = sensitivity_x
        self.sensitivity_y = sensitivity_y

        self._previous_x = None
        self._previous_y = None


    def update(self, win, program, dt: float):
        w, h = glfw.get_framebuffer_size(win)
        self.aspect_ratio = w / h

        pass


    def cursor_handler(self, win: Any, x: float, y: float, rel_x: float, rel_y: float):
        if self._previous_x is None or self._previous_y is None:
            self._previous_x = x
            self._previous_y = y
            return

        # Compute the current movement
        dx = x - self._previous_x
        dy = y - self._previous_y

        # Weigh the movement by the sensitivity
        dx *= self.sensitivity_x
        dy *= self.sensitivity_y

        # Compute the new yaw and pitch
        self.yaw = (self.yaw + dx) % 360.0
        self.pitch = np.clip(self.pitch + dy, -89.0, 89.0)

        # Update history
        self._previous_x = x
        self._previous_y = y
    

    @property
    def front(self) -> glm.vec3:
        front = glm.vec3()
        front.x = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        front.y = np.sin(np.radians(self.pitch))
        front.z = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        return glm.normalize(front)

    @property
    def target(self) -> glm.vec3:
        return self.position + self.front
