import os
from PIL import Image

def generate_halftone_portrait():
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    portrait_path = os.path.join(assets_dir, "portrait.png")

    if os.path.exists(portrait_path):
        print(f"Using transparent halftone portrait at {portrait_path}.")
        return

    print("Warning: portrait.png not found.")

if __name__ == "__main__":
    generate_halftone_portrait()
