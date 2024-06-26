# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

from typing import Optional, Iterable

import numpy as np
from glfw import os
import OpenGL.GL as gl
from PIL import Image

from shader import Shader
from wavefront import load_mtllib


class Material:
    shader: Shader
    texture_id: int
    texture_path: Optional[str]
    ka: np.ndarray
    kd: np.ndarray
    ks: np.ndarray
    ns: float
    d: float

    def __init__(
        self,
        shader: Shader,
        texture_path: Optional[str] = None,
        ka: np.ndarray = np.array([1.0, 1.0, 1.0]),
        kd: np.ndarray = np.array([1.0, 1.0, 1.0]),
        ks: np.ndarray = np.array([1.0, 1.0, 1.0]),
        ns: float = 0,
        d: float = 1.0,
    ):
        assert shader is not None, "Shader must be provided"

        self.shader = shader
        self.texture_id = 0
        self.texture_path = texture_path

        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ns = ns
        self.d = d

    @staticmethod
    def from_texture(shader: Shader, texture_path: str) -> "Material":
        """Loads a material from a shader and texture path"""
        if not os.path.isfile(texture_path):
            raise FileNotFoundError(f"Texture file {texture_path} not found")

        return Material(shader, texture_path)

    @staticmethod
    def load_mtllib(
        shader: Shader,
        filepath: str,
        prefix: str = "",
        overwrite_ka_with_kd: bool = False,
    ) -> dict[str, "Material"]:
        materials = load_mtllib(filepath)
        parsed_materials = {}
        for material_name, material in materials.items():
            texture_path = None

            # Check for texture
            if "map_Kd" in material:
                texture_path = os.path.realpath(
                    os.path.join(os.path.dirname(filepath), material["map_Kd"])
                )

            kd = material["Kd"] if "Kd" in material else np.array([0.0, 0.0, 0.0])
            ka = material["Ka"] if "Ka" in material else kd
            ks = material["Ks"] if "Ks" in material else np.array([1.0, 1.0, 1.0])
            d = float(material["d"]) if "d" in material else 1.0

            if overwrite_ka_with_kd:
                ka = kd

            ns = material["Ni"] if "Ni" in material else 0.0

            parsed_materials[prefix + material_name] = Material(
                shader, texture_path, ka, kd, ks, ns, d
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
