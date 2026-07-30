import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_rounded(im, radius):
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, im.size[0], im.size[1]), radius=radius, fill=255)
    result = im.copy()
    result.putalpha(mask)
    return result

def create_og_background():
    W, H = 1200, 630
    
    # 1. Base dark background (Solid RGBA, alpha 255)
    base = Image.new("RGBA", (W, H), (11, 15, 25, 255))
    draw = ImageDraw.Draw(base)
    
    # Smooth dark gradient background
    for y in range(H):
        r = int(11 + (20 - 11) * (y / H))
        g = int(15 + (24 - 15) * (y / H))
        b = int(25 + (40 - 25) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Glowing radial gradient overlay in center
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    center_x, center_y = W // 2, H // 2 - 40
    for r in range(350, 0, -5):
        alpha = int(35 * (1 - r / 350))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 122, 255, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, glow)

    # 3. Main Brand Logo (favicon-96x96.png)
    fav_path = "favicon-96x96.png"
    if not os.path.exists(fav_path):
        fav_path = "apple-touch-icon.png"
    
    logo_size = 110
    logo_im = Image.open(fav_path).convert("RGBA").resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_rounded = make_rounded(logo_im, 24)
    
    logo_x = (W - logo_size) // 2
    logo_y = 85
    
    # Logo subtle glow border
    logo_border_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lb_draw = ImageDraw.Draw(logo_border_overlay)
    lb_draw.rounded_rectangle([logo_x - 3, logo_y - 3, logo_x + logo_size + 3, logo_y + logo_size + 3], radius=27, outline=(255, 255, 255, 60), width=2)
    base = Image.alpha_composite(base, logo_border_overlay)
    base.paste(logo_rounded, (logo_x, logo_y), logo_rounded)

    # 4. Fonts
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
        font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        font_footer = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    draw = ImageDraw.Draw(base)

    # Title: NekosofTech's Repo
    title_text = "NekosofTech's Repo"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, logo_y + logo_size + 24), title_text, fill=(255, 255, 255, 255), font=font_title)

    # Subtitle: Premium iOS Tweak Repository
    sub_text = "Premium iOS Tweak Repository"
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    draw.text(((W - sw) // 2, logo_y + logo_size + 90), sub_text, fill=(148, 163, 184, 255), font=font_sub)

    # 5. Glass Container overlay for 3 icons (composited properly via alpha_composite)
    card_w, card_h = 480, 90
    card_x = (W - card_w) // 2
    card_y = H - 165

    card_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_overlay)
    # Solid dark tint blended over gradient
    card_draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(255, 255, 255, 16), outline=(255, 255, 255, 40), width=1)
    base = Image.alpha_composite(base, card_overlay)

    # 6. Icons inside container
    icon_paths = [
        ("logo/SileoIcon.png", "Sileo"),
        ("logo/ZebraIcon.png", "Zebra"),
        ("logo/CydiaIcon.png", "Cydia")
    ]

    draw = ImageDraw.Draw(base)
    item_w = card_w // 3
    icon_dim = 44
    for idx, (ipath, iname) in enumerate(icon_paths):
        ix = card_x + idx * item_w + (item_w - (icon_dim + 60)) // 2
        iy = card_y + (card_h - icon_dim) // 2
        
        if os.path.exists(ipath):
            ic_im = Image.open(ipath).convert("RGBA").resize((icon_dim, icon_dim), Image.Resampling.LANCZOS)
            ic_rounded = make_rounded(ic_im, 10)
            base.paste(ic_rounded, (ix, iy), ic_rounded)
            
        draw.text((ix + icon_dim + 12, iy + 12), iname, fill=(241, 245, 249, 255), font=font_badge)

    # 7. Footer text
    foot_text = "https://nekosoftech.com"
    bbox_foot = draw.textbbox((0, 0), foot_text, font=font_footer)
    fw = bbox_foot[2] - bbox_foot[0]
    draw.text(((W - fw) // 2, H - 45), foot_text, fill=(100, 116, 139, 255), font=font_footer)

    # Convert to RGB to ensure ZERO transparency cutouts in output file
    final_image = base.convert("RGB")
    
    os.makedirs("logo", exist_ok=True)
    final_image.save("logo/og_background.png", "PNG")
    print("Successfully generated solid logo/og_background.png (RGB)")

if __name__ == "__main__":
    create_og_background()
