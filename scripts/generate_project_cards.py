import json
import os

def xml_escape(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def generate_card_svg(project, dark_mode=True):
    width, height = 440, 240

    if dark_mode:
        bg = "#0d1117"
        border = "#30363d"
        title_color = "#58a6ff"
        cat_bg = "rgba(56, 189, 248, 0.12)"
        cat_color = "#38bdf8"
        desc_color = "#c9d1d9"
        tech_bg = "#161b22"
        tech_border = "#21262d"
        tech_color = "#34d399"
        footer_text = "#8b949e"
        accent = "#10b981"
        link_icon = "#6e7681"
    else:
        bg = "#ffffff"
        border = "#e1e4e8"
        title_color = "#0969da"
        cat_bg = "#ddf4ff"
        cat_color = "#0969da"
        desc_color = "#24292e"
        tech_bg = "#f6f8fa"
        tech_border = "#d0d7de"
        tech_color = "#059669"
        footer_text = "#57606a"
        accent = "#059669"
        link_icon = "#57606a"

    # Category Pill
    cat_text = xml_escape(project.get("category", "Project"))
    
    # Description multiline wrapping
    desc = project.get("description", "")
    words = desc.split(" ")
    lines = []
    curr_line = ""
    for w in words:
        if len(curr_line + " " + w) > 46:
            lines.append(curr_line)
            curr_line = w
        else:
            curr_line = (curr_line + " " + w).strip()
    if curr_line:
        lines.append(curr_line)
    lines = lines[:3] # max 3 lines

    desc_tspan = []
    for i, l in enumerate(lines):
        desc_tspan.append(f'<tspan x="20" y="{86 + (i * 18)}">{xml_escape(l)}</tspan>')

    # Tech Badges
    techs = project.get("technologies", [])[:5]
    badge_x = 20
    badge_y = 148
    tech_badges = []
    for t in techs:
        approx_w = len(t) * 7 + 14
        tech_badges.append(f"""
    <rect x="{badge_x}" y="{badge_y}" width="{approx_w}" height="22" rx="6" fill="{tech_bg}" stroke="{tech_border}" stroke-width="1"/>
    <text x="{badge_x + approx_w//2}" y="{badge_y + 15}" fill="{tech_color}" font-family="Fira Code, monospace" font-size="10" text-anchor="middle">{xml_escape(t)}</text>
    """)
        badge_x += approx_w + 6

    # Footer status
    live_url = project.get("live")
    live_badge = ""
    if live_url:
        live_badge = f'<text x="{width - 20}" y="208" fill="{accent}" font-family="Fira Code, monospace" font-size="11" text-anchor="end">⚡ Live Demo</text>'
    else:
        live_badge = f'<text x="{width - 20}" y="208" fill="{footer_text}" font-family="Fira Code, monospace" font-size="11" text-anchor="end">🐙 GitHub Repository</text>'

    lang_tag = xml_escape(project.get("language", ""))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-header {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 600; }}
    .card-title {{ font-family: 'Fira Code', monospace; font-size: 15px; font-weight: 700; }}
    .card-desc {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; line-height: 1.4; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <circle cx="20" cy="20" r="4.5" fill="#ff5f56"/>
  <circle cx="34" cy="20" r="4.5" fill="#ffbd2e"/>
  <circle cx="48" cy="20" r="4.5" fill="#27c93f"/>
  <text x="65" y="24" fill="{title_color}" class="terminal-header">$ ./{xml_escape(project["id"])}</text>
  
  <!-- Category Pill -->
  <rect x="{width - 150}" y="10" width="130" height="20" rx="10" fill="{cat_bg}"/>
  <text x="{width - 85}" y="24" fill="{cat_color}" font-family="Fira Code, monospace" font-size="10" font-weight="600" text-anchor="middle">{cat_text}</text>

  <line x1="0" y1="38" x2="{width}" y2="38" stroke="{border}" stroke-width="1"/>

  <!-- Project Name -->
  <text x="20" y="62" fill="{title_color}" class="card-title">{xml_escape(project["name"])}</text>

  <!-- Description -->
  <text fill="{desc_color}" class="card-desc">
    {"".join(desc_tspan)}
  </text>

  <!-- Tech Stack Badges -->
  {"".join(tech_badges)}

  <line x1="20" y1="188" x2="{width - 20}" y2="188" stroke="{border}" stroke-width="1"/>

  <!-- Footer Info -->
  <text x="20" y="208" fill="{footer_text}" font-family="Fira Code, monospace" font-size="11">🛠️ {lang_tag}</text>
  {live_badge}
</svg>"""
    return svg

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")
    cards_dir = os.path.join(assets_dir, "cards")
    os.makedirs(cards_dir, exist_ok=True)

    projects_file = os.path.join(assets_dir, "projects.json")
    with open(projects_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    projects = data.get("projects", [])
    for p in projects:
        p_id = p["id"]
        dark_svg = generate_card_svg(p, dark_mode=True)
        light_svg = generate_card_svg(p, dark_mode=False)

        dark_path = os.path.join(cards_dir, f"{p_id}-dark.svg")
        light_path = os.path.join(cards_dir, f"{p_id}-light.svg")

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(dark_svg)
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(light_svg)
        print(f"Generated card: {p_id}-dark.svg & {p_id}-light.svg")

if __name__ == "__main__":
    run()
