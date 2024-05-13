import os
from typing import Any, Callable, List

import glfw
import glm
import numpy as np
import OpenGL.GL as gl
from PIL import Image

from camera import Camera
from renderer import Renderer
from entity import Model, Entity


def local_relative_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


VERTEX_SHADER_FILE = local_relative_path("../shaders/vertex.vert")
FRAGMENT_SHADER_FILE = local_relative_path("../shaders/fragment.frag")

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


def setup_shaders():
    with open(VERTEX_SHADER_FILE) as vertex_file:
        vertex_shader_source = vertex_file.read()

    with open(FRAGMENT_SHADER_FILE) as fragment_file:
        fragment_shader_source = fragment_file.read()

    program = gl.glCreateProgram()

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
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)

    gl.glLinkProgram(program)
    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        err = gl.glGetProgramInfoLog(program)
        raise RuntimeError(f"Program linking error: {err}")

    # Delete shaders
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    # Return program
    gl.glUseProgram(program)

    return program


def setup_buffers(program, models: list[Model] = []):
    # Create buffer slot
    buffer = gl.glGenBuffers(2)

    # Bind the Vertex Array Object
    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    # Setup vertices
    vertices = np.ndarray([0, 3], dtype=np.float32)
    for model in models:
        model.offset = len(vertices)
        vertices = np.concatenate([vertices, model.vertices], dtype=np.float32)

    # Make this the current buffer and upload the data
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer[0])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

    # Bind the position attribute
    stride = vertices.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

    # Setup texture mappings
    texture_coords = np.ndarray([0, 2], dtype=np.float32)
    for model in models:
        texture_coords = np.concatenate(
            [texture_coords, model.texture_coords], dtype=np.float32
        )

    # Make this the current buffer and upload the data
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer[1])
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER,
        texture_coords.nbytes,
        texture_coords,
        gl.GL_STATIC_DRAW,
    )

    # Bind the position attribute
    stride = texture_coords.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "texture_coord")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)


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


def setup_textures(program, texture_files):
    # Load texture
    textures = gl.glGenTextures(len(texture_files))

    for i, texture_file in enumerate(texture_files):
        # Load the image
        img = Image.open(texture_file)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

        # Select the texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, i)

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

    return textures


def closer_handler(win, key, scancode, action, mods):
    # Exit handler (ESC)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, True)


def main():
    models: List[Model] = []
    textures: List[str] = []
    entities: List[Entity] = []

    box_texture = local_relative_path("../../examples/caixa/caixa.jpg")
    box_model = Model.load_obj(local_relative_path("../../examples/caixa/caixa.obj"), 0)

    models.append(box_model)
    textures.append(box_texture)
    entities.append(Entity(box_model))

    monster_model = Model.load_obj(
        local_relative_path("../../examples/monstro/monstro.obj"), 1
    )
    monster_texture = local_relative_path("../../examples/monstro/monstro.jpg")

    models.append(monster_model)
    textures.append(monster_texture)
    entities.append(Entity(monster_model, position=glm.vec3(0, 0, 4)))

    # TODO: move this
    camera = Camera()
    camera.position = glm.vec3(10, 1, 0)

    polygon_mode = False

    def polygon_handler(win, key, scancode, action, mods):
        nonlocal polygon_mode

        if key == glfw.KEY_P and action == glfw.PRESS:
            polygon_mode = not polygon_mode

    # Configure window
    win = init_window("Eldrich Horrors Beyond Your Comprehension :D", 1280, 720)
    # Load shaders
    program = setup_shaders()
    # Load buffers
    setup_buffers(program, models)
    # Setup events
    setup_events(
        win,
        key_handlers=[closer_handler, polygon_handler, camera.key_handler],
        cursor_handlers=[camera.cursor_handler],
    )
    # Load textures
    setup_textures(program, textures)

    # Show window
    glfw.show_window(win)

    # Key variables
    model_loc = gl.glGetUniformLocation(program, "model")
    view_loc = gl.glGetUniformLocation(program, "view")
    projection_loc = gl.glGetUniformLocation(program, "projection")

    renderer = Renderer(program, model_loc, view_loc, projection_loc)

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
        camera.update(win, program, delta_time)

        renderer.setup_camera(camera)
        # Render elements
        for entity in entities:
            renderer.render(entity)

        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()


if __name__ == "__main__":
    main()
