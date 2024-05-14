from typing import Any, Dict, Iterable, List, cast

import numpy as np
import OpenGL.GL as gl

from shader import Shader
from material import Material
from wavefront import load_file


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
        cls,
        filepath: str,
        materials: Dict[str, Material],
        prefix_materials: str = "",
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


class Buffers:
    vertex_buffer: int
    texture_map_buffer: int

    def __init__(self, vertex_buffer: int, texture_map_buffer: int) -> None:
        self.vertex_buffer = vertex_buffer
        self.texture_map_buffer = texture_map_buffer

    def bind(self, shader: Shader):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_buffer)
        loc = gl.glGetAttribLocation(shader.program_id, "position")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, 12, gl.ctypes.c_void_p(0))

        if shader.has_texture:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.texture_map_buffer)
            loc = gl.glGetAttribLocation(shader.program_id, "texture_coord")
            gl.glEnableVertexAttribArray(loc)
            gl.glVertexAttribPointer(
                loc, 2, gl.GL_FLOAT, False, 8, gl.ctypes.c_void_p(0)
            )

    @staticmethod
    def setup_buffers(models: Iterable[Model] = []) -> "Buffers":
        # Create buffer slot
        vertex_buffer, texture_map_buffer = cast(List[int], gl.glGenBuffers(2))

        # Bind the Vertex Array Object
        vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(vao)

        # Setup vertices
        vertices = np.ndarray([0, 3], dtype=np.float32)
        for model in models:
            model.offset = len(vertices)
            vertices = np.concatenate([vertices, model.vertices], dtype=np.float32)

        # Make this the current buffer and upload the data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW
        )

        # Setup texture mappings
        texture_coords = np.ndarray([0, 2], dtype=np.float32)
        for model in models:
            texture_coords = np.concatenate(
                [texture_coords, model.texture_coords], dtype=np.float32
            )

        # Make this the current buffer and upload the texture data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, texture_map_buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            texture_coords.nbytes,
            texture_coords,
            gl.GL_STATIC_DRAW,
        )

        return Buffers(vertex_buffer, texture_map_buffer)
