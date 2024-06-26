# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

import os
from typing import Any, Dict

import random
import numpy as np
import glfw
import glm

from camera import Camera
from renderer import Renderer
from window import KeyHandler, init_window, setup_events, closer_handler
from light_source import LightSource
from material import Material
from shader import Shader
from model import Buffers, Model
from entity import Entity, Skybox, OkuuFumo, SelectableEntity, GlowingEntity


def local_relative_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


LOG_FPS = True

VERTEX_SHADER_FILE = local_relative_path("../shaders/phong.vert")
FRAGMENT_SHADER_FILE = local_relative_path("../shaders/phong.frag")


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


def ambient_handler(
    renderer: Renderer,
    light_sources: list[LightSource],

) -> KeyHandler:
    def handler(
        win: Any,
        key: int,
        scancode: int,
        action: int,
        mods: int,
    ) -> None:
        if key == glfw.KEY_N and action == glfw.PRESS:
            renderer.ambient_intensity -= 0.1
            print(f"Ambient intensity: {renderer.ambient_intensity}")
        if key == glfw.KEY_M and action == glfw.PRESS:
            renderer.ambient_intensity += 0.1
            print(f"Ambient intensity: {renderer.ambient_intensity}")

        if key == glfw.KEY_9 and action == glfw.PRESS:
            for light in light_sources:
                light.intensity_d -= 0.1
                light.intensity_d = np.clip(light.intensity_d,0,1)
                print(f"Diffuse Intensity: {light.intensity_d}")

        if key == glfw.KEY_0 and action == glfw.PRESS:
            for light in light_sources:
                light.intensity_d += 0.1
                light.intensity_d = np.clip(light.intensity_d,0,1)
                print(f"Diffuse Intensity: {light.intensity_d}")

        if key == glfw.KEY_V and action == glfw.PRESS:
            for light in light_sources:
                light.intensity_s -= 0.1
                light.intensity_s = np.clip(light.intensity_s,0,1)
                print(f"Specular Intensity: {light.intensity_s}")

        if key == glfw.KEY_B and action == glfw.PRESS:
            for light in light_sources:
                light.intensity_s += 0.1
                light.intensity_s = np.clip(light.intensity_s,0,1)
                print(f"Specular Intensity: {light.intensity_s}")

        if renderer.ambient_intensity < 0:
            renderer.ambient_intensity = 0

        if renderer.ambient_intensity > 1:
            renderer.ambient_intensity = 1

    return handler

def main():

    # Configure window
    win = init_window("Eldrich Horrors Beyond Your Comprehension :D", 1280, 720)

    # Load and compile shaders
    main_shader = Shader.load_from_files(VERTEX_SHADER_FILE, FRAGMENT_SHADER_FILE)

    # Create the renderer
    renderer = Renderer(
        ambient_color=np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        ambient_intensity=0.1,
    )

    # Create the camera
    camera = Camera(
        # Direct the camera to the main building
        yaw=245.0,
        position=glm.vec3(12, 1.5, 55),
    )

    # Load all materials
    materials: Dict[str, Material] = {
        **Material.load_mtllib(
            main_shader, local_relative_path("../models/12lados.mtl"), "god"
        ),
        # Monstro, my beloved
        **Material.load_mtllib(
            main_shader, local_relative_path("../models/monstro.mtl"), "monster-"
        ),
        **Material.load_mtllib(
            main_shader, local_relative_path("../models/skybox.mtl"), "sb"
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/burgerpiz/inner.mtl"),
            "burgerpiz-inner-",
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
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/boatmobile.mtl"),
            "boatmobile-",
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/krabbypatty.mtl"),
            "krabbypatty-",
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/shion.mtl"),
            "shion-",
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/spongebob.mtl"),
            "spongebob-",
        ),
        **Material.load_mtllib(
            main_shader,
            local_relative_path("../models/squidward_house.mtl"),
            "squidhouse-",
        ),
    }

    # Load all models
    models: Dict[str, Model] = {
        **Model.load_obj(
            local_relative_path("../models/12lados.obj"), materials, "god", "god"
        ),
        # Monstro, my beloved
        **Model.load_obj(
            local_relative_path("../models/monstro.obj"),
            materials,
            "monster-",
            "monster",
        ),
        **Model.load_obj(
            local_relative_path("../models/skybox.obj"),
            materials,
            "sb",
            "skybox",
        ),
        **Model.load_obj(
            local_relative_path("../models/burgerpiz/inner.obj"),
            materials,
            "burgerpiz-inner-",
            "burgerpiz_inner",
        ),
        **Model.load_obj(
            local_relative_path("../models/burgerpiz/outer.obj"),
            materials,
            "burgerpiz-",
            "burgerpiz_outer",
        ),
        **Model.load_obj(
            local_relative_path("../models/okuu_fumo.obj"),
            materials,
            "okuufumo-",
            "okuu_fumo",
        ),
        **Model.load_obj(
            local_relative_path("../models/boatmobile.obj"),
            materials,
            "boatmobile-",
            "boatmobile",
        ),
        **Model.load_obj(
            local_relative_path("../models/krabbypatty.obj"),
            materials,
            "krabbypatty-",
            "krabbypatty",
        ),
        **Model.load_obj(
            local_relative_path("../models/shion.obj"),
            materials,
            "shion-",
            "shion",
        ),
        **Model.load_obj(
            local_relative_path("../models/spongebob.obj"),
            materials,
            "spongebob-",
            "spongebob",
        ),
        **Model.load_obj(
            local_relative_path("../models/squidward_house.obj"),
            materials,
            "squidhouse-",
            "squidward_house",
        ),
    }

    # Create light sources
    internal_source = LightSource(
        position=np.array([0.0, 0.0, 0.0]),
        color=np.array([0.6, 0.6, 1.0]),
        intensity_d=1.0,
        intensity_s=1.0,
        decay_coefs=np.array([1.0, 0.01, 0.01]),
    )

    external_source = LightSource(
        position=np.array([0.0, 0.0, 0.0]),
        color=np.array([1.0, 1.0, 0.7]),
        intensity_d=1.0,
        intensity_s=1.0,
        decay_coefs=np.array([1.0, 0.01, 0]),
    )

    def god_inside_animation(entity, dt):
        entity.angle_y += 720 * dt * (np.random.normal(0.5) - 0.5)
        entity.angle_z += 720 * dt * (np.random.normal(0.5) - 0.5)
        entity.angle_x += 720 * dt * (np.random.normal(0.5) - 0.5)
        entity.scale = glm.vec3(0.1) + glm.vec3(0.01) * (random.random() - 0.5)

    def god_outside_animation(entity, dt):
        time = glfw.get_time()
        rate = 0.2
        radius = 50
        entity.position = glm.vec3(12, 16, 55) + glm.vec3(
            radius * np.cos(rate * np.pi * time),
            0,
            radius * np.sin(rate * np.pi * time),
        )

    # Create entities
    entities: Dict[str, Entity] = {
        "god_outside": GlowingEntity(
            models["god"],
            position=glm.vec3(12, 10, 55),
            scale=glm.vec3(3),
            light_source=external_source,
            ignore_lighting=True,
            animator=god_outside_animation,
        ),
        "god_inside": GlowingEntity(
            models["god"],
            position=glm.vec3(3.5, 1.85, 15),
            scale=glm.vec3(0.1),
            light_source=internal_source,
            ignore_lighting=True,
            animator=god_inside_animation,
        ),
        "monster": SelectableEntity(
            glfw.KEY_1,
            "monster",
            models["monster"],
            position=glm.vec3(-1.5, 0, 7.6),
            scale=glm.vec3(0.5),
            log_position=True,
            light_sources=[internal_source],
        ),
        "skybox": Skybox(models["skybox"]),
        "okuufumo": OkuuFumo(
            models["okuu_fumo"],
            position=glm.vec3(3.5, 0.85, 15),
            light_sources=[internal_source],
        ),
        "boatmobile": SelectableEntity(
            glfw.KEY_2,
            "boatmobile",
            models["boatmobile"],
            position=glm.vec3(2, 0.4, 50),
            angle_y=-90.0,
            log_position=True,
            light_sources=[external_source],
        ),
        "krabbypatty": SelectableEntity(
            glfw.KEY_3,
            "krabbypatty",
            models["krabbypatty"],
            position=glm.vec3(1.5, 6.8, 23),
            scale=glm.vec3(1.2),
            log_position=True,
            light_sources=[external_source],
        ),
        "shion": SelectableEntity(
            glfw.KEY_4,
            "shion",
            models["shion"],
            position=glm.vec3(2.5, 1.35, 11),
            scale=glm.vec3(0.1),
            angle_y=-90.0,
            log_position=True,
            light_sources=[internal_source],
        ),
        "spongebob": SelectableEntity(
            glfw.KEY_5,
            "spongebob",
            models["spongebob"],
            position=glm.vec3(2, 1, 4.94),
            scale=glm.vec3(1.66),
            angle_y=90,
            log_position=True,
            light_sources=[internal_source],
        ),
        "squidward_house": SelectableEntity(
            glfw.KEY_6,
            "squidward_house",
            models["squidward_house"],
            position=glm.vec3(-11, 0, 43),
            scale=glm.vec3(1.8),
            log_position=True,
            light_sources=[external_source],
        ),
        "okuufumo-ee": OkuuFumo(
            models["okuu_fumo"],
            position=glm.vec3(-11, 2, 43),
            rotation_speed=3600,
            scale=glm.vec3(4),
            handle_events=False,
            ignore_lighting=True,
        ),
        "map_internal": Entity(
            models["burgerpiz_inner"],
            position=glm.vec3(0, -0.02, 0),
            light_sources=[internal_source],
        ),
        "map_external": Entity(
            models["burgerpiz_outer"],
            position=glm.vec3(0, -0.02, 0),
            light_sources=[external_source],
        ),
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
            ambient_handler(renderer,[internal_source,external_source]),
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
