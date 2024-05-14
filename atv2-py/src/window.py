from typing import Any, List, Callable


import glfw

from entity import Entity

KeyHandler = Callable[[Any, int, int, int, int], None]
CursorHandler = Callable[[Any, float, float, float, float], None]


def init_window(
    title: str,
    width: int,
    height: int,
    resizable=False,
) -> Any:
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


def setup_events(
    win: Any,
    entities: list[Entity] = [],
    key_handlers: List[KeyHandler] = [],
    cursor_handlers: List[CursorHandler] = [],
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


def closer_handler(win: Any, key: int, scancode: int, action: int, mods: int) -> None:
    # Exit handler (ESC)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(win, True)
