import os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

def process_original_pumpkin():
    src_path = "C:/Users/usuario/.gemini/antigravity/brain/b4b702e5-a4cc-4d77-a0e3-3f97fd1625ca/glass_pumpkin_logo_1790889872947.jpg"
    out_path = "C:/antigravity 1/.agents/skills/precision-agriculture/scripts/fitosanitario/assets/logo_calabaza_glassmorphism.png"
    
    if not os.path.exists(src_path):
        print(f"Error: {src_path} does not exist")
        return
        
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # 1. Background color detection (corners)
    arr = np.array(img, dtype=np.float32)
    bg_color = np.mean([arr[10, 10], arr[10, w-10], arr[h-10, 10], arr[h-10, w-10]], axis=0)
    print("Detected background color:", bg_color)
    
    # Compute distance from background color
    diff = np.sqrt(np.sum((arr - bg_color) ** 2, axis=2))
    
    # Mask creation
    # Pumpkin is light grey/white, background is dark ~50
    # Thresholding
    thresh_low = 18.0
    thresh_high = 38.0
    
    alpha = np.clip((diff - thresh_low) / (thresh_high - thresh_low), 0.0, 1.0)
    
    # Enhance the interior relief lines:
    # Convert image to grayscale to detect the grooves inside the pumpkin
    gray = img.convert("L")
    
    # Edge filter to find the vertical relief grooves
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges_arr = np.array(edges, dtype=np.float32)
    
    # In the original pumpkin, the relief lines are darker creases flanked by light specular lines.
    # Let's extract the pumpkin interior
    # Adjust luminance: Make the pumpkin glass body more translucent (lower opacity in the middle)
    # while boosting the rim highlight and relief lines!
    
    # Create final RGBA image
    # We want:
    # 1. Translucent glass body: alpha around 110-140 where pumpkin exists
    # 2. Specular outer rim: alpha up to 255 (bright white)
    # 3. Relief lines: enhanced with crisp contrast
    # 4. Floating drop shadow beneath
    
    # Let's calculate brightness
    brightness = np.mean(arr, axis=2) / 255.0
    
    # Create RGBA channels
    # Body color: pristine frosted white with subtle sage tint (240, 248, 242)
    r_chan = np.full((h, w), 245, dtype=np.uint8)
    g_chan = np.full((h, w), 252, dtype=np.uint8)
    b_chan = np.full((h, w), 246, dtype=np.uint8)
    
    # Modulate color based on original shading so it retains its natural frosted glass highlights
    norm_orig = np.clip((arr - 45.0) / 160.0, 0.0, 1.0)
    r_chan = np.clip(180 + norm_orig[:, :, 0] * 75, 0, 255).astype(np.uint8)
    g_chan = np.clip(195 + norm_orig[:, :, 1] * 60, 0, 255).astype(np.uint8)
    b_chan = np.clip(185 + norm_orig[:, :, 2] * 70, 0, 255).astype(np.uint8)
    
    # Base alpha: translucent body (~110) but opaque on specular rims (~255)
    # We use brightness of the original to give more alpha to the shiny edges
    body_alpha = alpha * (90 + norm_orig[:, :, 0] * 140)
    
    # Enhance relief lines:
    # High-pass filter on gray image to find the grooves
    gray_arr = np.array(gray, dtype=np.float32)
    blurred = np.array(gray.filter(ImageFilter.GaussianBlur(radius=4)), dtype=np.float32)
    groove_detail = blurred - gray_arr  # Positive where there's a dark groove!
    
    # Where groove_detail > 3, it's a relief line!
    # Darken the relief lines and make them super defined
    groove_mask = np.clip((groove_detail - 2.0) / 10.0, 0.0, 1.0) * alpha
    
    # Apply groove darkening
    r_chan = np.clip(r_chan * (1.0 - groove_mask * 0.55), 0, 255).astype(np.uint8)
    g_chan = np.clip(g_chan * (1.0 - groove_mask * 0.45), 0, 255).astype(np.uint8)
    b_chan = np.clip(b_chan * (1.0 - groove_mask * 0.55), 0, 255).astype(np.uint8)
    # Boost alpha along relief lines so they are sharp and visible
    body_alpha = np.clip(body_alpha + groove_mask * 90, 0, 255)
    
    # Assemble pumpkin layer
    pumpkin_layer = Image.merge("RGBA", (
        Image.fromarray(r_chan),
        Image.fromarray(g_chan),
        Image.fromarray(b_chan),
        Image.fromarray(body_alpha.astype(np.uint8))
    ))
    
    # Create Shadow Layer
    # Smooth silhouette mask
    sil_mask = Image.fromarray((alpha * 255).astype(np.uint8))
    # Erode slightly and blur heavily for drop shadow
    shadow = Image.new("RGBA", (w, h), (14, 40, 22, 0))
    shadow_fill = Image.new("RGBA", (w, h), (14, 40, 22, 130))
    shadow.paste(shadow_fill, (0, int(h * 0.028)), mask=sil_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Sharper ambient shadow near base
    shadow2 = Image.new("RGBA", (w, h), (14, 40, 22, 0))
    shadow2_fill = Image.new("RGBA", (w, h), (14, 40, 22, 90))
    shadow2.paste(shadow2_fill, (0, int(h * 0.012)), mask=sil_mask)
    shadow2 = shadow2.filter(ImageFilter.GaussianBlur(radius=8))
    
    # Composite all layers
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.alpha_composite(shadow)
    result.alpha_composite(shadow2)
    result.alpha_composite(pumpkin_layer)
    
    # Crop to bounding box with small margin
    bbox = result.getbbox()
    if bbox:
        # Keep 1:1 aspect ratio
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        side = max(bw, bh) + 40
        cx = (bbox[0] + bbox[2]) // 2
        cy = (bbox[1] + bbox[3]) // 2
        crop_box = (
            max(0, cx - side // 2),
            max(0, cy - side // 2),
            min(w, cx + side // 2),
            min(h, cy + side // 2)
        )
        result = result.crop(crop_box)
        result = result.resize((1024, 1024), Image.Resampling.LANCZOS)
        
    result.save(out_path, "PNG", optimize=True)
    print("Successfully processed and saved enhanced pumpkin to:", out_path)

if __name__ == "__main__":
    process_original_pumpkin()
