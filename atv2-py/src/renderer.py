from typing import Any

import numpy as np
import OpenGL.GL as gl
import glm

from entity import Entity, Shader
from camera import Camera


class Renderer:

    # _current_program: int

    def __init__(
        self,
    ) -> None:
        # self._current_program = -1
        pass

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

    def setup_camera(self, shader: Shader, camera: Camera):

        view = self._view_matrix(camera)
        projection = self._projection_matrix(camera)

        gl.glUniformMatrix4fv(shader.view_loc, 1, gl.GL_TRUE, view)
        gl.glUniformMatrix4fv(shader.projection_loc, 1, gl.GL_TRUE, projection)

    def render(self, entity: Entity, camera: Camera) -> None:
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

            # Check if a program swap is needed
            # if self._current_program != material.program_id:
            material.shader.use()
            self.setup_camera(material.shader, camera)
            gl.glUniformMatrix4fv(material.shader.model_loc, 1, gl.GL_TRUE, mat)

            # Set texture
            gl.glBindTexture(
                gl.GL_TEXTURE_2D,
                material.texture_id,
            )

            # Draw segment
            gl.glDrawArrays(model.draw_mode, model.offset + start, end - start)
