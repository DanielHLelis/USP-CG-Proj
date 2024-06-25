# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626

from typing import Any, Callable
import glfw

from .entity import Entity


def entity_position_handler(
    entity: Entity, name: str, key: int = glfw.KEY_Z
) -> Callable[[Any, int, int, int, int], None]:
    target_key = key

    def handler(win: Any, key: int, scancode: int, action: int, mods: int):
        nonlocal target_key, name
        if key == target_key and action == glfw.PRESS:
            print(
                f"Entity ({name}): position({entity.position.x}, {entity.position.y}, {entity.position.z}) scale({entity.scale.x}, {entity.scale.y}, {entity.scale.z}) rotation({entity.angle_x}, {entity.angle_y}, {entity.angle_z})"
            )

    return handler
