#
# Lelis - 12543822
# Atividade 1 - Transformações Geométricas 2D
#

from textwrap import dedent
import colorsys

import glfw
import numpy as np
import OpenGL.GL as gl


# Settings
STOP_ON_CURSOR = True

# Window


def init_window(
    title: str,
    width: int,
    height: int,
):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)

    win = glfw.create_window(width, height, title, None, None)
    glfw.make_context_current(win)

    glfw.swap_interval(1)

    return win


# Shaders

vertex_shader_source = dedent(
    """
    attribute vec2 position;
    uniform mat4 mat;
    void main() {
        gl_Position = mat * vec4(position, 0.0, 1.0);
    }
"""
)

fragment_shader_source = dedent(
    """
    uniform vec4 color;
    void main() {
        gl_FragColor = color;
    }
"""
)


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


class Entity:
    vertices: np.ndarray
    x: float
    y: float
    scale_x: float
    scale_y: float
    rotation: float  # in radians
    visible: bool  # Whether to draw the entity or not
    oob_loop: bool  # Whether to loop the entity when it goes out of bounds
    color: np.ndarray
    draw_mode: int

    def __init__(
        self,
        vertices: np.ndarray,
        x: float = 0,
        y: float = 0,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
        rotation: float = 0.0,
        visible: bool = True,
        oob_loop: bool = False,
        color: np.ndarray = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        draw_mode: int = gl.GL_TRIANGLES,
    ):
        self.vertices = vertices
        self.x = x
        self.y = y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.rotation = rotation
        self.visible = visible
        self.oob_loop = oob_loop
        self.color = color
        self.draw_mode = draw_mode

    def tranformation_matrix(self):
        cos = np.cos(self.rotation)
        sin = np.sin(self.rotation)
        rotation_matrix = np.array(
            [
                [
                    cos,
                    -sin,
                    0,
                    0,
                ],
                [
                    sin,
                    cos,
                    0,
                    0,
                ],
                [
                    0,
                    0,
                    1,
                    0,
                ],
                [
                    0,
                    0,
                    0,
                    1,
                ],
            ],
            np.float32,
        )

        scale_matrix = np.array(
            [
                [self.scale_x, 0, 0, 0],
                [0, self.scale_y, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            np.float32,
        )

        translation_matrix = np.array(
            [
                [1, 0, 0, self.x],
                [0, 1, 0, self.y],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            np.float32,
        )

        return (translation_matrix @ rotation_matrix @ scale_matrix).reshape(-1)

    def update(self, dt):
        # By default, do nothing
        pass

    def draw(self, program, vertex_offset=0):
        if not self.visible:
            return

        # Get the location of the color
        loc = gl.glGetUniformLocation(program, "color")
        # Upload the color
        gl.glUniform4fv(loc, 1, self.color)

        # Get the location of the matrix
        loc = gl.glGetUniformLocation(program, "mat")
        # Get the transformation matrix
        mat = self.tranformation_matrix()
        # Upload the matrix
        gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, mat)
        # Draw the element
        vertex_count = self.vertex_count()
        gl.glDrawArrays(self.draw_mode, vertex_offset, vertex_count)

        if self.oob_loop:
            old_x = self.x
            old_y = self.y

            # Render four times, with the entity in the four corners
            self.oob_loop = False

            self.x = old_x + 2
            self.draw(program, vertex_offset)

            self.x = old_x - 2
            self.draw(program, vertex_offset)

            self.x = old_x

            self.y = old_y + 2
            self.draw(program, vertex_offset)

            self.y = old_y - 2
            self.draw(program, vertex_offset)

            self.y = old_y

            self.oob_loop = True

        return len(self.vertices)

    def vertex_count(self):
        return len(self.vertices) // 2


class Ship(Entity):
    MIN_SCALE = 0.01
    MAX_SCALE = 1.5
    MAX_SPEED = 2.0
    MIN_SPEED = 0.0
    INITIAL_SCALE = 0.2
    ACCELERATING_RATE = 0.4

    acceleration: float  # Units per second
    accelerating: int

    def __init__(self, acceleration: float = 0.0, **kwargs):
        # Initialize super class
        super().__init__(
            np.array(
                [
                    0.0,
                    0.5,
                    -0.5,
                    -0.5,
                    0.5,
                    -0.5,
                ],
                dtype=np.float32,
            ),
            scale_x=self.INITIAL_SCALE,
            scale_y=self.INITIAL_SCALE,
            oob_loop=True,
            **kwargs,
        )

        self.acceleration = acceleration
        self.accelerating = 0
        self.mouse_x = 0.0
        self.mouse_y = 0.0

    def update(self, dt):
        # Handle continuous acceleration
        if self.accelerating != 0:
            self.acceleration += (
                self.ACCELERATING_RATE * dt * np.sign(self.accelerating)
            )
            self.acceleration = np.clip(
                self.acceleration, self.MIN_SPEED, self.MAX_SPEED
            )

        # Compute the difference between the mouse and the ship
        dx = self.mouse_x - self.x
        dy = self.mouse_y - self.y

        if STOP_ON_CURSOR:
            # If the mouse is too close to the center, do nothing
            if abs(dx) <= 0.01 and abs(dy) <= 0.01:
                return

        # Compute the angle of the ship based on the mouse position
        # Subtracting pi/2 to make the ship point upwards
        angle = np.arctan2(dy, dx) - np.pi / 2

        # Normalize the angle
        if angle < 0:
            angle += 2 * np.pi

        self.rotation = angle

        # Update position according to the angle and acceleration
        sin = np.sin(self.rotation)
        cos = np.cos(self.rotation)

        self.x += self.acceleration * -sin * dt
        self.y += self.acceleration * cos * dt

        # Wrap around on overflow
        if self.x > 1:
            self.x -= 2
        if self.x < -1:
            self.x += 2
        if self.y > 1:
            self.y -= 2
        if self.y < -1:
            self.y += 2

    def update_scale(self, increase: bool, factor: float = 1.1):
        # Exponential scaling
        if increase:
            self.scale_x *= factor
            self.scale_y *= factor
        else:
            self.scale_x /= factor
            self.scale_y /= factor

        # Clamp the scale
        self.scale_x = np.clip(self.scale_x, self.MIN_SCALE, self.MAX_SCALE)
        self.scale_y = np.clip(self.scale_y, self.MIN_SCALE, self.MAX_SCALE)

    def reset(self):
        self.x = 0
        self.y = 0
        self.scale_x = self.INITIAL_SCALE
        self.scale_y = self.INITIAL_SCALE
        self.rotation = 0.0
        self.acceleration = 0.0


class Asteroid(Entity):
    acc_x: float
    acc_y: float

    @staticmethod
    def make_random():
        color = colorsys.hls_to_rgb(
            np.random.uniform(0, 1),
            np.random.uniform(0.7, 0.8),
            np.random.uniform(0.8, 0.9),
        )
        color = np.array(color, dtype=np.float32)
        color = np.concatenate([color, [1.0]])

        scale = np.random.uniform(0.05, 0.15)

        return Asteroid(
            acc_y=np.random.uniform(-0.2, 0.2),
            acc_x=np.random.uniform(-0.2, 0.2),
            rotation=np.random.uniform(0, 2 * np.pi),
            scale_x=scale,
            scale_y=scale,
            x=np.random.uniform(-1, 1),
            y=np.random.uniform(-1, 1),
            color=color,
            draw_mode=gl.GL_TRIANGLE_STRIP,
        )

    def __init__(
        self,
        vertices: np.ndarray = None,
        acc_x: float = 0.0,
        acc_y: float = 0.0,
        **kwargs,
    ):
        if vertices is None:
            vertices = np.array(
                [
                    0.0,
                    0.5,
                    -0.5,
                    -0.5,
                    0.5,
                    -0.5,
                ],
                dtype=np.float32,
            )

        super().__init__(vertices, oob_loop=True, **kwargs)

        # Random initial acceleration
        self.acc_x = acc_x
        self.acc_y = acc_y

    def update(self, dt):
        self.x += self.acc_x * dt
        self.y += self.acc_y * dt

        # Wrap around on overflow
        if self.x > 1:
            self.x -= 2
        if self.x < -1:
            self.x += 2
        if self.y > 1:
            self.y -= 2
        if self.y < -1:
            self.y += 2


ship = Ship()
asteroids = [Asteroid.make_random() for _ in range(np.random.randint(8, 16))]

entities = [
    *asteroids,
    ship,
]


def setup_buffers(program):
    # Create buffer slot
    buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    flat_vertices = np.concatenate([entity.vertices for entity in entities])

    # Upload data
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER, flat_vertices.nbytes, flat_vertices, gl.GL_STATIC_DRAW
    )

    # Make this the default buffer
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    # Bind the position attribute
    stride = flat_vertices.strides[0]
    offset = gl.ctypes.c_void_p(0)
    loc = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)


def setup_events(win):
    def key_handler(win, key, scancode, action, mods):
        global entities

        # Exit handler (ESC)
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, True)

        # Scale Down handler (Minus/Underscore)
        if key == glfw.KEY_MINUS and action == glfw.PRESS:
            ship.update_scale(False)

        # Scale Up handler (Equal/Plus)
        if key == glfw.KEY_EQUAL and action == glfw.PRESS:
            ship.update_scale(True)

        # Accelerate on W or Up
        if (key == glfw.KEY_W or key == glfw.KEY_UP) and action == glfw.PRESS:
            ship.acceleration += 0.1
            ship.accelerating += 1

        if (key == glfw.KEY_W or key == glfw.KEY_UP) and action == glfw.RELEASE:
            ship.accelerating -= 1

        # Decelerate on S or Down
        if (key == glfw.KEY_S or key == glfw.KEY_DOWN) and (action == glfw.PRESS):
            ship.acceleration -= 0.1
            ship.accelerating -= 1

        if (key == glfw.KEY_S or key == glfw.KEY_DOWN) and action == glfw.RELEASE:
            ship.accelerating += 1

        # Reset handler (R)
        if key == glfw.KEY_R and action == glfw.PRESS:
            ship.reset()

    def cursor_handler(win, x, y):
        # Compute the normalized coordinates of the cursor
        vp_x, vp_y = glfw.get_window_size(win)
        rel_x = (x / vp_x) * 2 - 1
        rel_y = -((y / vp_y) * 2 - 1)

        # Update the rotation of the ship
        ship.mouse_x = rel_x
        ship.mouse_y = rel_y

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
