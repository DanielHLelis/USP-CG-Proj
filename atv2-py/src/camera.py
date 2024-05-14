from typing import Any, Optional

import glm
import glfw
import numpy as np


class Camera:
    position: glm.vec3
    yaw: float
    pitch: float
    _fov: float
    up: glm.vec3
    _front: glm.vec3

    aspect_ratio: float
    near: float
    far: float

    sensitivity_x: float
    sensitivity_y: float

    move_xyz: bool
    base_speed: float
    base_fov: float
    running_speed: float
    running_fov: float

    fov_interpolation: float
    speed_interpolation: float

    _previous_x: Optional[float]
    _previous_y: Optional[float]
    _pressed_keys: set[int]
    _fov: float
    _movement_speed: float

    # TODO: Document the class and its methods
    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 0.0),
        yaw=180.0,
        pitch=0.0,
        up=glm.vec3(0.0, 1.0, 0.0),
        aspect_ratio=1.0,
        near=0.1,
        far=5100.0,
        sensitivity_x=0.05,
        sensitivity_y=0.05,
        move_xyz=True,
        base_speed=10.0,
        base_fov=80.0,
        running_speed=25.0,
        running_fov=90.0,
        fov_interpolation=4.0,
        speed_interpolation=4.0,
    ):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.up = up

        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far

        self.sensitivity_x = sensitivity_x
        self.sensitivity_y = sensitivity_y

        self.move_xyz = move_xyz

        self.base_fov = base_fov
        self.base_speed = base_speed
        self.running_speed = running_speed
        self.running_fov = running_fov

        self.fov_interpolation = fov_interpolation
        self.speed_interpolation = speed_interpolation

        self._previous_x = None
        self._previous_y = None
        self._pressed_keys = set()
        self._front = self.update_front()
        self._fov = base_fov
        self._movement_speed = 0.0

    def _update_aspect_ratio(self, win):
        w, h = glfw.get_framebuffer_size(win)
        self.aspect_ratio = w / h

    def _update_speed_and_fov(self, dt: float):
        if glfw.KEY_LEFT_SHIFT in self._pressed_keys:
            self._movement_speed = np.clip(
                self._movement_speed
                + (self.running_speed - self.base_speed)
                * dt
                * self.speed_interpolation,
                self.base_speed,
                self.running_speed,
            )
            self._fov = np.clip(
                self._fov
                + (self.running_fov - self.base_fov) * dt * self.fov_interpolation,
                self.base_fov,
                self.running_fov,
            )
        else:
            self._movement_speed = np.clip(
                self._movement_speed
                - (self.running_speed - self.base_speed)
                * dt
                * self.speed_interpolation,
                self.base_speed,
                self.running_speed,
            )
            self._fov = np.clip(
                self._fov
                - (self.running_fov - self.base_fov) * dt * self.fov_interpolation,
                self.base_fov,
                self.running_fov,
            )

    def _update_position(self, dt: float):
        self._update_speed_and_fov(dt)

        if self.move_xyz:
            for key in self._pressed_keys:
                match key:
                    case glfw.KEY_W:
                        self.position += self._movement_speed * dt * self._front
                    case glfw.KEY_S:
                        self.position -= self._movement_speed * dt * self._front
                    case glfw.KEY_A:
                        self.position -= (
                            glm.normalize(glm.cross(self._front, self.up))
                            * dt
                            * self._movement_speed
                        )
                    case glfw.KEY_D:
                        self.position += (
                            glm.normalize(glm.cross(self._front, self.up))
                            * dt
                            * self._movement_speed
                        )
                    case glfw.KEY_SPACE:
                        self.position += self.up * dt * self._movement_speed
                    case glfw.KEY_LEFT_CONTROL:
                        self.position -= self.up * dt * self._movement_speed
        else:
            for key in self._pressed_keys:
                no_z_front = glm.normalize(self._front * glm.vec3(1.0, 0.0, 1.0))
                match key:
                    case glfw.KEY_W:
                        self.position += self._movement_speed * dt * no_z_front
                    case glfw.KEY_S:
                        self.position -= self._movement_speed * dt * no_z_front
                    case glfw.KEY_A:
                        self.position -= (
                            glm.normalize(glm.cross(no_z_front, self.up))
                            * dt
                            * self._movement_speed
                        )
                    case glfw.KEY_D:
                        self.position += (
                            glm.normalize(glm.cross(no_z_front, self.up))
                            * dt
                            * self._movement_speed
                        )
                    case glfw.KEY_SPACE:
                        self.position += self.up * dt * self._movement_speed
                    case glfw.KEY_LEFT_CONTROL:
                        self.position -= self.up * dt * self._movement_speed

        # Clamp position
        if self.position.y < 0.0:
            self.position.y = 0.0

        if self.position.y > 100.0:
            self.position.y = 100.0

    def update(self, win, program, dt: float):
        self._update_aspect_ratio(win)
        self._update_position(dt)

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
        self.pitch = np.clip(self.pitch - dy, -89.9, 89.9)

        # Update history
        self._previous_x = x
        self._previous_y = y

        self._front = self.update_front()

    def key_handler(self, win: Any, key: int, scancode: int, action: int, modes: int):
        # Update the movement keys
        if key in (
            glfw.KEY_W,
            glfw.KEY_S,
            glfw.KEY_A,
            glfw.KEY_D,
            glfw.KEY_SPACE,
            glfw.KEY_LEFT_CONTROL,
            glfw.KEY_LEFT_SHIFT,
        ):
            if action == glfw.PRESS:
                self._pressed_keys.add(key)
            elif action == glfw.RELEASE:
                self._pressed_keys.remove(key)

    def update_front(self) -> glm.vec3:
        front = glm.vec3()
        front.x = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        front.y = np.sin(np.radians(self.pitch))
        front.z = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        return glm.normalize(front)

    @property
    def fov(self) -> float:
        return self._fov

    @property
    def target(self) -> glm.vec3:
        return self.position + self._front
