import math
from PIL import Image, ImageDraw, ImageOps, ImageFilter
from config import INTENTION_COLORS, KAMEA_SQUARES

def draw_background(draw, cx, cy, outer_radius, method, planet=None, show_grid=False, grid_color="gray"):
    """Draw background: circle for most methods, square grid for Kamea, optional internal lines."""
    if method == "kamea":
        # Square boundary
        draw.rectangle(
            (cx - outer_radius, cy - outer_radius, cx + outer_radius, cy + outer_radius),
            outline="black",
            width=2
        )
        if show_grid:
            size = len(KAMEA_SQUARES.get(planet, [[0]]))
            cell_size = (outer_radius * 2) / size
            for i in range(1, size):
                # Vertical lines
                draw.line(
                    [(cx - outer_radius + i * cell_size, cy - outer_radius),
                     (cx - outer_radius + i * cell_size, cy + outer_radius)],
                    fill=grid_color, width=1
                )
                # Horizontal lines
                draw.line(
                    [(cx - outer_radius, cy - outer_radius + i * cell_size),
                     (cx + outer_radius, cy - outer_radius + i * cell_size)],
                    fill=grid_color, width=1
                )
    else:
        # Circle boundary
        draw.ellipse(
            (cx - outer_radius, cy - outer_radius, cx + outer_radius, cy + outer_radius),
            outline="black",
            width=2
        )
        if show_grid:
            if method == "numeric":
                divisions = 9
            elif method == "planetary":
                divisions = 7
            elif method == "rosicrucian":
                divisions = 4  # arms of the cross
            else:  # classic
                divisions = len("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

            for i in range(divisions):
                angle = (i / divisions) * 2 * math.pi
                x = cx + outer_radius * math.cos(angle)
                y = cy + outer_radius * math.sin(angle)
                draw.line([(cx, cy), (x, y)], fill=grid_color, width=1)

def draw_sigil(draw, cx, cy, outer_radius, points, stroke_width, line_color, circle_color, method, planet=None, show_grid=False, grid_color="gray"):
    """Draw points and connecting lines of a sigil."""
    draw_background(draw, cx, cy, outer_radius, method, planet, show_grid, grid_color)

    for px, py in points:
        draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=line_color)

    if len(points) > 1:
        draw.line(points, fill=line_color, width=stroke_width, joint="curve")

def generate_sigil(phrase, filepath, intention, mode, versions, method_func, method="classic", planet=None, show_grid=False):
    """Generate a sigil image using a specific method function."""
    size, margin, stroke_width = 800, 20, 5
    cx, cy = size / 2, size / 2
    outer_radius = size / 2 - margin

    if mode == "traditional":
        line_color, circle_color = "black", "black"
    else:
        line_color, circle_color = INTENTION_COLORS.get(intention, ("black", "gray"))

    # Generate sigil points once
    points = method_func(cx=cx, cy=cy, radius=outer_radius, text=phrase, rotation_deg=(len(phrase) * 7) % 360)

    for v in versions:
        # Grid color depends on output version
        grid_color = "black" if v in ["bw", "transparent"] else "gray"

        if v == "transparent":
            # Transparent canvas
            transparent_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            transparent_draw = ImageDraw.Draw(transparent_img)

            draw_sigil(
                transparent_draw, cx, cy, outer_radius, points,
                stroke_width, line_color, circle_color, method, planet, show_grid,
                grid_color=grid_color
            )

            transparent_img.save(filepath.replace(".png", "_transparent.png"))
            continue

        # White canvas for other modes
        base_img = Image.new("RGB", (size, size), "white")
        draw = ImageDraw.Draw(base_img)

        # Glow effect (modern only, not for transparent)
        if mode == "modern":
            glow_layer = Image.new("RGB", (size, size), "black")
            glow_draw = ImageDraw.Draw(glow_layer)
            draw_sigil(glow_draw, cx, cy, outer_radius, points, stroke_width*2, line_color, line_color, method, planet, show_grid, grid_color)
            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(25))
            base_img = Image.composite(glow_layer, base_img, glow_layer.convert("L"))
            draw = ImageDraw.Draw(base_img)

        # Final sigil
        draw_sigil(draw, cx, cy, outer_radius, points, stroke_width, line_color, circle_color, method, planet, show_grid, grid_color)

        # Save in requested version
        if v == "normal":
            base_img.save(filepath.replace(".png", "_normal.png"))
        elif v == "inverted":
            ImageOps.invert(base_img).save(filepath.replace(".png", "_inverted.png"))
        elif v == "bw":
            bw = base_img.convert("L").point(lambda x: 0 if x < 128 else 255, '1')
            bw.save(filepath.replace(".png", "_bw.png"))
