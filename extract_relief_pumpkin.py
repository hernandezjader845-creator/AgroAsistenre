import numpy as np
from PIL import Image, ImageFilter

def extract_pumpkin():
    src_path = "C:/Users/usuario/.gemini/antigravity/brain/b4b702e5-a4cc-4d77-a0e3-3f97fd1625ca/glass_pumpkin_relief_1790897305004.jpg"
    out_path = "C:/antigravity 1/.agents/skills/precision-agriculture/scripts/fitosanitario/assets/logo_calabaza_glassmorphism.png"
    out_icon_path = "C:/antigravity 1/.agents/skills/precision-agriculture/scripts/fitosanitario/assets/logo_calabaza_icon.png"
    
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    arr = np.array(img, dtype=np.float32)
    
    # Also save the complete squircle as the app icon!
    img.save(out_icon_path, "PNG")
    print("Saved app icon squircle to:", out_icon_path)
    
    # Now let's extract the pumpkin from inside the squircle:
    # Inside the squircle, the squircle background color is around:
    # (210, 230, 215) to (225, 240, 228)
    # The pumpkin has a white rim (245, 255, 248) and a shadow underneath (150, 185, 160)
    
    # Crop central area where pumpkin is located
    # Pumpkin center is roughly (512, 500)
    # Let's crop from (180, 160) to (840, 800)
    crop_area = (160, 140, 864, 844)
    cropped = img.crop(crop_area)
    cw, ch = cropped.size
    
    # We want a transparent background outside the pumpkin and its shadow.
    # The squircle surface around the pumpkin is roughly:
    # r: 215-225, g: 232-242, b: 218-228
    c_arr = np.array(cropped, dtype=np.float32)
    
    # Sample squircle color from the corners of cropped
    corners = [c_arr[15, 15], c_arr[15, cw-15], c_arr[ch-15, 15], c_arr[ch-15, cw-15]]
    sq_bg = np.mean(corners, axis=0)
    print("Squircle background color:", sq_bg)
    
    # Color distance from squircle surface
    diff = np.sqrt(np.sum((c_arr - sq_bg) ** 2, axis=2))
    
    # The pumpkin and its shadow have diff > threshold
    # Shadow is darker (diff ~ 15-40), pumpkin is brighter/white (diff ~ 20-80)
    # We create a smooth alpha mask
    alpha = np.clip((diff - 6.0) / 18.0, 0.0, 1.0)
    
    # Clean edges with slight blur on alpha
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=1.5))
    
    # Create final RGBA image
    r = cropped.getchannel("R")
    g = cropped.getchannel("G")
    b = cropped.getchannel("B")
    
    final_rgba = Image.merge("RGBA", (r, g, b, alpha_img))
    
    # Resize to clean 1024x1024 with transparent margins
    target_canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    # Resize cropped to 880x880 and center
    resized = final_rgba.resize((860, 860), Image.Resampling.LANCZOS)
    target_canvas.paste(resized, (82, 82), mask=resized)
    
    target_canvas.save(out_path, "PNG", optimize=True)
    print("Saved transparent relief pumpkin to:", out_path)

if __name__ == "__main__":
    extract_pumpkin()
