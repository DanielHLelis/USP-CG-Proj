from typing import Optional, Callable, Any, Dict

from glfw import os

from wavefront import load_file

import numpy as np
import OpenGL.GL as gl
import glm


class Material:
    program_id: int
    texture_id: int
    texture_path: Optional[str]

    def __init__(self, proogram_id: int, texture_path: Optional[str] = None):
        self.program_id = proogram_id
        self.texture_id = 0
        self.texture_path = texture_path

    @staticmethod
    def from_texture(program_id: int, texture_path: str) -> "Material":
        if not os.path.isfile(texture_path):
            raise FileNotFoundError(f"Texture file {texture_path} not found")

        return Material(program_id, texture_path)


class Model:
    vertices: np.ndarray
    texture_coords: np.ndarray
    materials: Dict[Any, Material]
    material_swaps: Dict[int, Any]
    draw_mode: int

    offset: int
    texture_offset: int

    def __init__(
        self,
        vertices: np.ndarray,
        texture_coords: np.ndarray,
        materials: Dict[str, Material],
        material_swaps: Dict[int, str] = {0: "default"},
        draw_mode=gl.GL_TRIANGLES,
    ):
        assert len(vertices) == len(
            texture_coords
        ), "Vertices and texture coordinates must have the same length"
        assert (
            min(material_swaps.keys()) >= 0
        ), "Material swaps must have non-negative keys"
        assert max(material_swaps.keys()) < len(
            vertices
        ), "Material swaps must have keys less than the number of vertices"
        assert all(
            [material in materials for material in material_swaps.values()]
        ), "Material swaps must have valid materials"

        self.vertices = vertices.astype(np.float32)
        self.texture_coords = texture_coords.astype(np.float32)
        self.materials = materials
        self.material_swaps = material_swaps
        self.draw_mode = draw_mode
        self.offset = 0
        self.texture_offset = 0

    @classmethod
    def load_obj(
        cls, filepath: str, materials: Dict[str, Material], prefix_materials: str = ""
    ) -> "Model":
        model = load_file(filepath)
        texture_coords = []
        vertices = []

        material_swaps = {}
        last_material = None

        for i, face in enumerate(model["faces"]):
            cur_material = prefix_materials + face[2]
            if last_material != cur_material:
                material_swaps[i * 3] = cur_material
                last_material = cur_material
            for vertex in face[0]:
                vertices.append(model["vertices"][vertex - 1])
            for texture in face[1]:
                texture_coords.append(model["texture"][texture - 1])

        vertices = np.array(vertices, dtype=np.float32)
        texture_coords = np.array(texture_coords, dtype=np.float32)

        return Model(vertices, texture_coords, materials, material_swaps)


class Entity:
    model: Model
    position: glm.vec3
    scale: glm.vec3
    rotation: glm.vec3
    angle: float

    visible: bool  # Whether to draw the entity or not

    def __init__(
        self,
        model: Model,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        rotation: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        angle: float = 90,
        visible: bool = True,
        draw_mode: int = gl.GL_TRIANGLES,
    ):
        self.model = model
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.angle = angle
        self.visible = visible
        self.draw_mode = draw_mode

    def update(self, dt: int):
        # By default, do nothing
        pass

    def key_handler(self) -> Optional[Callable[[Any, int, int, int, int], None]]:
        pass

    def cursor_handler(
        self,
    ) -> Optional[Callable[[Any, float, float, float, float], None]]:
        pass
