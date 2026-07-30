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

def create_tweak_og_image(pkg_id, meta):
    W, H = 1200, 630
    
    # Solid dark gradient background
    base = Image.new("RGBA", (W, H), (11, 15, 25, 255))
    draw = ImageDraw.Draw(base)
    
    for y in range(H):
        r = int(11 + (20 - 11) * (y / H))
        g = int(15 + (24 - 15) * (y / H))
        b = int(25 + (40 - 25) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Glowing radial gradient overlay in center-left
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(400, 0, -5):
        alpha = int(30 * (1 - r / 400))
        glow_draw.ellipse([300 - r, 315 - r, 300 + r, 315 + r], fill=(0, 122, 255, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, glow)

    # Fonts
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        font_desc = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
        font_meta = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        font_brand = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_meta = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # Load Preview/Banner Image or Icon
    banner_path = f"depictions/{pkg_id}/banner.png"
    icon_path = f"depictions/{pkg_id}/icon.png"
    if not os.path.exists(icon_path):
        icon_path = "favicon-96x96.png"

    # 1. Preview Card on Left Side
    card_w, card_h = 440, 440
    card_x, card_y = 70, 95
    
    if os.path.exists(banner_path):
        prev_im = Image.open(banner_path).convert("RGBA")
        # Fit into card container
        prev_im.thumbnail((card_w, card_h), Image.Resampling.LANCZOS)
        prev_w, prev_h = prev_im.size
        prev_rounded = make_rounded(prev_im, 20)
        
        # Center inside preview area
        px = card_x + (card_w - prev_w) // 2
        py = card_y + (card_h - prev_h) // 2
        
        # Border
        border_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(border_overlay)
        b_draw.rounded_rectangle([px - 3, py - 3, px + prev_w + 3, py + prev_h + 3], radius=23, outline=(255, 255, 255, 60), width=2)
        base = Image.alpha_composite(base, border_overlay)
        base.paste(prev_rounded, (px, py), prev_rounded)
    else:
        # Fallback icon preview
        prev_im = Image.open(icon_path).convert("RGBA").resize((240, 240), Image.Resampling.LANCZOS)
        prev_rounded = make_rounded(prev_im, 32)
        px = card_x + (card_w - 240) // 2
        py = card_y + (card_h - 240) // 2
        base.paste(prev_rounded, (px, py), prev_rounded)

    # 2. Right Side Details
    text_x = 560
    text_y = 110

    draw = ImageDraw.Draw(base)

    # Brand Header (NekosofTech Repo)
    fav_im = Image.open("favicon-96x96.png").convert("RGBA").resize((36, 36), Image.Resampling.LANCZOS)
    fav_rounded = make_rounded(fav_im, 8)
    base.paste(fav_rounded, (text_x, text_y), fav_rounded)
    draw.text((text_x + 48, text_y + 6), "NekosofTech Repo", fill=(0, 122, 255, 255), font=font_brand)

    # Tweak Title
    title = meta["name"]
    draw.text((text_x, text_y + 65), title, fill=(255, 255, 255, 255), font=font_title)

    # Tweak Description (word wrap if needed)
    desc = meta["description"]
    # Wrap text manually
    words = desc.split(" ")
    lines = []
    curr_line = ""
    for w in words:
        test_line = f"{curr_line} {w}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_desc)
        if (bbox[2] - bbox[0]) < 560:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)

    desc_y = text_y + 140
    for l in lines[:3]:
        draw.text((text_x, desc_y), l, fill=(203, 213, 225, 255), font=font_desc)
        desc_y += 32

    # Metadata Pills (Compatibility & Price)
    pill_y = H - 150
    comp_text = f"iOS: {meta['compatibility']}"
    
    pill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pill_overlay)
    
    # Compatibility pill
    bbox_comp = draw.textbbox((0, 0), comp_text, font=font_meta)
    pw = (bbox_comp[2] - bbox_comp[0]) + 28
    p_draw.rounded_rectangle([text_x, pill_y, text_x + pw, pill_y + 38], radius=12, fill=(255, 255, 255, 18), outline=(255, 255, 255, 35), width=1)
    
    # Free badge pill
    free_x = text_x + pw + 12
    p_draw.rounded_rectangle([free_x, pill_y, free_x + 80, pill_y + 38], radius=12, fill=(0, 122, 255, 40), outline=(0, 122, 255, 100), width=1)
    
    base = Image.alpha_composite(base, pill_overlay)

    draw = ImageDraw.Draw(base)
    draw.text((text_x + 14, pill_y + 8), comp_text, fill=(241, 245, 249, 255), font=font_meta)
    draw.text((free_x + 18, pill_y + 8), "FREE", fill=(56, 189, 248, 255), font=font_meta)

    # Footer link
    draw.text((text_x, H - 70), "https://nekosoftech.github.io/repo/", fill=(100, 116, 139, 255), font=font_meta)

    # Convert to RGB (Solid, 0% transparency)
    final_image = base.convert("RGB")
    
    out_dir = f"package/{pkg_id}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/og.png"
    final_image.save(out_path, "PNG")
    print(f"Generated solid OG preview: {out_path}")

if __name__ == "__main__":
    from build_repo import PACKAGES_META
    for pkg_id, meta in PACKAGES_META.items():
        create_tweak_og_image(pkg_id, meta)
