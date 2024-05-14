import os
from typing import Any, Dict

import glfw
import glm

from camera import Camera
from renderer import Renderer
from window import KeyHandler, init_window, setup_events, closer_handler
from material import Material
from shader import Shader
from model import Buffers, Model
from entity import Entity, Skybox, OkuuFumo, SelectableEntity


def local_relative_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


LOG_FPS = True

VERTEX_SHADER_FILE = local_relative_path("../shaders/main.vert")
FRAGMENT_SHADER_FILE = local_relative_path("../shaders/main.frag")


def debug_camera_handler(
    camera: Camera,
) -> KeyHandler:
    def handler(
        win: Any,
        key: int,
        scancode: int,
        action: int,
        mods: int,
    ) -> None:
        if key == glfw.KEY_Z and action == glfw.PRESS:
            print(
                f"Camera: position({camera.position.x}, {camera.position.y}, {camera.position.z})"
            )

    return handler


def main():
    # Create the renderer
    renderer = Renderer()

    # Create the camera
    camera = Camera(
        # Direct the camera to the main building
        yaw=270.0,
        position=glm.vec3(0, 0.5, 50),
    )

    # Configure window
    win = init_window("Eldrich Horrors Beyond Your Comprehension :D", 1280, 720)

    # Load and compile shaders
    main_shader = Shader.load_from_files(VERTEX_SHADER_FILE, FRAGMENT_SHADER_FILE)
    # Load all materials
    materials: Dict[str, Material] = {
        "monster-default": Material.from_texture(
            main_shader,
            local_relative_path("../../examples/monstro/monstro.jpg"),
        ),
        **Material.load_mtllib(
            main_shader, local_relative_path("../models/skybox.mtl"), "sb"
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/burgerpiz/burgerpiz.mtl"),
            "burgerpiz-",
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/okuu_fumo.mtl"),
            "okuufumo-",
        ),
    }

    # Load all models
    models: Dict[str, Model] = {
        "monster": Model.load_obj(
            local_relative_path("../../examples/monstro/monstro.obj"),
            materials,
            "monster-",
        ),
        "skybox": Model.load_obj(
            local_relative_path("../models/skybox.obj"),
            materials,
            "sb",
        ),
        "burgerpiz": Model.load_obj(
            local_relative_path("../models/burgerpiz/burgerpiz.obj"),
            materials,
            "burgerpiz-",
        ),
        "okuu_fumo": Model.load_obj(
            local_relative_path("../models/okuu_fumo.obj"),
            materials,
            "okuufumo-",
        ),
    }

    # Create entities
    entities: Dict[str, Entity] = {
        "monster": SelectableEntity(
            glfw.KEY_1,
            "monster",
            models["monster"],
            position=glm.vec3(-1.5, -0.97, 7.6),
            scale=glm.vec3(0.5),
            log_position=True,
        ),
        "skybox": Skybox(models["skybox"]),
        "map": Entity(models["burgerpiz"], position=glm.vec3(0, -1, 0)),
        "okuufumo": OkuuFumo(models["okuu_fumo"], position=glm.vec3(3.5, -0.15, 15)),
    }

    # Load buffers
    buffers = Buffers.setup_buffers(models.values())
    buffers.bind(main_shader)

    # Load textures
    Material.setup_all(materials.values())

    # Setup events
    setup_events(
        win,
        entities.values(),
        key_handlers=[
            closer_handler,
            renderer.key_handler,
            camera.key_handler,
            debug_camera_handler(camera),
        ],
        cursor_handlers=[camera.cursor_handler],
    )

    # Show window
    glfw.show_window(win)

    # Main loop
    renderer.init()
    last_render = glfw.get_time()
    last_fps = last_render
    frame_count = 0
    while not glfw.window_should_close(win):
        # Keep track of elapsed time
        current_time = glfw.get_time()
        delta_time = current_time - last_render

        if LOG_FPS:
            if current_time - last_fps >= 1:
                print(
                    f"FPS: {frame_count}; Frame Time: {(current_time - last_fps) / frame_count * 1000:.4}ms"
                )
                frame_count = 0
                last_fps = glfw.get_time()
            else:
                frame_count += 1

        # Get the events
        glfw.poll_events()

        # Update the camera
        camera.update(win, main_shader, delta_time)

        # Update elements
        for entity in entities.values():
            entity.update(delta_time, camera)

        # Clear the screen
        renderer.pre_render()

        # Render elements
        for entity in entities.values():
            renderer.draw_entity(entity, camera)

        glfw.swap_buffers(win)
        last_render = current_time

    glfw.terminate()


if __name__ == "__main__":
    main()
