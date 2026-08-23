import os
import urllib.request
import math
from PIL import Image, ImageDraw, ImageEnhance

def generate_halftone_portrait():
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    avatar_path = os.path.join(assets_dir, "avatar.png")
    out_path = os.path.join(assets_dir, "portrait.png")

    if not os.path.exists(avatar_path):
        url = "https://avatars.githubusercontent.com/u/143344009?v=4"
        urllib.request.urlretrieve(url, avatar_path)

    orig_img = Image.open(avatar_path).convert("RGBA")
    w, h = orig_img.size

    # Crop tightly on head, face, and upper body
    crop_box = (int(w * 0.32), int(h * 0.12), int(w * 0.76), int(h * 0.68))
    img_cropped = orig_img.crop(crop_box).convert("RGB")

    # Enhance contrast and warmth for skin tones
    enhancer_c = ImageEnhance.Contrast(img_cropped)
    img_cropped = enhancer_c.enhance(2.3)

    enhancer_s = ImageEnhance.Color(img_cropped)
    img_cropped = enhancer_s.enhance(1.6)

    # Canvas size
    out_size = 560
    
    # Grid resolution (dots across)
    grid_cols = 68
    grid_rows = 68
    cell_w = out_size / grid_cols
    cell_h = out_size / grid_rows

    img_sampled = img_cropped.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS)
    pixels = img_sampled.load()

    dots = []
    max_radius = min(cell_w, cell_h) * 0.48

    for y in range(grid_rows):
        for x in range(grid_cols):
            r, g, b = pixels[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b

            # Subject segmentation
            is_skin = (r > g and r > b and r > 35)
            is_white_shirt = (r > 110 and g > 110 and b > 110 and y > grid_rows * 0.4)
            is_dark_clothing_or_hair = (lum > 18 and lum < 80 and abs(r - g) < 20 and not (g > r + 3))

            if not (is_skin or is_white_shirt or is_dark_clothing_or_hair):
                continue

            if lum < 18:
                continue

            # Scale dot radius by brightness
            normalized_lum = min(1.0, lum / 200.0)
            dot_r = (normalized_lum ** 0.75) * max_radius
            if dot_r < 0.8:
                dot_r = 0.8

            cx = (x + 0.5) * cell_w
            cy = (y + 0.5) * cell_h

            dots.append((cx, cy, dot_r, (r, g, b, 255)))

    # Calculate vertical shift to center subject in canvas
    if dots:
        min_y = min(d[1] - d[2] for d in dots)
        max_y = max(d[1] + d[2] for d in dots)
        subject_h = max_y - min_y
        offset_y = (out_size - subject_h) / 2.0 - min_y
    else:
        offset_y = 0

    # Draw dark background canvas (#0d1117)
    canvas = Image.new("RGBA", (out_size, out_size), (13, 17, 23, 255))
    draw = ImageDraw.Draw(canvas)

    for cx, cy, dot_r, color in dots:
        cy_centered = cy + offset_y
        draw.ellipse(
            [cx - dot_r, cy_centered - dot_r, cx + dot_r, cy_centered + dot_r],
            fill=color
        )

    canvas.save(out_path, "PNG")
    print(f"Successfully generated centered halftone matrix portrait PNG at {out_path}!")

if __name__ == "__main__":
    generate_halftone_portrait()
