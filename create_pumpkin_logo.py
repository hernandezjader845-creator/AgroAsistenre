import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_glass_pumpkin(size=1024, output_path="assets/logo_calabaza_glassmorphism.png"):
    # Canvas with alpha
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Scale factor
    scale = size / 1000.0
    
    # Dimensions and centers
    cx, cy = size / 2.0, size * 0.54
    w, h = 380 * scale, 290 * scale
    
    # We will build layers:
    # 1. Shadow Layer (soft drop shadow)
    # 2. Translucent Glass Body (layered lobes with frosted gradients)
    # 3. Relief Lines (inner grooves with specular highlights)
    # 4. Glass Rim / Border (crisp frosted bevel)
    # 5. Stem (glass stem with contour)
    
    # --- Helper to draw smooth polygon lobes ---
    # Center lobe:
    # Left inner lobe:
    # Right inner lobe:
    # Left outer lobe:
    # Right outer lobe:
    
    # High-resolution supersampling canvas (2x)
    ss = 2
    sw, sh = size * ss, size * ss
    scx, scy = cx * ss, cy * ss
    
    # Shadow canvas
    shadow_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    
    # Body canvas (translucent glass)
    body_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    body_draw = ImageDraw.Draw(body_img)
    
    # Relief lines canvas
    lines_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    lines_draw = ImageDraw.Draw(lines_img)
    
    # Stem canvas
    stem_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    stem_draw = ImageDraw.Draw(stem_img)
    
    # --- Define Pumpkin Lobes (Bezier-like sampling) ---
    # Lobes configuration: (x_offset, width_factor, height_factor, y_offset)
    lobes = [
        # Outer left
        (-260 * scale * ss, 140 * scale * ss, 220 * scale * ss, 20 * scale * ss),
        # Outer right
        (260 * scale * ss, 140 * scale * ss, 220 * scale * ss, 20 * scale * ss),
        # Mid left
        (-150 * scale * ss, 180 * scale * ss, 260 * scale * ss, 10 * scale * ss),
        # Mid right
        (150 * scale * ss, 180 * scale * ss, 260 * scale * ss, 10 * scale * ss),
        # Center
        (0 * scale * ss, 210 * scale * ss, 280 * scale * ss, 0)
    ]
    
    # 1. DRAW SHADOW
    # Draw dark green-tinted shadow beneath the pumpkin
    shadow_y_offset = 35 * scale * ss
    for l_x, l_w, l_h, l_y in lobes:
        bbox = (
            scx + l_x - l_w,
            scy + l_y - l_h + shadow_y_offset,
            scx + l_x + l_w,
            scy + l_y + l_h + shadow_y_offset
        )
        shadow_draw.ellipse(bbox, fill=(16, 45, 25, 95))
        
    # Blur shadow
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=28 * scale * ss))
    
    # 2. DRAW TRANSLUCENT GLASS BODY
    # We want a subtle, elegant frosted glass fill:
    # Alpha around 70-110 (translucent, lets background breathe through!)
    for l_x, l_w, l_h, l_y in lobes:
        bbox = (
            scx + l_x - l_w,
            scy + l_y - l_h,
            scx + l_x + l_w,
            scy + l_y + l_h
        )
        # Translucent glass fill with fresh mint/white tone
        body_draw.ellipse(bbox, fill=(245, 252, 246, 85))
        
    # Add a soft vertical gradient of light to give frosted glass vibrancy
    gradient_mask = Image.new("L", (sw, sh), 0)
    g_draw = ImageDraw.Draw(gradient_mask)
    for y in range(int(scy - 300 * scale * ss), int(scy + 300 * scale * ss)):
        # Brighter at top edge, translucent in middle
        ratio = (y - (scy - 300 * scale * ss)) / (600 * scale * ss)
        val = int(120 * (1 - ratio * 0.6))
        g_draw.line([(0, y), (sw, y)], fill=max(20, min(255, val)))
        
    glass_glow = Image.new("RGBA", (sw, sh), (255, 255, 255, 0))
    # Apply glow mask to body
    
    # 3. DRAW STEM (Tallo elegante)
    # Stem points
    stem_pts = [
        (scx - 22 * scale * ss, scy - 250 * scale * ss),
        (scx - 10 * scale * ss, scy - 310 * scale * ss),
        (scx + 25 * scale * ss, scy - 380 * scale * ss),
        (scx + 75 * scale * ss, scy - 420 * scale * ss),
        (scx + 95 * scale * ss, scy - 400 * scale * ss),
        (scx + 50 * scale * ss, scy - 340 * scale * ss),
        (scx + 25 * scale * ss, scy - 290 * scale * ss),
        (scx + 22 * scale * ss, scy - 250 * scale * ss)
    ]
    stem_draw.polygon(stem_pts, fill=(230, 245, 232, 130))
    # Stem contour
    stem_draw.line(stem_pts + [stem_pts[0]], fill=(18, 48, 27, 220), width=int(6 * scale * ss))
    stem_draw.line(stem_pts + [stem_pts[0]], fill=(255, 255, 255, 200), width=int(2 * scale * ss))

    # 4. DRAW CRISP RELIEF LINES (Las líneas de los relieves)
    # Each groove is drawn with a dual-stroke:
    # - Darker subtle shadow line (groove depth)
    # - Bright specular highlight line alongside it (ridge crest reflection)
    # This creates the exact "relief" the user requested without looking 3D heavy!
    
    grooves = []
    
    # Left inner groove
    pts_l1 = []
    # Left outer groove
    pts_l2 = []
    # Right inner groove
    pts_r1 = []
    # Right outer groove
    pts_r2 = []
    
    steps = 60
    top_y = scy - 270 * scale * ss
    bot_y = scy + 270 * scale * ss
    
    for i in range(steps + 1):
        t = i / steps
        y = top_y + t * (bot_y - top_y)
        # Parabolic bulge
        bulge = math.sin(t * math.pi)
        
        # Inner left curve
        xl1 = scx - 15 * scale * ss - bulge * (125 * scale * ss)
        pts_l1.append((xl1, y))
        
        # Outer left curve
        xl2 = scx - 22 * scale * ss - bulge * (245 * scale * ss)
        pts_l2.append((xl2, y - bulge * (15 * scale * ss)))
        
        # Inner right curve
        xr1 = scx + 15 * scale * ss + bulge * (125 * scale * ss)
        pts_r1.append((xr1, y))
        
        # Outer right curve
        xr2 = scx + 22 * scale * ss + bulge * (245 * scale * ss)
        pts_r2.append((xr2, y - bulge * (15 * scale * ss)))

    grooves = [pts_l2, pts_l1, pts_r1, pts_r2]
    
    for g_pts in grooves:
        # A. Shadow / Depth groove stroke (dark botanical green, crisp)
        lines_draw.line(g_pts, fill=(16, 45, 25, 200), width=int(7 * scale * ss))
        # B. Specular highlight stroke (shifted 1px right/up for light direction)
        g_highlight = [(px + 2 * scale * ss, py - 1 * scale * ss) for px, py in g_pts]
        lines_draw.line(g_highlight, fill=(255, 255, 255, 240), width=int(3 * scale * ss))

    # 5. DRAW OUTER CONTOUR / RIM BEVEL
    # The outer boundary of the pumpkin lobes with crisp edge definition
    for l_x, l_w, l_h, l_y in lobes:
        bbox = (
            scx + l_x - l_w,
            scy + l_y - l_h,
            scx + l_x + l_w,
            scy + l_y + l_h
        )
        # Subtle outer dark definition
        lines_draw.ellipse(bbox, outline=(16, 45, 25, 170), width=int(6 * scale * ss))
        # Inner bright specular rim
        bbox_in = (
            scx + l_x - l_w + 2 * scale * ss,
            scy + l_y - l_h + 2 * scale * ss,
            scx + l_x + l_w - 2 * scale * ss,
            scy + l_y + l_h - 2 * scale * ss
        )
        lines_draw.ellipse(bbox_in, outline=(255, 255, 255, 220), width=int(3 * scale * ss))

    # Center vertical subtle crease
    pts_center = [(scx, top_y + t * (bot_y - top_y)) for t in [i/30.0 for i in range(31)]]
    lines_draw.line(pts_center, fill=(16, 45, 25, 90), width=int(4 * scale * ss))
    lines_draw.line([(px + 1 * scale * ss, py) for px, py in pts_center], fill=(255, 255, 255, 140), width=int(2 * scale * ss))

    # --- COMPOSITING ---
    final_ss = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    final_ss.alpha_composite(shadow_img)
    final_ss.alpha_composite(body_img)
    final_ss.alpha_composite(stem_img)
    final_ss.alpha_composite(lines_img)
    
    # Downsample with Lanczos for super-crisp, anti-aliased finish
    final_img = final_ss.resize((size, size), Image.Resampling.LANCZOS)
    
    # Ensure dir exists and save
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        
    final_img.save(output_path, "PNG", optimize=True)
    print(f"Created glass pumpkin icon at: {output_path} ({size}x{size})")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "assets", "logo_calabaza_glassmorphism.png")
    create_glass_pumpkin(1024, target)
