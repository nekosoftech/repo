#!/usr/bin/env python3
import os
import json
import gzip
import bz2
import subprocess
import glob
from datetime import datetime

# Master Tweak Catalog with accurate metadata per tweak
PACKAGES_META = {
    "com.hdun9.camaction": {
        "name": "CamAction",
        "description": "Use volume buttons to control camera zoom in the native Camera app.",
        "detailed_description": "CamAction allows you to effortlessly control camera zoom using physical hardware volume buttons inside the native iOS Camera app. Easily adjust zoom levels while taking photos or recording video.",
        "compatibility": "iOS 14.0 - 17.x (Rootless / Rootful)",
        "min_ios": "14.0",
        "version": "2.2.0-1+debug",
        "developer": "DAN9",
        "section": "Tweaks",
        "features": [
            "Use physical volume buttons for smooth camera zoom",
            "Seamless native integration with iOS Camera app",
            "Lightweight, fast, and battery friendly",
            "Compatible with Rootless & Rootful jailbreaks"
        ],
        "deb_file": "debs/com.hdun9.camaction_2.2.0-1+debug_iphoneos-arm64.deb"
    },
    "com.hdun9.homeaction": {
        "name": "Home Action",
        "description": "Hold Volume Down for 2s to trigger custom actions.",
        "detailed_description": "Home Action allows you to assign custom system shortcuts to a 2-second press of the Volume Down button. Choose between toggling Silent Mode, Do Not Disturb, Flashlight, Voice Memo, or Magnifier.",
        "compatibility": "iOS 14.0 - 17.x (Rootless / Rootful)",
        "min_ios": "14.0",
        "version": "1.0.2-4+debug",
        "developer": "DAN9",
        "section": "Tweaks",
        "features": [
            "Hold Volume Down for 2 seconds to activate custom action",
            "Supports Silent Mode, DND, Flashlight, Voice Memos & Magnifier",
            "Customizable settings panel via PreferenceLoader",
            "Optimized for iOS 14.0 - 17.x"
        ],
        "deb_file": "debs/com.hdun9.homeaction_1.0.2-4+debug_iphoneos-arm64.deb"
    },
    "com.hdun9.privacydisplay": {
        "name": "Privacy Display",
        "description": "Automatically hides screen content when device is tilted using gyroscope roll detection.",
        "detailed_description": "Privacy Display keeps your personal conversations and app content private in public places. Powered by real-time iPhone gyroscope roll detection, it automatically dims or hides your screen when your device is tilted past a customizable angle.",
        "compatibility": "iOS 14.0 - 17.x (Rootless / Rootful)",
        "min_ios": "14.0",
        "version": "1.0.0-4+debug",
        "developer": "DAN9",
        "section": "Tweaks",
        "features": [
            "Automatic screen dimming/hiding on device tilt",
            "Real-time gyroscope angle sensitivity threshold adjustment",
            "Protect sensitive messaging and bank apps in public",
            "Smooth fade animations and zero background battery drain"
        ],
        "deb_file": "debs/com.hdun9.privacydisplay_1.0.0-4-release_iphoneos-arm64.deb"
    },
    "com.huudung.liquiddynamicisland": {
        "name": "Liquid Island",
        "description": "Native Liquid Glass styling and a settings app for Dynamic Island.",
        "detailed_description": "Liquid Island brings sleek glassmorphism aesthetic and dynamic fluid animations to your Dynamic Island on iOS. Features a full native preferences app to customize island styles, colors, and layout effects.",
        "compatibility": "iOS 16.0 - 17.x (Rootless)",
        "min_ios": "16.0",
        "version": "0.1.0-20+debug",
        "developer": "DAN9",
        "section": "Tweaks",
        "features": [
            "Beautiful Liquid Glass visual styling for Dynamic Island",
            "Dedicated native preferences app for custom colors & styling",
            "Smooth spring physics animations",
            "Built with ElleKit for iOS 16.0+ Rootless jailbreaks"
        ],
        "deb_file": "debs/com.huudung.liquiddynamicisland_0.1.0-20+debug_iphoneos-arm64.deb"
    }
}

REPO_URL = "https://nekosoftech.github.io/repo"

def generate_sileo_depictions():
    """Generates sileo.json and base.json for each package with precise metadata."""
    print("--> Generating Depiction JSONs...")
    for pkg_id, meta in PACKAGES_META.items():
        pkg_dir = f"depictions/{pkg_id}"
        os.makedirs(pkg_dir, exist_ok=True)
        
        # Gather screenshots if any
        screenshots = []
        for file in sorted(os.listdir(pkg_dir)):
            if file.startswith("screenshot") and file.endswith((".png", ".jpg", ".jpeg")):
                screenshots.append({
                    "url": f"{REPO_URL}/depictions/{pkg_id}/{file}",
                    "accessibilityText": f"{meta['name']} Screenshot"
                })

        features_md = "\n".join([f"- {f}" for f in meta["features"]])

        details_views = [
            {
                "class": "DepictionMarkdownView",
                "markdown": f"### Welcome to {meta['name']}\n\n{meta['detailed_description']}",
                "useSpacing": True
            },
            {
                "class": "DepictionSpacerView",
                "spacing": 16
            }
        ]

        if screenshots:
            details_views.append({
                "class": "DepictionScreenshotsView",
                "itemCornerRadius": 10,
                "itemSize": "{160, 346.5}",
                "screenshots": screenshots
            })
            details_views.append({
                "class": "DepictionSpacerView",
                "spacing": 16
            })

        details_views.extend([
            {
                "class": "DepictionHeaderView",
                "title": "Features",
                "useBoldText": True
            },
            {
                "class": "DepictionMarkdownView",
                "markdown": features_md,
                "useSpacing": True
            },
            {
                "class": "DepictionSpacerView",
                "spacing": 16
            },
            {
                "class": "DepictionSeparatorView"
            },
            {
                "class": "DepictionHeaderView",
                "title": "Information",
                "useBoldText": True
            },
            {
                "class": "DepictionTableTextView",
                "title": "Developer",
                "text": meta["developer"]
            },
            {
                "class": "DepictionTableTextView",
                "title": "Compatibility",
                "text": meta["compatibility"]
            }
        ])

        depiction = {
            "minVersion": "0.1",
            "class": "DepictionTabView",
            "headerImage": f"{REPO_URL}/depictions/{pkg_id}/banner.png",
            "tintColor": "#007aff",
            "tabs": [
                {
                    "tabname": "Details",
                    "class": "DepictionStackView",
                    "views": details_views
                },
                {
                    "tabname": "Changelog",
                    "class": "DepictionStackView",
                    "views": [
                        {
                            "class": "DepictionHeaderView",
                            "title": f"Version {meta['version']}",
                            "useBoldText": True
                        },
                        {
                            "class": "DepictionMarkdownView",
                            "markdown": "- Latest release.\n- Added core functionality & performance improvements.\n- Optimized for modern iOS jailbreaks.",
                            "useSpacing": True
                        }
                    ]
                }
            ]
        }

        with open(f"{pkg_dir}/sileo.json", "w") as f:
            json.dump(depiction, f, indent=4)
        with open(f"{pkg_dir}/base.json", "w") as f:
            json.dump(depiction, f, indent=4)

def generate_static_package_pages():
    """Generates standalone clean SEO-optimized HTML pages for each tweak."""
    print("--> Generating Standalone Package HTML Pages for SEO...")
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — iOS Tweak | NekosofTech</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{name}, {pkg_id}, iOS tweak, jailbreak, Sileo, Zebra, Cydia, NekosofTech, DAN9">
    <meta name="author" content="{developer}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{page_url}">
    
    <!-- Open Graph SEO -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{page_url}">
    <meta property="og:title" content="{name} — iOS Tweak">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{banner_url}">
    <meta property="og:site_name" content="NekosofTech">
    
    <!-- Twitter Card SEO -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{page_url}">
    <meta name="twitter:title" content="{name} — iOS Tweak">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{banner_url}">
    
    <!-- Favicons -->
    <link rel="icon" type="image/png" sizes="48x48" href="../../favicon-48x48.png">
    <link rel="icon" type="image/png" sizes="96x96" href="../../favicon-96x96.png">
    <link rel="apple-touch-icon" sizes="180x180" href="../../apple-touch-icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "{name}",
      "operatingSystem": "{compatibility}",
      "applicationCategory": "UtilitiesApplication",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "description": "{description}",
      "author": {{
        "@type": "Person",
        "name": "{developer}"
      }},
      "image": "{icon_url}"
    }}
    </script>

    <style>
        :root {{
            --bg-color: #f4f4f7;
            --surface-color: #ffffff;
            --surface-border: #eef0f2;
            --primary-color: #007aff;
            --text-main: #1c1c1e;
            --text-muted: #8e8e93;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.03);
            --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.06);
            --tag-bg: #e6f2ff;
            --tag-text: #007aff;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }}
        body {{ background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; align-items: center; -webkit-font-smoothing: antialiased; }}
        a {{ text-decoration: none; color: inherit; }}
        .container {{ max-width: 800px; width: 100%; padding: 40px 24px; }}
        
        .header-nav {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }}
        .back-nav {{ display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: var(--primary-color); }}
        .back-nav:hover {{ text-decoration: underline; }}
        
        .card {{ background: var(--surface-color); border: 1px solid var(--surface-border); border-radius: 24px; padding: 32px; box-shadow: var(--shadow-sm); }}
        .banner {{ width: 100%; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 1px solid var(--surface-border); aspect-ratio: 5 / 2; }}
        .banner img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
        
        .pkg-header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 24px; flex-wrap: wrap; }}
        .pkg-icon {{ width: 80px; height: 80px; border-radius: 20px; overflow: hidden; border: 1px solid var(--surface-border); flex-shrink: 0; background: #f4f4f5; }}
        .pkg-icon img {{ width: 100%; height: 100%; object-fit: cover; }}
        .pkg-info {{ flex: 1; min-width: 200px; }}
        .pkg-info h1 {{ font-size: 2rem; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.5px; }}
        .pkg-info .meta {{ color: var(--text-muted); font-size: 0.95rem; font-weight: 500; }}
        
        .btn-grid {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 24px 0; }}
        .btn-action {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 14px; font-weight: 600; font-size: 0.95rem; background: var(--surface-color); border: 1px solid var(--surface-border); box-shadow: var(--shadow-sm); transition: transform 0.2s, box-shadow 0.2s; }}
        .btn-action:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-md); }}
        .btn-action img {{ width: 24px; height: 24px; border-radius: 6px; }}
        .btn-primary {{ background: var(--primary-color); color: #ffffff; border: none; }}
        
        .section-title {{ font-size: 1.3rem; font-weight: 700; margin: 28px 0 12px; }}
        .description {{ line-height: 1.6; color: #374151; font-size: 1.05rem; }}
        
        .features-list {{ margin-left: 20px; margin-top: 12px; color: #374151; line-height: 1.7; }}
        
        .info-table {{ width: 100%; border-top: 1px solid var(--surface-border); margin-top: 28px; padding-top: 12px; }}
        .table-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--surface-border); font-size: 0.95rem; }}
        .table-row:last-child {{ border-bottom: none; }}
        .table-label {{ color: var(--text-muted); font-weight: 500; }}
        .table-value {{ font-weight: 600; color: var(--text-main); }}
        
        .screenshots-grid {{ display: flex; gap: 12px; overflow-x: auto; padding-bottom: 12px; margin-top: 12px; }}
        .screenshots-grid img {{ height: 340px; border-radius: 12px; border: 1px solid var(--surface-border); flex-shrink: 0; }}
        
        .footer {{ margin-top: auto; padding: 48px 24px 32px; text-align: center; font-size: 0.85rem; color: var(--text-muted); }}
        .footer a {{ color: var(--primary-color); font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-nav">
            <a href="../../" class="back-nav">← Back to NekosofTech Repo</a>
        </div>
        
        <div class="card">
            <div class="banner">
                <img src="../../depictions/{pkg_id}/banner.png" alt="{name} banner" onerror="this.parentElement.style.display='none';">
            </div>
            
            <div class="pkg-header">
                <div class="pkg-icon">
                    <img src="../../depictions/{pkg_id}/icon.png" alt="{name} icon" onerror="this.src='../../logo/CydiaIcon.png';">
                </div>
                <div class="pkg-info">
                    <h1>{name}</h1>
                    <div class="meta">v{version} &bull; {developer}</div>
                    <div class="meta" style="margin-top:4px;">Compatibility: {compatibility}</div>
                </div>
                <div style="margin-left: auto;">
                    <span style="background:var(--tag-bg); color:var(--tag-text); font-weight:700; padding:8px 18px; border-radius:12px; font-size:1rem;">FREE</span>
                </div>
            </div>
            
            <div class="btn-grid">
                <a href="sileo://source/https://nekosoftech.github.io/repo" class="btn-action">
                    <img src="../../logo/SileoIcon.png" alt="Sileo"> Add to Sileo
                </a>
                <a href="zbra://sources/add/https://nekosoftech.github.io/repo" class="btn-action">
                    <img src="../../logo/ZebraIcon.png" alt="Zebra"> Add to Zebra
                </a>
                <a href="cydia://url/https://cydia.saurik.com/api/share#?source=https://nekosoftech.github.io/repo" class="btn-action">
                    <img src="../../logo/CydiaIcon.png" alt="Cydia"> Add to Cydia
                </a>
                <a href="../../{deb_file}" class="btn-action btn-primary" download>
                    📥 Download .DEB
                </a>
            </div>
            
            <div class="section-title">About {name}</div>
            <div class="description">{detailed_description}</div>
            
            <div class="section-title">Features</div>
            <ul class="features-list">
                {features_html}
            </ul>
            
            {screenshots_html}
            
            <div class="info-table">
                <div class="table-row">
                    <div class="table-label">Developer</div>
                    <div class="table-value">{developer}</div>
                </div>
                <div class="table-row">
                    <div class="table-label">Version</div>
                    <div class="table-value">{version}</div>
                </div>
                <div class="table-row">
                    <div class="table-label">Compatibility</div>
                    <div class="table-value">{compatibility}</div>
                </div>
                <div class="table-row">
                    <div class="table-label">Bundle ID</div>
                    <div class="table-value">{pkg_id}</div>
                </div>
                <div class="table-row">
                    <div class="table-label">Section</div>
                    <div class="table-value">{section}</div>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer">
        &copy; 2026 <a href="https://nekosoftech.com/" target="_blank" rel="noopener">NekosofTech</a>. Built by {developer}
    </footer>
</body>
</html>
"""

    for pkg_id, meta in PACKAGES_META.items():
        out_dir = f"package/{pkg_id}"
        os.makedirs(out_dir, exist_ok=True)
        
        # Features HTML
        features_html = "\n".join([f"<li>{f}</li>" for f in meta["features"]])
        
        # Screenshots
        screenshots_dir = f"depictions/{pkg_id}"
        screenshots = []
        if os.path.exists(screenshots_dir):
            for file in sorted(os.listdir(screenshots_dir)):
                if file.startswith("screenshot") and file.endswith((".png", ".jpg", ".jpeg")):
                    screenshots.append(f"../../depictions/{pkg_id}/{file}")
        
        if screenshots:
            imgs = "".join([f'<img src="{s}" alt="Screenshot">' for s in screenshots])
            screenshots_html = f'<div class="section-title">Screenshots</div><div class="screenshots-grid">{imgs}</div>'
        else:
            screenshots_html = ""

        page_url = f"{REPO_URL}/package/{pkg_id}/"
        banner_url = f"{REPO_URL}/depictions/{pkg_id}/banner.png"
        icon_url = f"{REPO_URL}/depictions/{pkg_id}/icon.png"

        html_content = html_template.format(
            name=meta["name"],
            description=meta["description"],
            detailed_description=meta["detailed_description"],
            pkg_id=pkg_id,
            version=meta["version"],
            developer=meta["developer"],
            compatibility=meta["compatibility"],
            section=meta["section"],
            deb_file=meta["deb_file"],
            features_html=features_html,
            screenshots_html=screenshots_html,
            page_url=page_url,
            banner_url=banner_url,
            icon_url=icon_url
        )
        
        with open(f"{out_dir}/index.html", "w") as f:
            f.write(html_content)

def generate_packages_files():
    """Generates updated Packages, Packages.gz, and Packages.bz2 files."""
    print("--> Generating Packages APT repo files...")
    packages_blocks = []
    
    for pkg_id, meta in PACKAGES_META.items():
        deb_file = meta["deb_file"]
        if not os.path.exists(deb_file):
            print(f"Warning: {deb_file} missing!")
            continue
            
        file_size = os.path.getsize(deb_file)
        
        # Extract deb control using dpkg-deb
        res = subprocess.run(["dpkg-deb", "-f", deb_file], capture_output=True, text=True)
        control_text = res.stdout.strip()
        
        # Parse fields
        fields = {}
        for line in control_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fields[k.strip()] = v.strip()
                
        # Override metadata
        fields["Package"] = pkg_id
        fields["Name"] = meta["name"]
        fields["Version"] = meta["version"]
        fields["Description"] = meta["description"]
        fields["Maintainer"] = meta["developer"]
        fields["Author"] = meta["developer"]
        fields["Section"] = meta["section"]
        fields["Filename"] = deb_file
        fields["Size"] = str(file_size)
        fields["Depiction"] = f"{REPO_URL}/depictions/{pkg_id}/info.xml"
        fields["SileoDepiction"] = f"{REPO_URL}/depictions/{pkg_id}/sileo.json"
        
        block = ""
        for k, v in fields.items():
            block += f"{k}: {v}\n"
        packages_blocks.append(block)

    full_packages_text = "\n".join(packages_blocks) + "\n"
    
    with open("Packages", "w") as f:
        f.write(full_packages_text)
        
    with gzip.open("Packages.gz", "wb") as f:
        f.write(full_packages_text.encode("utf-8"))
        
    with bz2.open("Packages.bz2", "wb") as f:
        f.write(full_packages_text.encode("utf-8"))

def generate_sitemap():
    """Generates sitemap.xml with all clean URLs."""
    print("--> Generating sitemap.xml...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    urls = [
        f"""  <url>
    <loc>{REPO_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]
    
    for pkg_id in PACKAGES_META.keys():
        urls.append(f"""  <url>
    <loc>{REPO_URL}/package/{pkg_id}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")
        
    urls_joined = "\n".join(urls)
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_joined}
</urlset>
"""
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_content)

def generate_sileo_featured():
    """Generates sileo-featured.json."""
    print("--> Generating sileo-featured.json...")
    banners = []
    for pkg_id, meta in PACKAGES_META.items():
        banners.append({
            "url": f"{REPO_URL}/depictions/{pkg_id}/banner.png",
            "title": meta["name"],
            "package": pkg_id,
            "hideShadow": False
        })
    featured = {
        "class": "FeaturedBannersView",
        "itemSize": "{263, 148}",
        "itemCornerRadius": 10,
        "banners": banners
    }
    with open("sileo-featured.json", "w") as f:
        json.dump(featured, f, indent=4)

if __name__ == "__main__":
    generate_sileo_depictions()
    generate_static_package_pages()
    generate_packages_files()
    generate_sitemap()
    generate_sileo_featured()
    print("✨ Build completed successfully!")
