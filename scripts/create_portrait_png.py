import os
import urllib.request
from PIL import Image, ImageDraw

def create_circular_portrait():
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    avatar_path = os.path.join(assets_dir, "avatar.png")
    
    # Download avatar if needed
    if not os.path.exists(avatar_path):
        url = "https://avatars.githubusercontent.com/u/143344009?v=4"
        urllib.request.urlretrieve(url, avatar_path)

    # Load original avatar photo
    img = Image.open(avatar_path).convert("RGBA")
    
    # Target canvas dimensions
    canvas_size = (280, 280) # 2x resolution for crisp display
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Draw outer background ring (#0d1117)
    draw.ellipse((10, 10, 270, 270), fill=(13, 17, 23, 255), outline=(16, 185, 129, 255), width=6)

    # Crop avatar into inner circle
    avatar_size = (220, 220)
    img_resized = img.resize(avatar_size, Image.Resampling.LANCZOS)
    
    mask = Image.new("L", avatar_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 220, 220), fill=255)

    # Paste cropped avatar in center (x=30, y=30)
    canvas.paste(img_resized, (30, 30), mask)

    # Draw inner green border ring around avatar
    draw.ellipse((30, 30, 250, 250), outline=(16, 185, 129, 255), width=4)

    # Save crisp portrait PNG
    out_path = os.path.join(assets_dir, "portrait.png")
    canvas.save(out_path, "PNG")
    print(f"Successfully generated crisp portrait PNG at {out_path}!")

if __name__ == "__main__":
    create_circular_portrait()
