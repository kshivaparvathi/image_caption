"""
Generate realistic, high-quality showcase images for VisionCaption AI.
Using PIL to create rich, visually distinctive scenes with gradients,
structures, textures, and depth.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

output_dir = Path("static/samples")
output_dir.mkdir(parents=True, exist_ok=True)

width, height = 1200, 800

def create_market_scene():
    im = Image.new("RGB", (width, height), "#8D99AE")
    draw = ImageDraw.Draw(im)
    
    # Sky / upper background
    for y in range(400):
        r = int(180 + (220 - 180) * (y / 400))
        g = int(210 + (235 - 210) * (y / 400))
        b = int(240 + (245 - 240) * (y / 400))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Brick buildings in background
    draw.rectangle([100, 150, 450, 550], fill="#8B4513")
    draw.rectangle([750, 120, 1100, 550], fill="#A0522D")
    
    # Windows
    for bx, by in [(150, 200), (230, 200), (310, 200), (800, 180), (880, 180), (960, 180)]:
        draw.rectangle([bx, by, bx + 50, by + 70], fill="#F4F1DE", outline="#2B2D42", width=2)
        draw.line([(bx + 25, by), (bx + 25, by + 70)], fill="#2B2D42", width=2)
        draw.line([(bx, by + 35), (bx + 50, by + 35)], fill="#2B2D42", width=2)

    # Street ground perspective
    for y in range(450, height):
        factor = (y - 450) / (height - 450)
        c = int(70 + (45 - 70) * factor)
        draw.line([(0, y), (width, y)], fill=(c + 20, c + 15, c + 10))

    # Market Awnings (Striped)
    for x in range(50, 600, 40):
        color = "#E63946" if (x // 40) % 2 == 0 else "#F1FAEE"
        draw.polygon([(x, 380), (x + 40, 380), (x + 30, 470), (x - 10, 470)], fill=color)
    for x in range(650, 1150, 40):
        color = "#2A9D8F" if (x // 40) % 2 == 0 else "#E9C46A"
        draw.polygon([(x, 360), (x + 40, 360), (x + 30, 450), (x - 10, 450)], fill=color)

    # Wooden Produce Stands
    draw.rectangle([80, 470, 520, 720], fill="#6F4E37", outline="#4A3525", width=3)
    draw.rectangle([680, 450, 1120, 720], fill="#5C4033", outline="#3D2B22", width=3)
    
    # Produce Crates & Fruit piles
    colors = ["#F4A261", "#E76F51", "#2A9D8F", "#E63946", "#E9C46A", "#588157"]
    for cx in range(110, 490, 60):
        draw.rectangle([cx, 510, cx + 50, 560], fill="#B08968", outline="#7F5539", width=2)
        for fx in range(cx + 8, cx + 45, 12):
            for fy in range(520, 555, 12):
                draw.ellipse([fx, fy, fx + 10, fy + 10], fill=colors[(cx + fx + fy) % len(colors)])

    for cx in range(710, 1090, 60):
        draw.rectangle([cx, 490, cx + 50, 540], fill="#9C6644", outline="#7F5539", width=2)
        for fx in range(cx + 8, cx + 45, 12):
            for fy in range(500, 535, 12):
                draw.ellipse([fx, fy, fx + 10, fy + 10], fill=colors[(cx * 2 + fx + fy) % len(colors)])

    # Subtle Market Visitors (Silhouette and shapes)
    for px, py in [(550, 420), (600, 410), (450, 430), (660, 425)]:
        draw.ellipse([px, py, px + 22, py + 22], fill="#264653")
        draw.rectangle([px - 5, py + 22, px + 27, py + 95], fill="#1D3557")

    # Banner / Label
    draw.rectangle([420, 40, 780, 100], fill=(0, 0, 0, 160))
    draw.text((450, 55), "FRESH COMMUNITY MARKET", fill="#FFFFFF")

    im.save(output_dir / "street_market.jpg", quality=92)
    print("Generated street_market.jpg")

def create_tech_scene():
    im = Image.new("RGB", (width, height), "#1E293B")
    draw = ImageDraw.Draw(im)

    # Office Floor & Walls
    for y in range(480, height):
        factor = (y - 480) / (height - 480)
        c = int(50 + 30 * factor)
        draw.line([(0, y), (width, y)], fill=(c, c + 5, c + 15))

    # Glass Window / Wall with city skyline
    draw.rectangle([100, 60, 700, 450], fill="#0F172A", outline="#334155", width=4)
    # City silhouettes
    for bx in range(120, 680, 55):
        bh = 100 + (bx * 37) % 200
        draw.rectangle([bx, 450 - bh, bx + 45, 450], fill="#1E293B")
        for wy in range(450 - bh + 15, 430, 25):
            draw.rectangle([bx + 8, wy, bx + 18, wy + 12], fill="#FEF08A")
            draw.rectangle([bx + 26, wy, bx + 36, wy + 12], fill="#93C5FD")

    # Glass Whiteboard on right
    draw.rectangle([760, 80, 1140, 450], fill="#334155", outline="#64748B", width=3)
    # Sticky notes on whiteboard
    note_colors = ["#FEF08A", "#FBCFE8", "#BAE6FD", "#BBF7D0", "#FED7AA"]
    for i, (nx, ny) in enumerate([(800, 120), (870, 120), (940, 120), (1010, 120), 
                                 (800, 190), (870, 190), (940, 190), (1010, 190),
                                 (830, 270), (900, 270), (980, 270)]):
        draw.rectangle([nx, ny, nx + 50, ny + 50], fill=note_colors[i % len(note_colors)])
        draw.line([(nx + 5, ny + 15), (nx + 45, ny + 15)], fill="#475569", width=2)
        draw.line([(nx + 5, ny + 25), (nx + 35, ny + 25)], fill="#475569", width=2)

    # Modern Conference Wooden Desk
    draw.polygon([(200, 480), (1000, 480), (1150, 750), (50, 750)], fill="#854D0E", outline="#713F12", width=3)
    draw.rectangle([50, 750, 1150, 790], fill="#713F12")

    # Laptops on desk
    for lx, ly in [(250, 540), (520, 520), (820, 550)]:
        # Base
        draw.polygon([(lx - 15, ly + 60), (lx + 85, ly + 60), (lx + 95, ly + 75), (lx - 25, ly + 75)], fill="#94A3B8")
        # Screen
        draw.rectangle([lx - 10, ly, lx + 80, ly + 60], fill="#0284C7", outline="#CBD5E1", width=2)
        # Mock IDE lines
        draw.line([(lx, ly + 15), (lx + 60, ly + 15)], fill="#F8FAFC", width=2)
        draw.line([(lx + 10, ly + 25), (lx + 50, ly + 25)], fill="#38BDF8", width=2)
        draw.line([(lx + 10, ly + 35), (lx + 70, ly + 35)], fill="#4ADE80", width=2)

    # Ceramic Coffee Mugs & Notebooks
    for mx, my in [(420, 620), (740, 600)]:
        draw.ellipse([mx, my, mx + 25, my + 15], fill="#E2E8F0")
        draw.rectangle([mx, my + 8, mx + 25, my + 30], fill="#CBD5E1")
    draw.rectangle([340, 650, 460, 730], fill="#38BDF8", outline="#0284C7", width=2)

    # Collaborative Workers (Stylized professional silhouettes)
    for px, py, color in [(180, 430, "#0F766E"), (480, 400, "#4338CA"), (850, 420, "#9A3412")]:
        draw.ellipse([px + 20, py - 40, px + 60, py], fill="#FBBF24")
        draw.polygon([(px, py + 120), (px + 20, py), (px + 60, py), (px + 80, py + 120)], fill=color)

    # Title label
    draw.rectangle([400, 30, 800, 80], fill=(15, 23, 42, 200))
    draw.text((430, 45), "AGILE ENGINEERING WORKSPACE", fill="#38BDF8")

    im.save(output_dir / "tech_collaboration.jpg", quality=92)
    print("Generated tech_collaboration.jpg")

def create_nature_scene():
    im = Image.new("RGB", (width, height), "#38BDF8")
    draw = ImageDraw.Draw(im)

    # Sky gradient
    for y in range(350):
        r = int(56 + (224 - 56) * (y / 350))
        g = int(189 + (242 - 189) * (y / 350))
        b = int(248 + (254 - 248) * (y / 350))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Distant Mountains with Snow
    mountains = [
        [(0, 350), (200, 140), (420, 350)],
        [(300, 350), (550, 100), (800, 350)],
        [(650, 350), (920, 120), (1200, 350)]
    ]
    for pts in mountains:
        draw.polygon(pts, fill="#475569")
        # Snow cap
        peak_x, peak_y = pts[1]
        draw.polygon([(peak_x - 50, peak_y + 70), (peak_x, peak_y), (peak_x + 50, peak_y + 70)], fill="#F8FAFC")

    # Midground Pine Forest
    for tx in range(0, width, 25):
        th = 60 + (tx * 17) % 50
        draw.polygon([(tx - 20, 420), (tx, 420 - th), (tx + 20, 420)], fill="#14532D")
        draw.polygon([(tx - 15, 430), (tx, 430 - th + 15), (tx + 15, 430)], fill="#166534")

    # Alpine Turquoise Lake
    for y in range(430, height):
        factor = (y - 430) / (height - 430)
        r = int(13 + (15 - 13) * factor)
        g = int(148 + (118 - 148) * factor)
        b = int(136 + (110 - 136) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Water reflection of mountains (inverted subtle)
    for pts in mountains:
        peak_x, peak_y = pts[1]
        refl_y = 430 + (350 - peak_y) * 0.45
        draw.polygon([(pts[0][0], 430), (peak_x, refl_y), (pts[2][0], 430)], fill=(20, 110, 105, 100))

    # Shoreline with river rocks
    for rx in range(0, width, 40):
        rw = 30 + (rx % 25)
        rh = 15 + (rx % 12)
        draw.ellipse([rx, height - 60, rx + rw, height - 60 + rh], fill="#64748B", outline="#475569")

    # Header label
    draw.rectangle([420, 30, 780, 80], fill=(15, 23, 42, 160))
    draw.text((450, 45), "ALPINE MOUNTAIN WILDERNESS", fill="#E2E8F0")

    im.save(output_dir / "nature_wildlife.jpg", quality=92)
    print("Generated nature_wildlife.jpg")

def create_classroom_scene():
    im = Image.new("RGB", (width, height), "#0F172A")
    draw = ImageDraw.Draw(im)

    # Ceiling & Acoustic panels
    for x in range(50, width, 140):
        draw.rectangle([x, 20, x + 110, 80], fill="#334155", outline="#475569", width=2)
        draw.line([(x + 55, 80), (x + 55, 110)], fill="#E2E8F0", width=2)
        draw.ellipse([x + 45, 110, x + 65, 120], fill="#FEF08A")

    # Large Dual Projection Presentation Screens
    draw.rectangle([150, 130, 580, 370], fill="#1E293B", outline="#60A5FA", width=4)
    draw.rectangle([620, 130, 1050, 370], fill="#1E293B", outline="#60A5FA", width=4)

    # Technical diagram on left screen
    draw.ellipse([250, 200, 350, 300], outline="#38BDF8", width=3)
    draw.line([(350, 250), (450, 220)], fill="#4ADE80", width=4)
    draw.line([(450, 220), (510, 290)], fill="#F472B6", width=4)
    draw.text((180, 150), "ROBOTIC KINEMATICS & CONTROL", fill="#93C5FD")

    # Mathematical formulas on right screen
    draw.text((650, 160), "Inverse Kinematics: theta = atan2(y, x)", fill="#FDE047")
    draw.text((650, 210), "Jacobian Matrix: J(q) * dq/dt = v", fill="#FDE047")
    draw.text((650, 260), "PID Torque: tau = Kp*e + Kd*de/dt", fill="#38BDF8")

    # Professor at Podium
    draw.rectangle([520, 340, 680, 460], fill="#64748B", outline="#334155", width=3)
    draw.ellipse([580, 300, 620, 340], fill="#FBBF24")
    draw.rectangle([570, 340, 630, 440], fill="#0284C7")
    # Extended arm gesturing to screen
    draw.line([(630, 360), (700, 320)], fill="#0284C7", width=6)

    # Tiered Student Desks (Rows ascending)
    tiers = [
        (480, "#475569", [(250, 460), (400, 460), (750, 460), (900, 460)]),
        (580, "#334155", [(180, 550), (320, 550), (460, 550), (680, 550), (820, 550), (980, 550)]),
        (680, "#1E293B", [(120, 650), (260, 650), (400, 650), (540, 650), (720, 650), (860, 650), (1020, 650)])
    ]
    for ty, desk_color, students in tiers:
        draw.rectangle([0, ty, width, ty + 40], fill=desk_color, outline="#64748B", width=2)
        for sx, sy in students:
            # Student silhouette
            draw.ellipse([sx, sy - 30, sx + 30, sy], fill="#FBBF24")
            draw.rectangle([sx - 8, sy, sx + 38, sy + 60], fill="#3B82F6")
            # Open laptop on desk
            draw.rectangle([sx, ty + 5, sx + 28, ty + 25], fill="#E2E8F0")

    draw.rectangle([400, 20, 800, 70], fill=(15, 23, 42, 220))
    draw.text((430, 35), "INTERACTIVE ROBOTICS LECTURE", fill="#F8FAFC")

    im.save(output_dir / "classroom_lecture.jpg", quality=92)
    print("Generated classroom_lecture.jpg")

create_market_scene()
create_tech_scene()
create_nature_scene()
create_classroom_scene()
print("All 4 showcase images successfully generated!")
