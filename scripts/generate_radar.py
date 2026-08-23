import json
import math
import os
import urllib.request

def polar_to_cartesian(cx, cy, radius, angle_deg):
    angle_rad = math.radians(angle_deg - 90)
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)
    return round(x, 2), round(y, 2)

def generate_radar_svg(title, subtitle, data, dark_mode=True):
    width, height = 480, 360
    cx, cy = 240, 195
    max_r = 115
    levels = 4
    
    if dark_mode:
        bg = "#0d1117"
        border = "#30363d"
        title_color = "#58a6ff"
        sub_color = "#8b949e"
        grid_color = "#21262d"
        axis_color = "#30363d"
        poly_fill = "rgba(16, 185, 129, 0.2)"
        poly_stroke = "#10b981"
        dot_fill = "#34d399"
        label_color = "#c9d1d9"
        value_color = "#10b981"
        terminal_dot = "#10b981"
    else:
        bg = "#ffffff"
        border = "#e1e4e8"
        title_color = "#0969da"
        sub_color = "#57606a"
        grid_color = "#f6f8fa"
        axis_color = "#d0d7de"
        poly_fill = "rgba(5, 150, 105, 0.15)"
        poly_stroke = "#059669"
        dot_fill = "#059669"
        label_color = "#24292e"
        value_color = "#059669"
        terminal_dot = "#059669"

    keys = list(data.keys())
    values = list(data.values())
    n = len(keys)
    if n == 0:
        return ""

    angle_step = 360.0 / n

    # Grid rings
    grid_polys = []
    for level in range(1, levels + 1):
        r = (max_r / levels) * level
        pts = [f"{polar_to_cartesian(cx, cy, r, i * angle_step)[0]},{polar_to_cartesian(cx, cy, r, i * angle_step)[1]}" for i in range(n)]
        grid_polys.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{grid_color}" stroke-width="1.5" />')

    # Axis lines
    axis_lines = []
    for i in range(n):
        x, y = polar_to_cartesian(cx, cy, max_r, i * angle_step)
        axis_lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{axis_color}" stroke-width="1" stroke-dasharray="3,3" />')

    # Data polygon & dots & labels
    data_pts = []
    dots = []
    labels = []
    for i, (k, v) in enumerate(zip(keys, values)):
        r = (v / 100.0) * max_r
        x, y = polar_to_cartesian(cx, cy, r, i * angle_step)
        data_pts.append(f"{x},{y}")
        dots.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{dot_fill}" stroke="{bg}" stroke-width="1.5" />')

        # Label position slightly outside max_r
        lx, ly = polar_to_cartesian(cx, cy, max_r + 28, i * angle_step)
        anchor = "middle"
        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"
        
        labels.append(
            f'<text x="{lx}" y="{ly}" font-family="Fira Code, monospace, sans-serif" font-size="11" fill="{label_color}" text-anchor="{anchor}" dominant-baseline="middle">{k} <tspan fill="{value_color}" font-weight="bold">{v}%</tspan></text>'
        )

    poly_svg = f'<polygon points="{" ".join(data_pts)}" fill="{poly_fill}" stroke="{poly_stroke}" stroke-width="2.5" stroke-linejoin="round" />'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-header {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 600; }}
    .sub-header {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <circle cx="20" cy="20" r="4.5" fill="#ff5f56"/>
  <circle cx="34" cy="20" r="4.5" fill="#ffbd2e"/>
  <circle cx="48" cy="20" r="4.5" fill="#27c93f"/>
  <text x="65" y="24" fill="{title_color}" class="terminal-header">$ {title}</text>
  <text x="{width - 20}" y="24" fill="{sub_color}" class="sub-header" text-anchor="end">{subtitle}</text>
  <line x1="0" y1="38" x2="{width}" y2="38" stroke="{border}" stroke-width="1"/>

  <!-- Radar Grid & Axes -->
  {"".join(grid_polys)}
  {"".join(axis_lines)}

  <!-- Data Polygon & Elements -->
  {poly_svg}
  {"".join(dots)}
  {"".join(labels)}
</svg>"""
    return svg

def get_repo_languages():
    url = "https://api.github.com/users/Saidom0423/repos?per_page=100"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = json.loads(urllib.request.urlopen(req).read())
        lang_bytes = {}
        for r in data:
            lang = r.get("language")
            if lang:
                # Use size or approximate code weight
                lang_bytes[lang] = lang_bytes.get(lang, 0) + (r.get("size", 100) or 100)
        
        # Sort and take top 6
        sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:6]
        max_val = max([v for k, v in sorted_langs]) if sorted_langs else 1
        
        # Normalize to percentage scale
        result = {}
        for k, v in sorted_langs:
            score = min(98, max(45, int((v / max_val) * 95)))
            result[k] = score
        return result
    except Exception as e:
        print(f"Warning: Failed to fetch language stats ({e}), using default repo footprint.")
        return {
            "Dart": 92,
            "Python": 88,
            "JavaScript": 85,
            "HTML/CSS": 78,
            "Kotlin": 70,
            "C++": 65
        }

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # 1. Radar A: Engineering Capability
    skills_file = os.path.join(assets_dir, "skills.json")
    if os.path.exists(skills_file):
        with open(skills_file, "r") as f:
            skills_data = json.load(f)
    else:
        skills_data = {"Backend": 90, "API Design": 88, "Database": 82, "Frontend": 75, "Mobile": 78, "Networking": 72, "Cloud": 70, "System Design": 68}

    radar_dark = generate_radar_svg("skill_radar.sh", "Engineering Capability", skills_data, dark_mode=True)
    radar_light = generate_radar_svg("skill_radar.sh", "Engineering Capability", skills_data, dark_mode=False)

    with open(os.path.join(assets_dir, "radar-dark.svg"), "w", encoding="utf-8") as f:
        f.write(radar_dark)
    with open(os.path.join(assets_dir, "radar-light.svg"), "w", encoding="utf-8") as f:
        f.write(radar_light)
    print("Generated radar-dark.svg and radar-light.svg")

    # 2. Radar B: Repository Language Footprint
    langs_data = get_repo_languages()
    langs_dark = generate_radar_svg("repo_footprint.sh", "Language Footprint", langs_data, dark_mode=True)
    langs_light = generate_radar_svg("repo_footprint.sh", "Language Footprint", langs_data, dark_mode=False)

    with open(os.path.join(assets_dir, "radar-langs-dark.svg"), "w", encoding="utf-8") as f:
        f.write(langs_dark)
    with open(os.path.join(assets_dir, "radar-langs-light.svg"), "w", encoding="utf-8") as f:
        f.write(langs_light)
    print("Generated radar-langs-dark.svg and radar-langs-light.svg")

if __name__ == "__main__":
    run()
