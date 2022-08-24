from typing import NamedTuple


class Region(NamedTuple):
    x: int
    y: int
    width: int
    height: int


render_map = {
    "header": Region(0, 0, 80, 24),
    "footer": Region(0, 23, 80, 24),
    "sidebar": Region(0, 0, 30, 24),
}

new_render_map = render_map.copy()
# Change position
new_render_map["sidebar"] = Region(-2, 0, 30, 24)
# New widget
new_render_map["modal"] = Region(10, 2, 60, 20)


# Get widgets which are new or changed
print(render_map.items() ^ new_render_map.items())
