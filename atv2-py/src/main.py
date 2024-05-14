import os
from typing import List, Dict

import glfw
import glm

from camera import Camera
from renderer import Renderer
from window import init_window, setup_events, closer_handler
from material import Material
from shader import Shader
from model import Buffers, Model
from entity import Entity
from entity.skybox import Skybox


def local_relative_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


VERTEX_SHADER_FILE = local_relative_path("../shaders/main.vert")
FRAGMENT_SHADER_FILE = local_relative_path("../shaders/main.frag")

OTHER_VERTEX_SHADER_FILE = local_relative_path("../shaders/alt.vert")
OTHER_FRAGMENT_SHADER_FILE = local_relative_path("../shaders/alt.frag")


def main():
    # Create the renderer
    renderer = Renderer()

    # Create the camera
    camera = Camera()
    camera.position = glm.vec3(10, 1, 0)

    # Configure window
    win = init_window("Eldrich Horrors Beyond Your Comprehension :D", 1280, 720)

    # Load and compile shaders
    main_shader = Shader.load_from_files(VERTEX_SHADER_FILE, FRAGMENT_SHADER_FILE)
    alt_shader = Shader.load_from_files(
        OTHER_VERTEX_SHADER_FILE, OTHER_FRAGMENT_SHADER_FILE
    )
    alt_shader.has_texture = False

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
        "skybox": Material.from_texture(
            main_shader,
            local_relative_path("../textures/skybox.jpg"),
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
        "skybox": Model.load_obj(
            local_relative_path("../models/skybox.obj"),
            materials,
            "",
        ),
    }

    # Load all textures
    entities: List[Entity] = [
        Entity(models["box"]),
        Entity(models["monster"], position=glm.vec3(0, 0, 4)),
        Skybox(models["skybox"]),
    ]

    # Load buffers
    buffers = Buffers.setup_buffers(models.values())
    buffers.bind(main_shader)
    buffers.bind(alt_shader)

    # Load textures
    Material.setup_all(materials.values())

    # Setup events
    setup_events(
        win,
        key_handlers=[closer_handler, renderer.key_handler, camera.key_handler],
        cursor_handlers=[camera.cursor_handler],
    )

    # Show window
    glfw.show_window(win)

    # Main loop
    renderer.init()
    last_render = glfw.get_time()
    while not glfw.window_should_close(win):
        # Keep track of elapsed time
        current_time = glfw.get_time()
        delta_time = current_time - last_render
        # Get the events
        glfw.poll_events()

        # Update the camera
        camera.update(win, main_shader, delta_time)

        # Update elements
        for entity in entities:
            entity.update(delta_time, camera)

        # Clear the screen
        renderer.pre_render()

        # Render elements
        for entity in entities:
            renderer.draw_entity(entity, camera)

        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()


if __name__ == "__main__":
    main()
