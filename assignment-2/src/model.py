# CG 2024.1 - Assignment 2
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

from typing import Any, Dict, Iterable, List, cast, Optional

import numpy as np
import OpenGL.GL as gl

from shader import Shader
from material import Material
from wavefront import load_obj


class Model:
    vertices: np.ndarray
    texture_coords: np.ndarray
    normals: np.ndarray
    materials: Dict[Any, Material]
    material_swaps: Dict[int, Any]
    draw_mode: int
    ka_override: Optional[float]
    kd_override: Optional[float]
    ks_override: Optional[float]
    ns_override: Optional[float]

    offset: int
    texture_offset: int

    def __init__(
        self,
        vertices: np.ndarray,
        texture_coords: np.ndarray,
        normals: np.ndarray,
        materials: Dict[str, Material],
        material_swaps: Dict[int, str] = {0: "default"},
        draw_mode=gl.GL_TRIANGLES,
        ka_override: Optional[float] = None,
        kd_override: Optional[float] = None,
        ks_override: Optional[float] = None,
        ns_override: Optional[float] = None,
    ):
        assert len(vertices) == len(
            texture_coords
        ), "Vertices and texture coordinates must have the same length"
        assert len(vertices) == len(
            normals
        ), "Vertices and normals must have the same length"
        assert (
            len(material_swaps) == 0 or min(material_swaps.keys()) >= 0
        ), "Material swaps must have non-negative keys"
        assert len(material_swaps) == 0 or max(material_swaps.keys()) < len(
            vertices
        ), "Material swaps must have keys less than the number of vertices"

        for material in material_swaps.values():
            if material not in materials:
                print(material)

        assert all(
            [material in materials for material in material_swaps.values()]
        ), "Material swaps must have valid materials"

        self.vertices = vertices.astype(np.float32)
        self.normals = normals.astype(np.float32)
        self.texture_coords = texture_coords.astype(np.float32)
        self.materials = materials
        self.material_swaps = material_swaps
        self.draw_mode = draw_mode
        self.offset = 0
        self.texture_offset = 0
        self.ka_override = ka_override
        self.kd_override = kd_override
        self.ks_override = ks_override
        self.ns_override = ns_override

    @classmethod
    def load_obj(
        cls,
        filepath: str,
        materials: Dict[str, Material],
        prefix_materials: str = "",
        prefix_models: str = "",
        split_objects=False,
    ) -> Dict[str, "Model"]:
        models = load_obj(filepath, split_objects)
        result = {}
        for model in models:
            texture_coords = []
            vertices = []
            normals = []

            material_swaps = {}
            last_material = None

            for i, face in enumerate(model["faces"]):
                cur_material = prefix_materials + face[3]
                if last_material != cur_material:
                    material_swaps[i * 3] = cur_material
                    last_material = cur_material
                for vertex in face[0]:
                    vertices.append(model["vertices"][vertex - 1])
                for texture in face[1]:
                    texture_coords.append(model["texture"][texture - 1])
                for normal in face[2]:
                    normals.append(model["normals"][normal - 1])

            vertices = np.array(vertices, dtype=np.float32)
            texture_coords = np.array(texture_coords, dtype=np.float32)
            normals = np.array(normals, dtype=np.float32)
            if split_objects:
                result[prefix_models + model["name"]] = Model(
                    vertices, texture_coords, normals, materials, material_swaps
                )
            else:
                result[prefix_models] = Model(
                    vertices, texture_coords, normals, materials, material_swaps
                )

        return result


class Buffers:
    vertex_buffer: int
    texture_map_buffer: int
    normal_buffer: int

    def __init__(
        self, vertex_buffer: int, texture_map_buffer: int, normal_buffer: int
    ) -> None:
        self.vertex_buffer = vertex_buffer
        self.texture_map_buffer = texture_map_buffer
        self.normal_buffer = normal_buffer

    def bind(self, shader: Shader):
        """Associates a model with a shader"""
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

        try:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.normal_buffer)
            loc = gl.glGetAttribLocation(shader.program_id, "normal")
            gl.glEnableVertexAttribArray(loc)
            gl.glVertexAttribPointer(
                loc, 3, gl.GL_FLOAT, False, 12, gl.ctypes.c_void_p(0)
            )
        except Exception as e:
            print(e)

    @staticmethod
    def setup_buffers(models: Iterable[Model] = []) -> "Buffers":
        """Sets up the buffers"""
        # Create buffer slot
        vertex_buffer, texture_map_buffer, normal_buffer = cast(
            List[int], gl.glGenBuffers(3)
        )

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

        # Setup normals
        normals = np.ndarray([0, 3], dtype=np.float32)
        for model in models:
            model.offset = len(normals)
            normals = np.concatenate([normals, model.normals], dtype=np.float32)

        # Make this the current buffer and upload the data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, normal_buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, normals.nbytes, normals, gl.GL_STATIC_DRAW)

        return Buffers(vertex_buffer, texture_map_buffer, normal_buffer)
