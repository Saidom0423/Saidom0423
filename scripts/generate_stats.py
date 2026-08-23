import json
import os
import urllib.request

def fetch_github_data():
    user_url = "https://api.github.com/users/Saidom0423"
    repos_url = "https://api.github.com/users/Saidom0423/repos?per_page=100"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        user_req = urllib.request.Request(user_url, headers=headers)
        user_info = json.loads(urllib.request.urlopen(user_req).read())
        
        repos_req = urllib.request.Request(repos_url, headers=headers)
        repos_info = json.loads(urllib.request.urlopen(repos_req).read())

        total_repos = len(repos_info)
        total_stars = sum(r.get("stargazers_count", 0) for r in repos_info)
        total_forks = sum(r.get("forks_count", 0) for r in repos_info)

        # Count languages
        langs = {}
        for r in repos_info:
            l = r.get("language")
            if l:
                langs[l] = langs.get(l, 0) + 1

        return {
            "name": user_info.get("name") or "Sai Dom",
            "repos": total_repos,
            "stars": total_stars,
            "forks": total_forks,
            "followers": user_info.get("followers", 0),
            "following": user_info.get("following", 0),
            "languages": langs,
            "location": user_info.get("location") or "Pune, India"
        }
    except Exception as e:
        print(f"Warning: Could not fetch live GitHub metrics ({e}), using cached profile data.")
        return {
            "name": "Sai Dom",
            "repos": 11,
            "stars": 1,
            "forks": 0,
            "followers": 0,
            "following": 0,
            "languages": {"Dart": 3, "JavaScript": 4, "Python": 1, "HTML": 3},
            "location": "Pune, India"
        }

def generate_stats_svg(data, dark_mode=True):
    width, height = 480, 220

    if dark_mode:
        bg = "#0d1117"
        border = "#30363d"
        title_color = "#58a6ff"
        text_primary = "#c9d1d9"
        text_secondary = "#8b949e"
        accent = "#10b981"
        card_bg = "#161b22"
        card_border = "#21262d"
    else:
        bg = "#ffffff"
        border = "#e1e4e8"
        title_color = "#0969da"
        text_primary = "#24292e"
        text_secondary = "#57606a"
        accent = "#059669"
        card_bg = "#f6f8fa"
        card_border = "#d0d7de"

    stats_items = [
        {"label": "Public Repositories", "val": str(data["repos"]), "icon": "📦"},
        {"label": "Total Stars Earned", "val": str(data["stars"]), "icon": "⭐"},
        {"label": "Primary Focus", "val": "Backend &amp; Mobile", "icon": "⚙️"},
        {"label": "Location", "val": data["location"], "icon": "📍"},
    ]

    grid_cards = []
    positions = [(20, 52), (245, 52), (20, 130), (245, 130)]
    for i, item in enumerate(stats_items):
        x, y = positions[i]
        grid_cards.append(f"""
    <rect x="{x}" y="{y}" width="215" height="68" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <text x="{x + 14}" y="{y + 26}" fill="{text_secondary}" font-family="Fira Code, monospace" font-size="11">{item["icon"]} {item["label"]}</text>
    <text x="{x + 14}" y="{y + 52}" fill="{accent}" font-family="Fira Code, monospace" font-size="15" font-weight="bold">{item["val"]}</text>
    """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-header {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 600; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <circle cx="20" cy="20" r="4.5" fill="#ff5f56"/>
  <circle cx="34" cy="20" r="4.5" fill="#ffbd2e"/>
  <circle cx="48" cy="20" r="4.5" fill="#27c93f"/>
  <text x="65" y="24" fill="{title_color}" class="terminal-header">$ ./fetch_github_metrics.sh</text>
  <line x1="0" y1="38" x2="{width}" y2="38" stroke="{border}" stroke-width="1"/>

  <!-- Stats Grid -->
  {"".join(grid_cards)}
</svg>"""
    return svg

def generate_languages_svg(dark_mode=True):
    width, height = 480, 140

    if dark_mode:
        bg = "#0d1117"
        border = "#30363d"
        title_color = "#58a6ff"
        text_color = "#c9d1d9"
    else:
        bg = "#ffffff"
        border = "#e1e4e8"
        title_color = "#0969da"
        text_color = "#24292e"

    lang_data = [
        {"name": "Dart / Flutter", "pct": 42, "color": "#00B4AB"},
        {"name": "JavaScript / React", "pct": 28, "color": "#F7DF1E"},
        {"name": "Python / Django", "pct": 18, "color": "#3572A5"},
        {"name": "HTML / CSS", "pct": 12, "color": "#e34c26"},
    ]

    # Bar elements
    bar_x = 20
    bar_y = 55
    bar_w = 440
    bar_h = 16

    bar_rects = []
    curr_x = bar_x
    for l in lang_data:
        w = (l["pct"] / 100.0) * bar_w
        bar_rects.append(f'<rect x="{curr_x}" y="{bar_y}" width="{w}" height="{bar_h}" fill="{l["color"]}" />')
        curr_x += w

    # Legend items
    legend_items = []
    leg_x_positions = [20, 140, 280, 390]
    for i, l in enumerate(lang_data):
        lx = leg_x_positions[i]
        ly = 102
        legend_items.append(f"""
    <circle cx="{lx + 6}" cy="{ly}" r="5" fill="{l["color"]}"/>
    <text x="{lx + 16}" y="{ly + 4}" fill="{text_color}" font-family="Fira Code, monospace" font-size="11">{l["name"]} <tspan font-weight="bold">{l["pct"]}%</tspan></text>
    """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-header {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; font-weight: 600; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <circle cx="20" cy="20" r="4.5" fill="#ff5f56"/>
  <circle cx="34" cy="20" r="4.5" fill="#ffbd2e"/>
  <circle cx="48" cy="20" r="4.5" fill="#27c93f"/>
  <text x="65" y="24" fill="{title_color}" class="terminal-header">$ cat repo_languages.json</text>
  <line x1="0" y1="38" x2="{width}" y2="38" stroke="{border}" stroke-width="1"/>

  <!-- Progress Bar -->
  <g clip-path="url(#bar-clip)">
    <clipPath id="bar-clip">
      <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="8"/>
    </clipPath>
    {"".join(bar_rects)}
  </g>

  <!-- Legend -->
  {"".join(legend_items)}
</svg>"""
    return svg

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    data = fetch_github_data()

    stats_dark = generate_stats_svg(data, dark_mode=True)
    stats_light = generate_stats_svg(data, dark_mode=False)

    with open(os.path.join(assets_dir, "stats-dark.svg"), "w", encoding="utf-8") as f:
        f.write(stats_dark)
    with open(os.path.join(assets_dir, "stats-light.svg"), "w", encoding="utf-8") as f:
        f.write(stats_light)
    print("Generated stats-dark.svg and stats-light.svg")

    langs_svg = generate_languages_svg(dark_mode=True)
    with open(os.path.join(assets_dir, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(langs_svg)
    print("Generated languages.svg")

if __name__ == "__main__":
    run()
