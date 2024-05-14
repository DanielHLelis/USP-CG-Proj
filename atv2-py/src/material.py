from typing import Optional, Iterable

from glfw import os
import OpenGL.GL as gl
from PIL import Image

from shader import Shader


class Material:
    shader: Shader
    texture_id: int
    texture_path: Optional[str]

    def __init__(self, shader: Shader, texture_path: Optional[str] = None):
        self.shader = shader
        self.texture_id = 0
        self.texture_path = texture_path

    @staticmethod
    def from_texture(shader: Shader, texture_path: str) -> "Material":
        if not os.path.isfile(texture_path):
            raise FileNotFoundError(f"Texture file {texture_path} not found")

        return Material(shader, texture_path)

    @staticmethod
    def setup_all(materials: Iterable["Material"]) -> None:
        for material in materials:
            material.setup_texture()

    def setup_texture(self) -> None:
        # Skip if there is no texture
        if self.texture_path is None:
            return

        # Create the texture
        texture = gl.glGenTextures(1)
        self.texture_id = texture

        # Load the image
        img = Image.open(self.texture_path)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

        # Select the texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        # Set the texture filtering parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        # Load the texture
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            img.width,
            img.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            img_data,
        )
