# CG 2024.1 - Assignment 2
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

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
    ambient_color: np.ndarray
    ambient_intensity: float

    def __init__(
        self,
        polygon_mode: bool = False,
        ambient_color: np.ndarray = np.array([1.0, 1.0, 1.0, 1.0]),
        ambient_intensity: float = 1.0,
    ) -> None:
        self.polygon_mode = polygon_mode
        self.ambient_color = ambient_color
        self.ambient_intensity = ambient_intensity

    def _model_matrix(self, entity: Entity) -> np.ndarray:
        # rad_angle = np.radians(entity.angle)

        mat = glm.mat4(1.0)
        mat = glm.translate(mat, entity.position)
        # Join these rotations later
        mat = glm.rotate(
            mat,
            glm.radians(entity.angle_x),
            glm.vec3(1.0, 0.0, 0.0),
        )
        mat = glm.rotate(
            mat,
            glm.radians(entity.angle_y),
            glm.vec3(0.0, 1.0, 0.0),
        )
        mat = glm.rotate(
            mat,
            glm.radians(entity.angle_z),
            glm.vec3(0.0, 0.0, 1.0),
        )
        mat = glm.scale(
            mat,
            entity.scale,
        )
        return np.array(mat, dtype=np.float32)

    def _view_matrix(self, camera: Camera) -> np.ndarray:
        view = glm.lookAt(camera.position, camera.target, camera.up)
        return np.array(view, dtype=np.float32)

    def _projection_matrix(self, camera: Camera):
        projection = glm.perspective(
            glm.radians(camera.fov), camera.aspect_ratio, camera.near, camera.far
        )
        return np.array(projection, dtype=np.float32)

    def _bootstrap_lighting(self, shader: Shader, camera: Camera):
        pass

        # TODO

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
        light_sources = entity.light_sources
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

            # Load model
            gl.glUniformMatrix4fv(material.shader.model_loc, 1, gl.GL_TRUE, mat)

            # Load view & projection
            self.setup_camera(material.shader, camera)

            # Setup camera position
            gl.glUniform3fv(
                material.shader.view_pos_loc,
                1,
                np.array(camera.position, dtype=np.float32),
            )

            # Setup ambient lights
            gl.glUniform3fv(material.shader.ambient_color_loc, 1, self.ambient_color)
            gl.glUniform1f(
                material.shader.ambient_intensity_loc, self.ambient_intensity
            )

            # Setup light sources
            gl.glUniform1i(material.shader.light_count_loc, len(light_sources))
            for i in range(len(light_sources)):
                gl.glUniform3fv(
                    material.shader.light_positions_loc + i,
                    1,
                    np.array(light_sources[i].position),
                )
                gl.glUniform3fv(
                    material.shader.light_colors_loc + i,
                    1,
                    np.array(light_sources[i].color),
                )
                gl.glUniform3fv(
                    material.shader.light_decay_loc + i,
                    1,
                    np.array(light_sources[i].decay_coefs),
                )
                gl.glUniform1f(
                    material.shader.light_intensities_d_loc + i,
                    light_sources[i].intensity_d,
                )
                gl.glUniform1f(
                    material.shader.light_intensities_s_loc + i,
                    light_sources[i].intensity_s,
                )

            # Material properties
            gl.glUniform3fv(material.shader.ka_loc, 1, material.ka)
            gl.glUniform3fv(material.shader.kd_loc, 1, material.kd)
            gl.glUniform3fv(material.shader.ks_loc, 1, material.ks)
            gl.glUniform1fv(material.shader.ns_loc, 1, material.ns)
            gl.glUniform1fv(material.shader.d_loc, 1, material.d)

            # Ignore lighting
            gl.glUniform1i(material.shader.ignore_lighting_loc, entity.ignore_lighting)

            # Set texture
            gl.glBindTexture(
                gl.GL_TEXTURE_2D,
                material.texture_id,
            )

            # Draw segment
            gl.glDrawArrays(model.draw_mode, model.offset + start, end - start)
