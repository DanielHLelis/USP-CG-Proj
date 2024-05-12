from typing import Optional, Callable, List

import glfw
import numpy as np
import OpenGL.GL as gl
from PIL import Image


from entity import Entity


VERTEX_SHADER_FILE = './shaders/vertex.vert'
FRAGMENT_SHADER_FILE = './shaders/fragment.frag'


def init_window(
        title: str,
        width: int,
        height: int,
):
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)

    win = glfw.create_window(width, height, title, None, None)
    glfw.make_context_current(win)

    glfw.swap_interval(1)

    return win


# Shaders
with open(VERTEX_SHADER_FILE) as vertex_file:
    vertex_shader_source = vertex_file.read()

with open(FRAGMENT_SHADER_FILE) as fragment_file:
    fragment_shader_source = fragment_file.read()


def setup_shaders():
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


cubo = [
    # Face 1 do Cubo (vértices do quadrado)
    (-0.2, -0.2, +0.2),
    (+0.2, -0.2, +0.2),
    (-0.2, +0.2, +0.2),
    (+0.2, +0.2, +0.2),

    # Face 2 do Cubo
    (+0.2, -0.2, +0.2),
    (+0.2, -0.2, -0.2),         
    (+0.2, +0.2, +0.2),
    (+0.2, +0.2, -0.2),
    
    # Face 3 do Cubo
    (+0.2, -0.2, -0.2),
    (-0.2, -0.2, -0.2),            
    (+0.2, +0.2, -0.2),
    (-0.2, +0.2, -0.2),

    # Face 4 do Cubo
    (-0.2, -0.2, -0.2),
    (-0.2, -0.2, +0.2),         
    (-0.2, +0.2, -0.2),
    (-0.2, +0.2, +0.2),

    # Face 5 do Cubo
    (-0.2, -0.2, -0.2),
    (+0.2, -0.2, -0.2),         
    (-0.2, -0.2, +0.2),
    (+0.2, -0.2, +0.2),
    
    # Face 6 do Cubo
    (-0.2, +0.2, +0.2),
    (+0.2, +0.2, +0.2),           
    (-0.2, +0.2, -0.2),
    (+0.2, +0.2, -0.2)
]

def setup_buffers(program, entities: list[Entity] = []):
    # Create buffer slot
    buffer = gl.glGenBuffers(2)
    vao = gl.glGenVertexArrays(1)

    # Setup vertices
    # flat_vertices = np.concatenate([entity.vertices for entity in entities]) if len(entities) != 0 else np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
    flat_vertices = np.array(cubo, dtype=np.float32)

    # Make this the current buffer and upload the data
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer[0])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, flat_vertices.nbytes, flat_vertices, gl.GL_DYNAMIC_DRAW)

    # Bind the Vertex Array Object
    gl.glBindVertexArray(vao)

    # Bind the position attribute
    stride = flat_vertices.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

    # Setup texture mappings
    # flat_texture_mappings = np.concatenate([entity.texture_mappings for entity in entities]) if len(entities) != 0 else np.array([[0.0, 0.0]], dtype=np.float32)
    flat_texture_mappings = np.array([1.0, 1.0] * len(cubo), dtype=np.float32)

    # Make this the current buffer and upload the data
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer[1])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, flat_texture_mappings.nbytes, flat_texture_mappings, gl.GL_DYNAMIC_DRAW)

    # Bind the position attribute
    stride = flat_texture_mappings.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "texture_coord")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)


def setup_events(win, 
                 entities: list[Entity] = [], 
                 key_handlers: List[Callable[[any, int, int, int, int], None]] = [],
                 cursor_handlers: List[Callable[[any, float, float, float, float], None]] = []):
    # Local copy of the handlers
    local_key_handlers = [*key_handlers]
    local_cursor_handlers = [*cursor_handlers]

    # Add the handlers from the entities
    for entity in entities:
        key_handler = entity.key_handler()
        if key_handler is not None:
            local_key_handlers.append(key_handler)

        cursor_handler = entity.cursor_handler()
        if cursor_handler is not None:
            local_cursor_handlers.append(cursor_handler)

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


def setup_textures(program):
    # Load texture
    textures = gl.glGenTextures(2)

    # Set the texture wrapping parameters
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

    # Set the texture filtering parameters
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    # Load the image
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    img = Image.open("textures/test.jpg")
    img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0,
        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data
    )

    return textures


def closer_handler(win, key, scancode, action, mods):
    # Exit handler (ESC)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, True)


def main():
    # Configure window
    win = init_window("Hello, Triangle!", 800, 800)
    # Load shaders
    program = setup_shaders()
    # Load buffers
    setup_buffers(program)
    # Setup events
    setup_events(win, key_handlers=[closer_handler])
    # Load textures
    setup_textures(program)

    # Show window
    glfw.show_window(win)

    # Key variables
    color_loc = gl.glGetUniformLocation(program, "color")
    model_loc = gl.glGetUniformLocation(program, "model")
    view_loc = gl.glGetUniformLocation(program, "view")
    projection_loc = gl.glGetUniformLocation(program, "projection")

    # Main loop
    last_render = glfw.get_time()
    while not glfw.window_should_close(win):
        # Keep track of elapsed time
        current_time = glfw.get_time()
        delta_time = current_time - last_render
        # Get the events
        glfw.poll_events()

        # Clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(0, 0, 0.5, 1.0)

        # Update elements
        # for entity in entities:
        #     entity.update()

        # Render elements
        offset = 0
        # for entity in entities:
        #     offset += entity.draw(program, offset)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)


        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()

if __name__ == "__main__":
    main()
