import json
import os
import sys
import xml.etree.ElementTree as ET

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_portrait_avatar(dark_mode=True):
    width, height = 140, 140
    bg = "#0d1117" if dark_mode else "#ffffff"
    border = "#30363d" if dark_mode else "#e1e4e8"
    accent = "#10b981" if dark_mode else "#059669"

    avatar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "avatar.png")
    if not os.path.exists(avatar_path):
        import urllib.request
        try:
            url = "https://avatars.githubusercontent.com/u/143344009?v=4"
            urllib.request.urlretrieve(url, avatar_path)
        except Exception:
            pass

    b64_img = ""
    if os.path.exists(avatar_path):
        import base64
        with open(avatar_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")

    if b64_img:
        img_element = f'<image href="data:image/png;base64,{b64_img}" x="16" y="16" width="108" height="108" clip-path="url(#avatar-clip)" />'
    else:
        text_color = "#58a6ff" if dark_mode else "#0969da"
        img_element = f'<text x="70" y="70" fill="{text_color}" font-family="Fira Code, monospace" font-size="28" font-weight="bold" text-anchor="middle">SD</text>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <clipPath id="avatar-clip">
      <circle cx="70" cy="70" r="54" />
    </clipPath>
  </defs>

  <!-- Outer Styled Ring -->
  <circle cx="70" cy="70" r="66" fill="{bg}" stroke="{accent}" stroke-width="2.5"/>
  <circle cx="70" cy="70" r="60" fill="none" stroke="{border}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- User Avatar Image -->
  {img_element}

  <!-- Overlay Accent Ring -->
  <circle cx="70" cy="70" r="54" fill="none" stroke="{accent}" stroke-width="2"/>

  <!-- Terminal Badge Pill -->
  <rect x="35" y="112" width="70" height="20" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <text x="70" y="125" fill="{accent}" font-family="Fira Code, monospace" font-size="10" font-weight="bold" text-anchor="middle">&gt;_ dev</text>
</svg>"""
    return svg

def validate_json_configs(assets_dir):
    skills_path = os.path.join(assets_dir, "skills.json")
    projects_path = os.path.join(assets_dir, "projects.json")

    print("[1/5] Validating JSON configurations...")
    if not os.path.exists(skills_path):
        raise FileNotFoundError(f"Missing {skills_path}")
    with open(skills_path, "r", encoding="utf-8") as f:
        skills = json.load(f)
        if not isinstance(skills, dict):
            raise ValueError("skills.json must be a JSON object mapping skills to numbers.")

    if not os.path.exists(projects_path):
        raise FileNotFoundError(f"Missing {projects_path}")
    with open(projects_path, "r", encoding="utf-8") as f:
        projects = json.load(f)
        if "projects" not in projects or not isinstance(projects["projects"], list):
            raise ValueError("projects.json must contain a 'projects' list.")
    print("  [OK] skills.json and projects.json validated successfully.")

def run_generators(script_dir):
    print("[2/5] Executing asset generator scripts...")
    
    # Import subgenerators directly
    sys.path.insert(0, script_dir)
    import generate_radar
    import generate_stats
    import generate_project_cards

    print("  -> Running generate_radar.py...")
    generate_radar.run()

    print("  -> Running generate_stats.py...")
    generate_stats.run()

    print("  -> Running generate_project_cards.py...")
    generate_project_cards.run()

def generate_portrait(assets_dir):
    print("[3/5] Generating profile avatar portrait SVG...")
    portrait_svg = generate_portrait_avatar(dark_mode=True)
    portrait_path = os.path.join(assets_dir, "portrait.svg")
    with open(portrait_path, "w", encoding="utf-8") as f:
        f.write(portrait_svg)
    print("  [OK] Generated assets/portrait.svg")

def validate_svgs(assets_dir):
    print("[4/5] Validating SVG files and XML structure...")
    svg_files = []
    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".svg"):
                svg_files.append(os.path.join(root, file))

    if not svg_files:
        raise RuntimeError("No SVG files found in assets directory!")

    invalid_count = 0
    for svg_path in svg_files:
        try:
            ET.parse(svg_path)
        except ET.ParseError as e:
            print(f"  [FAIL] XML Parse Error in {os.path.relpath(svg_path, assets_dir)}: {e}")
            invalid_count += 1

    if invalid_count > 0:
        raise RuntimeError(f"{invalid_count} SVG file(s) failed XML validation.")
    
    print(f"  [OK] All {len(svg_files)} generated SVG files passed XML validation.")

def validate_readme_links(project_root):
    print("[5/5] Checking README links and asset paths...")
    readme_path = os.path.join(project_root, "README.md")
    if not os.path.exists(readme_path):
        print("  [INFO] README.md does not exist yet. Skipping path check.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for assets/ references
    import re
    asset_refs = re.findall(r'assets/[a-zA-Z0-9_\-/\.]+', content)
    missing = []
    for ref in set(asset_refs):
        full_path = os.path.join(project_root, ref)
        if not os.path.exists(full_path):
            missing.append(ref)

    if missing:
        print(f"  [WARN] Found {len(missing)} broken relative asset reference(s): {missing}")
    else:
        print("  [OK] All referenced README asset paths verified successfully.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")

    print("==================================================")
    print("      BUILDING GITHUB PROFILE ASSET SYSTEM        ")
    print("==================================================")
    
    validate_json_configs(assets_dir)
    run_generators(script_dir)
    generate_portrait(assets_dir)
    validate_svgs(assets_dir)
    validate_readme_links(project_root)

    print("==================================================")
    print("  SUCCESS: Profile assets generated & validated!  ")
    print("==================================================")

if __name__ == "__main__":
    main()

