import numpy as np
import OpenGL.GL as gl

class Entity:
    vertices: np.ndarray
    x: float
    y: float
    scale_x: float
    scale_y: float
    rotation: float # in radians

    visible: bool # Whether to draw the entity or not
    oob_loop: bool # Whether to loop the entity when it goes out of bounds
    color: np.ndarray
    draw_mode: int

    def __init__(self,
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
        rotation_matrix = np.array([
            [cos, -sin, 0, 0,],
            [sin, cos, 0, 0,],
            [0, 0, 1, 0,],
            [0, 0, 0, 1,],
        ], np.float32)

        scale_matrix = np.array([
            [self.scale_x, 0, 0, 0],
            [0, self.scale_y, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], np.float32)

        translation_matrix = np.array([
            [1, 0, 0, self.x],
            [0, 1, 0, self.y],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], np.float32)

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