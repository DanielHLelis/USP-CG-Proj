from typing import Any, cast
import glfw
import numpy as np
import OpenGL.GL as gl
import glm

from entity import Entity
from shader import Shader
from camera import Camera


class Renderer:
    polygon_mode: bool

    def __init__(
        self,
        polygon_mode: bool = False,
    ) -> None:
        self.polygon_mode = polygon_mode

    def _model_matrix(self, entity: Entity) -> np.ndarray:
        rad_angle = np.radians(entity.angle)

        mat = glm.mat4(1.0)
        mat = glm.translate(mat, entity.position)
        mat = glm.rotate(
            mat,
            rad_angle,
            entity.rotation,
        )
        mat = glm.scale(
            mat,
            entity.scale,
        )
        return np.array(mat, dtype=np.float32).T

    def _view_matrix(self, camera: Camera) -> np.ndarray:
        view = glm.lookAt(camera.position, camera.target, camera.up)
        return np.array(view).T

    def _projection_matrix(self, camera: Camera):
        projection = glm.perspective(
            glm.radians(camera.fov), camera.aspect_ratio, camera.near, camera.far
        )
        return np.array(projection).T

    def key_handler(
        self,
        win: Any,
        key: int,
        scancode: int,
        action: int,
        mods: int,
    ) -> None:
        """Handles the keyboard event to enter and exit the polygon mode"""
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.polygon_mode = not self.polygon_mode

    def init(self):
        """Initializes the render stage"""
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDepthMask(gl.GL_TRUE)

    def pre_render(self) -> None:
        """Clears the buffer and prepares the pre-render"""
        # Clean the screen
        gl.glClear(
            cast(int, gl.GL_COLOR_BUFFER_BIT) | cast(int, gl.GL_DEPTH_BUFFER_BIT)
        )
        gl.glClearColor(0, 0, 0, 0)

        # Set polygon mode
        if self.polygon_mode:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    def setup_camera(self, shader: Shader, camera: Camera):
        """Sets up the camera"""
        view = self._view_matrix(camera)
        projection = self._projection_matrix(camera)

        gl.glUniformMatrix4fv(shader.view_loc, 1, gl.GL_TRUE, view)
        gl.glUniformMatrix4fv(shader.projection_loc, 1, gl.GL_TRUE, projection)

    def draw_entity(self, entity: Entity, camera: Camera) -> None:
        """Draws an entity based on it's components and the camera's attributes"""
        model = entity.model

        mat = self._model_matrix(entity)

        # Separate the model into segments per material
        segments = list(model.material_swaps.keys()) + [len(model.vertices)]

        # Render each segment
        for i in range(len(segments) - 1):
            # Segment endpoints
            start = segments[i]
            end = segments[i + 1]

            # Get material
            material = model.materials[model.material_swaps[start]]

            # Activate the right shader (does this have a big performance impact?)
            material.shader.use()
            self.setup_camera(material.shader, camera)
            gl.glUniformMatrix4fv(material.shader.model_loc, 1, gl.GL_TRUE, mat)
            gl.glUniform4fv(material.shader.color_loc, 1, np.array(material.color))
            gl.glUniform4fv(
                material.shader.texture_filter_loc, 1, np.array(material.texture_filter)
            )

            # Set texture
            gl.glBindTexture(
                gl.GL_TEXTURE_2D,
                material.texture_id,
            )

            # Draw segment
            gl.glDrawArrays(model.draw_mode, model.offset + start, end - start)
