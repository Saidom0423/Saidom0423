import os
import random
import xml.etree.ElementTree as ET

def generate_local_contribution_snake(dark_mode=True):
    width, height = 850, 160
    
    if dark_mode:
        bg = "#0d1117"
        border = "#21262d"
        title_color = "#58a6ff"
        text_color = "#8b949e"
        empty_dot = "#161b22"
        levels = ["#0e4429", "#006d32", "#26a641", "#39d353"]
        snake_head = "#38bdf8"
        snake_body = "#10b981"
    else:
        bg = "#ffffff"
        border = "#d0d7de"
        title_color = "#0969da"
        text_color = "#57606a"
        empty_dot = "#ebedf0"
        levels = ["#9be9a8", "#40c463", "#30a14e", "#216e39"]
        snake_head = "#0969da"
        snake_body = "#059669"

    # Grid 52 weeks x 7 days
    cols = 52
    rows = 7
    square_size = 11
    gap = 4
    start_x = 40
    start_y = 45

    # Random seed based on user for consistent contribution graph
    random.seed(423)

    rects = []
    for c in range(cols):
        for r in range(rows):
            x = start_x + c * (square_size + gap)
            y = start_y + r * (square_size + gap)
            
            # Determine contribution level
            rand_val = random.random()
            if rand_val > 0.70:
                color = random.choice(levels)
            else:
                color = empty_dot

            rects.append(f'<rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" rx="2" fill="{color}" />')

    # Add snake path elements across graph
    snake_cells = [(start_x + c * 15, start_y + (c % 7) * 15) for c in range(25, 42)]
    snake_dots = []
    for i, (sx, sy) in enumerate(snake_cells):
        color = snake_head if i == len(snake_cells) - 1 else snake_body
        r = 6 if i == len(snake_cells) - 1 else 5
        snake_dots.append(f'<circle cx="{sx + 5}" cy="{sy + 5}" r="{r}" fill="{color}" />')

    # Month labels
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    for i, m in enumerate(months):
        mx = start_x + (i * 4 * 15)
        month_labels.append(f'<text x="{mx}" y="35" fill="{text_color}" font-family="Fira Code, monospace" font-size="10">{m}</text>')

    # Day labels
    days = [("Mon", 2), ("Wed", 4), ("Fri", 6)]
    day_labels = []
    for d, r in days:
        dy = start_y + r * 15 - 3
        day_labels.append(f'<text x="12" y="{dy}" fill="{text_color}" font-family="Fira Code, monospace" font-size="10">{d}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-header {{ font-family: 'Fira Code', monospace; font-size: 12px; font-weight: 600; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <circle cx="20" cy="18" r="4" fill="#ff5f56"/>
  <circle cx="32" cy="18" r="4" fill="#ffbd2e"/>
  <circle cx="44" cy="18" r="4" fill="#27c93f"/>
  <text x="60" y="22" fill="{title_color}" class="terminal-header">$ ./contribution_snake.sh --user Saidom0423</text>
  <line x1="0" y1="30" x2="{width}" y2="30" stroke="{border}" stroke-width="1"/>

  <!-- Month & Day Labels -->
  {"".join(month_labels)}
  {"".join(day_labels)}

  <!-- Grid Cells -->
  {"".join(rects)}

  <!-- Snake Trail -->
  {"".join(snake_dots)}
</svg>"""
    return svg

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    assets_dir = os.path.join(project_root, "assets")

    dark_svg = generate_local_contribution_snake(dark_mode=True)
    light_svg = generate_local_contribution_snake(dark_mode=False)

    with open(os.path.join(assets_dir, "snake-dark.svg"), "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(os.path.join(assets_dir, "snake-light.svg"), "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Generated local assets/snake-dark.svg and assets/snake-light.svg!")

if __name__ == "__main__":
    run()
