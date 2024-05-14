from typing import Any, cast

import OpenGL.GL as gl


class Shader:
    program_id: int
    model_loc: Any
    view_loc: Any
    projection_loc: Any
    color_loc: Any
    texture_filter_loc: Any
    has_texture: bool

    def __init__(
        self,
        program_id: int,
        has_texture: bool = True,
    ) -> None:
        self.program_id = program_id
        self.model_loc = gl.glGetUniformLocation(program_id, "model")
        self.view_loc = gl.glGetUniformLocation(program_id, "view")
        self.projection_loc = gl.glGetUniformLocation(program_id, "projection")
        self.color_loc = gl.glGetUniformLocation(program_id, "u_color")
        self.texture_filter_loc = gl.glGetUniformLocation(
            program_id, "u_texture_filter"
        )
        self.has_texture = has_texture

    def use(self):
        gl.glUseProgram(self.program_id)

    @staticmethod
    def load_from_files(vertex_file: str, fragment_file: str) -> "Shader":
        """Loads a shader from a .vert and .frag file"""
        with open(vertex_file, "r") as f:
            vertex_shader = f.read()
        with open(fragment_file, "r") as f:
            fragment_shader = f.read()
        return Shader.compile(vertex_shader, fragment_shader)

    @staticmethod
    def compile(vertex_shader_source: str, fragment_shader_source: str) -> "Shader":
        program_id = cast(int, gl.glCreateProgram())

        # Build and compile vertex shader
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_shader_source)
        gl.glCompileShader(vertex_shader)
        if not gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS):
            err = gl.glGetShaderInfoLog(vertex_shader)
            raise RuntimeError(f"Vertex shader compilation error: {err}")

        # Build and compile fragment shader
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_shader_source)
        gl.glCompileShader(fragment_shader)
        if not gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS):
            err = gl.glGetShaderInfoLog(fragment_shader)
            raise RuntimeError(f"Fragment shader compilation error: {err}")

        # Link shaders
        gl.glAttachShader(program_id, vertex_shader)
        gl.glAttachShader(program_id, fragment_shader)

        gl.glLinkProgram(program_id)
        if not gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS):
            err = gl.glGetProgramInfoLog(program_id)
            raise RuntimeError(f"Program linking error: {err}")

        # Delete shaders
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        # Return program
        return Shader(program_id)
