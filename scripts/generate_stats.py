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

        return {
            "username": user_info.get("login") or "Saidom0423",
            "repos": total_repos,
            "stars": total_stars,
            "followers": user_info.get("followers", 0),
            "contributions": "100+",
            "current_streak": 1,
            "longest_streak": 5
        }
    except Exception as e:
        print(f"Warning: Could not fetch live GitHub metrics ({e}), using default profile stats.")
        return {
            "username": "Saidom0423",
            "repos": 11,
            "stars": 1,
            "followers": 0,
            "contributions": "100+",
            "current_streak": 1,
            "longest_streak": 5
        }

def generate_gargi_stats_card(data, dark_mode=True):
    width, height = 540, 360

    if dark_mode:
        bg = "#0d1117"
        border = "#21262d"
        user_color = "#10b981"
        meta_color = "#8b949e"
        num_color = "#ffffff"
        label_color = "#8b949e"
        lang_title_color = "#38bdf8"
        text_color = "#c9d1d9"
        sep_color = "#30363d"
    else:
        bg = "#ffffff"
        border = "#d0d7de"
        user_color = "#059669"
        meta_color = "#57606a"
        num_color = "#24292e"
        label_color = "#57606a"
        lang_title_color = "#0969da"
        text_color = "#24292e"
        sep_color = "#e1e4e8"

    # Languages breakdown data
    lang_data = [
        {"name": "Dart", "size": "184 kB", "pct": "42.0%", "val": 42.0, "color": "#00B4AB"},
        {"name": "JavaScript", "size": "43.0 kB", "pct": "28.0%", "val": 28.0, "color": "#F7DF1E"},
        {"name": "Python", "size": "17.5 kB", "pct": "18.0%", "val": 18.0, "color": "#3572A5"},
        {"name": "Kotlin", "size": "12.0 kB", "pct": "7.0%", "val": 7.0, "color": "#7F52FF"},
        {"name": "HTML/CSS", "size": "15.0 kB", "pct": "5.0%", "val": 5.0, "color": "#e34c26"},
    ]

    # Progress bar segments
    bar_x = 24
    bar_y = 230
    bar_w = 492
    bar_h = 10
    bar_rects = []
    curr_x = bar_x
    for l in lang_data:
        w = (l["val"] / 100.0) * bar_w
        bar_rects.append(f'<rect x="{curr_x}" y="{bar_y}" width="{w}" height="{bar_h}" fill="{l["color"]}" />')
        curr_x += w

    # Language list grid (2 columns)
    col1_items = [lang_data[0], lang_data[2], lang_data[3]]
    col2_items = [lang_data[1], lang_data[4]]

    col1_svg = []
    for i, l in enumerate(col1_items):
        y = 264 + (i * 22)
        col1_svg.append(f"""
    <circle cx="28" cy="{y - 4}" r="4" fill="{l["color"]}"/>
    <text x="40" y="{y}" fill="{text_color}" font-family="Fira Code, monospace" font-size="12">{l["name"]}</text>
    <text x="145" y="{y}" fill="{meta_color}" font-family="Fira Code, monospace" font-size="11">{l["size"]}</text>
    <text x="220" y="{y}" fill="{meta_color}" font-family="Fira Code, monospace" font-size="11" font-weight="bold">{l["pct"]}</text>
    """)

    col2_svg = []
    for i, l in enumerate(col2_items):
        y = 264 + (i * 22)
        col2_svg.append(f"""
    <circle cx="288" cy="{y - 4}" r="4" fill="{l["color"]}"/>
    <text x="300" y="{y}" fill="{text_color}" font-family="Fira Code, monospace" font-size="12">{l["name"]}</text>
    <text x="405" y="{y}" fill="{meta_color}" font-family="Fira Code, monospace" font-size="11">{l["size"]}</text>
    <text x="480" y="{y}" fill="{meta_color}" font-family="Fira Code, monospace" font-size="11" font-weight="bold">{l["pct"]}</text>
    """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .user-title {{ font-family: 'Fira Code', monospace; font-size: 18px; font-weight: 700; }}
    .at-glance {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; }}
    .stat-num {{ font-family: 'Fira Code', monospace; font-size: 24px; font-weight: 700; }}
    .stat-label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; }}
    .lang-header {{ font-family: 'Fira Code', monospace; font-size: 14px; font-weight: 700; }}
    .lang-sub {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; }}
  </style>

  <!-- Top Stats Container Card -->
  <rect width="{width}" height="175" rx="12" fill="{bg}" stroke="{border}" stroke-width="1.5"/>

  <!-- Card Header -->
  <text x="24" y="34" fill="{user_color}" class="user-title">{data["username"]}</text>
  <text x="{width - 24}" y="34" fill="{meta_color}" class="at-glance" text-anchor="end">at a glance</text>
  <line x1="24" y1="48" x2="{width - 24}" y2="48" stroke="{sep_color}" stroke-width="1"/>

  <!-- Row 1 Stats -->
  <g>
    <text x="24" y="78" fill="{num_color}" class="stat-num">{data["stars"]}</text>
    <text x="24" y="96" fill="{label_color}" class="stat-label">Total stars</text>

    <text x="200" y="78" fill="{num_color}" class="stat-num">{data["repos"]}</text>
    <text x="200" y="96" fill="{label_color}" class="stat-label">Public repos</text>

    <text x="380" y="78" fill="{num_color}" class="stat-num">{data["followers"]}</text>
    <text x="380" y="96" fill="{label_color}" class="stat-label">Followers</text>
  </g>

  <!-- Row 2 Stats -->
  <g>
    <text x="24" y="132" fill="{num_color}" class="stat-num">{data["contributions"]}</text>
    <text x="24" y="150" fill="{label_color}" class="stat-label">Contributions (1y)</text>

    <text x="200" y="132" fill="{num_color}" class="stat-num">{data["current_streak"]}</text>
    <text x="200" y="150" fill="{label_color}" class="stat-label">Current streak</text>

    <text x="380" y="132" fill="{num_color}" class="stat-num">{data["longest_streak"]}</text>
    <text x="380" y="150" fill="{label_color}" class="stat-label">Longest streak</text>
  </g>

  <!-- Bottom Languages Section -->
  <text x="24" y="200" fill="{lang_title_color}" class="lang-header">💬 5 Languages</text>
  <text x="{width / 2}" y="218" fill="{lang_title_color}" class="lang-sub" text-anchor="middle">Most used languages</text>

  <!-- Multi-color Progress Bar -->
  <g clip-path="url(#bar-clip)">
    <clipPath id="bar-clip">
      <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5"/>
    </clipPath>
    {"".join(bar_rects)}
  </g>

  <!-- 2-Column Languages List -->
  {"".join(col1_svg)}
  {"".join(col2_svg)}
</svg>"""
    return svg

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    data = fetch_github_data()

    stats_dark = generate_gargi_stats_card(data, dark_mode=True)
    stats_light = generate_gargi_stats_card(data, dark_mode=False)

    with open(os.path.join(assets_dir, "stats-dark.svg"), "w", encoding="utf-8") as f:
        f.write(stats_dark)
    with open(os.path.join(assets_dir, "stats-light.svg"), "w", encoding="utf-8") as f:
        f.write(stats_light)
    print("Generated Gargi-style stats-dark.svg and stats-light.svg")

if __name__ == "__main__":
    run()
