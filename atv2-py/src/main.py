import os
from typing import Any, Callable, List, Dict, Tuple, cast, Optional

import glfw
import glm
import numpy as np
import OpenGL.GL as gl
from PIL import Image

from camera import Camera
from renderer import Renderer
from entity import Material, Model, Entity, Shader


def local_relative_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


VERTEX_SHADER_FILE = local_relative_path("../shaders/main.vert")
FRAGMENT_SHADER_FILE = local_relative_path("../shaders/main.frag")

OTHER_VERTEX_SHADER_FILE = local_relative_path("../shaders/alt.vert")
OTHER_FRAGMENT_SHADER_FILE = local_relative_path("../shaders/alt.frag")

# TODO: support mtl :)


def init_window(
    title: str,
    width: int,
    height: int,
    resizable=False,
):
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE if resizable else glfw.FALSE)
    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)

    win = glfw.create_window(width, height, title, None, None)
    glfw.make_context_current(win)

    glfw.swap_interval(1)

    glfw.set_input_mode(win, glfw.STICKY_KEYS, glfw.TRUE)
    glfw.set_input_mode(win, glfw.CURSOR, glfw.CURSOR_DISABLED)
    if glfw.raw_mouse_motion_supported():
        glfw.set_input_mode(win, glfw.RAW_MOUSE_MOTION, glfw.TRUE)

    return win


def setup_shader(vertex_shader_source: str, fragment_shader_source: str) -> Shader:
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


def setup_buffers(models: list[Model] = []) -> Tuple[int, int]:
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
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

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

    return vertex_buffer, texture_map_buffer


def bind_buffers(
    program_id: int,
    vertex_buffer: int,
    texture_map_buffer: Optional[int],
):
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
    loc = gl.glGetAttribLocation(program_id, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, 12, gl.ctypes.c_void_p(0))

    if texture_map_buffer is not None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, texture_map_buffer)
        loc = gl.glGetAttribLocation(program_id, "texture_coord")
        gl.glEnableVertexAttribArray(loc)
        gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, 8, gl.ctypes.c_void_p(0))


def setup_events(
    win,
    entities: list[Entity] = [],
    key_handlers: List[Callable[[Any, int, int, int, int], None]] = [],
    cursor_handlers: List[Callable[[Any, float, float, float, float], None]] = [],
):
    # Local copy of the handlers
    local_key_handlers = [*key_handlers]
    local_cursor_handlers = [*cursor_handlers]

    # Add the handlers from the entities
    for entity in entities:
        key_callback = entity.key_handler()
        if key_callback is not None:
            local_key_handlers.append(key_callback)

        cursor_callback = entity.cursor_handler()
        if cursor_callback is not None:
            local_cursor_handlers.append(cursor_callback)

    # Add the handlers to the window
    def key_handler(win, key, scancode, action, mods):
        for handler in local_key_handlers:
            handler(win, key, scancode, action, mods)

    def cursor_handler(win, x, y):
        # Compute the normalized coordinates of the cursor
        vp_x, vp_y = glfw.get_window_size(win)
        rel_x = (x / vp_x) * 2 - 1
        rel_y = -((y / vp_y) * 2 - 1)

        for handler in local_cursor_handlers:
            handler(win, x, y, rel_x, rel_y)

    glfw.set_key_callback(win, key_handler)
    glfw.set_cursor_pos_callback(win, cursor_handler)


def setup_textures(materials: List[Material]):
    for material in materials:
        # Skip if there is no texture
        if material.texture_path is None:
            continue

        # Create the texture
        texture = gl.glGenTextures(1)
        material.texture_id = texture

        # Load the image
        img = Image.open(material.texture_path)
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


def closer_handler(win, key, scancode, action, mods):
    # Exit handler (ESC)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, True)


def main():
    # TODO: move this
    camera = Camera()
    camera.position = glm.vec3(10, 1, 0)

    # TODO: move this to renderer
    polygon_mode = False

    def polygon_handler(win, key, scancode, action, mods):
        nonlocal polygon_mode

        if key == glfw.KEY_P and action == glfw.PRESS:
            polygon_mode = not polygon_mode

    # Configure window
    win = init_window("Eldrich Horrors Beyond Your Comprehension :D", 1280, 720)

    # Load shaders
    with open(VERTEX_SHADER_FILE) as vertex_file:
        vertex_shader_source = vertex_file.read()

    with open(FRAGMENT_SHADER_FILE) as fragment_file:
        fragment_shader_source = fragment_file.read()

    with open(OTHER_VERTEX_SHADER_FILE) as vertex_file:
        other_vertex_shader_source = vertex_file.read()

    with open(OTHER_FRAGMENT_SHADER_FILE) as fragment_file:
        other_fragment_shader_source = fragment_file.read()

    main_shader = setup_shader(vertex_shader_source, fragment_shader_source)
    alt_shader = setup_shader(other_vertex_shader_source, other_fragment_shader_source)

    # Load all materials
    materials: Dict[str, Material] = {
        "box-Material.002": Material.from_texture(
            main_shader, local_relative_path("../../examples/caixa/caixa.jpg")
        ),
        "box-Material.003": Material(
            alt_shader,
        ),
        "monster-default": Material.from_texture(
            main_shader,
            local_relative_path("../../examples/monstro/monstro.jpg"),
        ),
    }

    # Load all models
    models: Dict[str, Model] = {
        "box": Model.load_obj(
            local_relative_path("../../examples/caixa/caixa.obj"),
            materials,
            "box-",
        ),
        "monster": Model.load_obj(
            local_relative_path("../../examples/monstro/monstro.obj"),
            materials,
            "monster-",
        ),
    }

    # Load all textures
    entities: List[Entity] = [
        Entity(models["box"]),
        Entity(models["monster"], position=glm.vec3(0, 0, 4)),
    ]

    # Load buffers
    vertex_buffer, texture_map_buffer = setup_buffers(list(models.values()))
    bind_buffers(main_shader.program_id, vertex_buffer, texture_map_buffer)
    bind_buffers(alt_shader.program_id, vertex_buffer, None)

    # Load textures
    setup_textures(list(materials.values()))

    # Setup events
    setup_events(
        win,
        key_handlers=[closer_handler, polygon_handler, camera.key_handler],
        cursor_handlers=[camera.cursor_handler],
    )

    # Show window
    glfw.show_window(win)

    # Key variables

    renderer = Renderer()

    # Main loop
    gl.glEnable(gl.GL_DEPTH_TEST)
    last_render = glfw.get_time()
    while not glfw.window_should_close(win):
        # Keep track of elapsed time
        current_time = glfw.get_time()
        delta_time = current_time - last_render
        # Get the events
        glfw.poll_events()

        # Clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(0, 0, 0, 1.0)

        if polygon_mode:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        # Update elements
        for entity in entities:
            entity.update(delta_time)

        # Update the camera
        camera.update(win, main_shader, delta_time)

        # Render elements
        for entity in entities:
            renderer.render(entity, camera)

        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()


if __name__ == "__main__":
    main()
