from typing import Optional, Iterable

from glfw import os
import glm
import OpenGL.GL as gl
from PIL import Image

from shader import Shader
from wavefront import load_mtllib

class Material:
    shader: Shader
    texture_id: int
    texture_path: Optional[str]
    color: glm.vec4

    def __init__(
        self,
        shader: Shader,
        texture_path: Optional[str] = None,
        color: Optional[glm.vec4] = None,
    ):
        assert shader is not None, "Shader must be provided"

        self.shader = shader
        self.texture_id = 0
        self.texture_path = texture_path
        if texture_path is not None:
            self.color = glm.vec4(0.0, 0.0, 0.0, 0.0)
        else:
            self.color = glm.vec4(1.0, 1.0, 1.0, 1.0) if color is None else color

    @property
    def texture_filter(self) -> glm.vec4:
        if self.texture_path is None:
            return glm.vec4(0.0, 0.0, 0.0, 0.0)
        else:
            return glm.vec4(
                1.0,
                1.0,
                1.0,
                1.0,
            )

    @staticmethod
    def from_texture(shader: Shader, texture_path: str) -> "Material":
        """Loads a material from a shader and texture path"""
        if not os.path.isfile(texture_path):
            raise FileNotFoundError(f"Texture file {texture_path} not found")

        return Material(shader, texture_path)

    @staticmethod
    def load_mtllib(
        shader: Shader, filepath: str, prefix: str = ""
    ) -> dict[str, "Material"]:
        materials = load_mtllib(filepath)
        parsed_materials = {}
        for material_name, material in materials.items():
            texture_path = None
            color = None
            # Check for texture
            if "map_Kd" in material:
                texture_path = os.path.realpath(
                    os.path.join(os.path.dirname(filepath), material["map_Kd"])
                )
            # Check for color
            if "Kd" in material:
                d = 1.0
                if "d" in material:
                    d = float(material["d"])
                color = glm.vec4(*material["Kd"], d)

            parsed_materials[prefix + material_name] = Material(
                shader, texture_path, color
            )

        return parsed_materials

    @staticmethod
    def setup_all(materials: Iterable["Material"]) -> None:
        """Sets up all materials"""
        for material in materials:
            material.setup_texture()

    def setup_texture(self) -> None:
        """Sets up a texture"""
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
