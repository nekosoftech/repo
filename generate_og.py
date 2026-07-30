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
    
    # Create dark gradient background
    base = Image.new("RGBA", (W, H), (11, 15, 25, 255))
    draw = ImageDraw.Draw(base)
    
    # Gradient background
    for y in range(H):
        r = int(11 + (20 - 11) * (y / H))
        g = int(15 + (24 - 15) * (y / H))
        b = int(25 + (40 - 25) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Add a glowing radial gradient overlay in center
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    center_x, center_y = W // 2, H // 2 - 40
    for r in range(350, 0, -5):
        alpha = int(35 * (1 - r / 350))
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(0, 122, 255, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, glow)

    # Re-obtain draw object
    draw = ImageDraw.Draw(base)

    # 1. Main Logo (favicon-96x96.png)
    fav_path = "favicon-96x96.png"
    if not os.path.exists(fav_path):
        fav_path = "apple-touch-icon.png"
    
    logo_size = 110
    logo_im = Image.open(fav_path).convert("RGBA").resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_rounded = make_rounded(logo_im, 24)
    
    # Logo container shadow & border
    logo_x = (W - logo_size) // 2
    logo_y = 90
    
    # Border
    draw.rounded_rectangle([logo_x - 3, logo_y - 3, logo_x + logo_size + 3, logo_y + logo_size + 3], radius=27, outline=(255, 255, 255, 40), width=2)
    base.paste(logo_rounded, (logo_x, logo_y), logo_rounded)

    # Load system/default font
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

    # Bottom 3 icons: SileoIcon, ZebraIcon, CydiaIcon
    icon_paths = [
        ("logo/SileoIcon.png", "Sileo"),
        ("logo/ZebraIcon.png", "Zebra"),
        ("logo/CydiaIcon.png", "Cydia")
    ]

    card_w, card_h = 480, 90
    card_x = (W - card_w) // 2
    card_y = H - 165

    # Glass container for 3 icons
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(255, 255, 255, 12), outline=(255, 255, 255, 25), width=1)

    # Place icons inside container
    item_w = card_w // 3
    icon_dim = 44
    for idx, (ipath, iname) in enumerate(icon_paths):
        ix = card_x + idx * item_w + (item_w - (icon_dim + 60)) // 2
        iy = card_y + (card_h - icon_dim) // 2
        
        if os.path.exists(ipath):
            ic_im = Image.open(ipath).convert("RGBA").resize((icon_dim, icon_dim), Image.Resampling.LANCZOS)
            ic_rounded = make_rounded(ic_im, 10)
            base.paste(ic_rounded, (ix, iy), ic_rounded)
            
        draw.text((ix + icon_dim + 12, iy + 12), iname, fill=(241, 245, 249, 230), font=font_badge)

    # Footer text
    foot_text = "https://nekosoftech.com"
    bbox_foot = draw.textbbox((0, 0), foot_text, font=font_footer)
    fw = bbox_foot[2] - bbox_foot[0]
    draw.text(((W - fw) // 2, H - 45), foot_text, fill=(100, 116, 139, 255), font=font_footer)

    os.makedirs("logo", exist_ok=True)
    base.save("logo/og_background.png", "PNG")
    print("Successfully generated logo/og_background.png")

if __name__ == "__main__":
    create_og_background()
