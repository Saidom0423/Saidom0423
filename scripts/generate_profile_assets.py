import json
import os
import sys
import xml.etree.ElementTree as ET

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_portrait_avatar(dark_mode=True):
    width, height = 120, 120
    bg = "#0d1117" if dark_mode else "#ffffff"
    border = "#30363d" if dark_mode else "#e1e4e8"
    accent = "#10b981" if dark_mode else "#059669"
    text_color = "#58a6ff" if dark_mode else "#0969da"
    sub_color = "#c9d1d9" if dark_mode else "#24292e"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="{width}" height="{height}" rx="60" fill="{bg}" stroke="{accent}" stroke-width="2.5"/>
  <!-- Terminal Grid Pattern -->
  <circle cx="60" cy="60" r="50" fill="none" stroke="{border}" stroke-width="1" stroke-dasharray="4 4"/>
  <circle cx="60" cy="60" r="38" fill="none" stroke="{accent}" stroke-width="1" stroke-opacity="0.4"/>
  
  <!-- Monogram & Terminal Prompt -->
  <text x="60" y="56" fill="{text_color}" font-family="Fira Code, monospace" font-size="24" font-weight="bold" text-anchor="middle">SD</text>
  <text x="60" y="76" fill="{accent}" font-family="Fira Code, monospace" font-size="11" font-weight="600" text-anchor="middle">&gt;_ dev</text>
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

