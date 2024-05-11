import glfw
import numpy as np
import OpenGL.GL as gl


from entity import Entity


VERTEX_SHADER_FILE = '../shaders/vertex.vert'
FRAGMENT_SHADER_FILE = '../shaders/fragment.frag'


def init_window(
        title: str,
        width: int,
        height: int,
):
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
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


def setup_buffers(program, entities: list[Entity]):
    # Create buffer slot
    buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    flat_vertices = np.concatenate([entity.vertices for entity in entities])


    # Upload data
    gl.glBufferData(gl.GL_ARRAY_BUFFER, flat_vertices.nbytes, flat_vertices, gl.GL_STATIC_DRAW)

    # Make this the default buffer
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    # Bind the position attribute
    stride = flat_vertices.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)


def setup_events(win):
    def key_handler(win, key, scancode, action, mods):
        global entities

        # Exit handler (ESC)
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, True)

        # Scale Down handler (Minus/Underscore)
        if key == glfw.KEY_MINUS and action == glfw.PRESS:
            # ship.update_scale(False)
            pass

        # Scale Up handler (Equal/Plus)
        if key == glfw.KEY_EQUAL and action == glfw.PRESS:
            # ship.update_scale(True)
            pass

        # Accelerate on W or Up
        if (key == glfw.KEY_W or key == glfw.KEY_UP) and action == glfw.PRESS:
            # ship.acceleration += 0.1
            # ship.accelerating += 1
            pass

        if (key == glfw.KEY_W or key == glfw.KEY_UP) and action == glfw.RELEASE:
            # ship.accelerating -= 1
            pass

        # Decelerate on S or Down
        if (key == glfw.KEY_S or key == glfw.KEY_DOWN) and (action == glfw.PRESS):
            # ship.acceleration -= 0.1
            # ship.accelerating -= 1
            pass

        if (key == glfw.KEY_S or key == glfw.KEY_DOWN) and action == glfw.RELEASE:
            # ship.accelerating += 1
            pass

        # Reset handler (R)
        if key == glfw.KEY_R and action == glfw.PRESS:
            # ship.reset()
            pass

    def cursor_handler(win, x, y):
        # Compute the normalized coordinates of the cursor
        vp_x, vp_y = glfw.get_window_size(win)
        rel_x = (x / vp_x) * 2 - 1
        rel_y = -((y / vp_y) * 2 - 1)

        # Update the rotation of the ship
        # ship.mouse_x = rel_x
        # ship.mouse_y = rel_y


    glfw.set_key_callback(win, key_handler)
    glfw.set_cursor_pos_callback(win, cursor_handler)


def main():
    # Configure window
    win = init_window("Hello, Triangle!", 800, 800)
    # Load shaders
    program = setup_shaders()
    # Load buffers
    setup_buffers(program)
    # Setup events
    setup_events(win)

    # Show window
    glfw.show_window(win)

    # Main loop
    last_render = glfw.get_time()
    while not glfw.window_should_close(win):
        # Keep track of elapsed time
        current_time = glfw.get_time()
        # Get the events
        glfw.poll_events()

        # Clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(0, 0, 0, 1.0)

        # Update elements
        for entity in entities:
            entity.update(current_time - last_render)

        # Render elements
        offset = 0
        for entity in entities:
            offset += entity.draw(program, offset)

        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()

if __name__ == "__main__":
    main()
