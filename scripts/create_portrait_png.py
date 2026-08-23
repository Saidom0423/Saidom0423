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

    # Crop precisely on head, face, and upper shoulders
    crop_box = (int(w * 0.35), int(h * 0.12), int(w * 0.75), int(h * 0.55))
    img_cropped = orig_img.crop(crop_box).convert("RGB")

    # Contrast & warmth enhancement
    enhancer_c = ImageEnhance.Contrast(img_cropped)
    img_cropped = enhancer_c.enhance(2.2)

    enhancer_s = ImageEnhance.Color(img_cropped)
    img_cropped = enhancer_s.enhance(1.6)

    # Resolution
    grid_cols = 64
    grid_rows = 64
    cell_size = 10

    img_sampled = img_cropped.resize((grid_cols, grid_rows), Image.Resampling.LANCZOS)
    pixels = img_sampled.load()

    dots = []
    max_radius = cell_size * 0.48

    for y in range(grid_rows):
        for x in range(grid_cols):
            cx = (x + 0.5) * cell_size
            cy = (y + 0.5) * cell_size

            # Ignore top sky noise
            if cy < 160 or (cx < 200 and cy < 240) or (cx > 450 and cy < 200):
                continue

            r, g, b = pixels[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b

            # Exclude foliage, sky, and non-subject elements
            is_skin = (r > g and r > b and r > 35)
            is_white_shirt = (r > 110 and g > 110 and b > 110 and y > grid_rows * 0.45)
            is_dark_hair_jacket = (lum > 18 and lum < 80 and abs(r - g) < 20 and not (g > r + 3))

            if not (is_skin or is_white_shirt or is_dark_hair_jacket):
                continue

            if lum < 18:
                continue

            normalized_lum = min(1.0, lum / 200.0)
            dot_r = (normalized_lum ** 0.75) * max_radius
            if dot_r < 0.8:
                dot_r = 0.8

            dots.append((cx, cy, dot_r, (r, g, b, 255)))

    if not dots:
        print("Warning: No dots generated.")
        return

    # Find tight bounding box of subject dots
    min_x = min(d[0] - d[2] for d in dots)
    max_x = max(d[0] + d[2] for d in dots)
    min_y = min(d[1] - d[2] for d in dots)
    max_y = max(d[1] + d[2] for d in dots)

    subject_w = int(max_x - min_x) + 20
    subject_h = int(max_y - min_y) + 20

    # Draw canvas cropped tightly to subject bounding box
    canvas = Image.new("RGBA", (subject_w, subject_h), (13, 17, 23, 255))
    draw = ImageDraw.Draw(canvas)

    for cx, cy, dot_r, color in dots:
        new_cx = cx - min_x + 10
        new_cy = cy - min_y + 10
        draw.ellipse(
            [new_cx - dot_r, new_cy - dot_r, new_cx + dot_r, new_cy + dot_r],
            fill=color
        )

    canvas.save(out_path, "PNG")
    print(f"Successfully generated pure halftone matrix portrait PNG ({subject_w}x{subject_h}) at {out_path}!")

if __name__ == "__main__":
    generate_halftone_portrait()
