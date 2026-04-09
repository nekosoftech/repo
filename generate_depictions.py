import json
import os

packages = {
    "com.hdun9.camaction": "CamAction",
    "com.hdun9.homeaction": "HomeAction",
    "com.hdun9.icloudremove": "iCloudRemove",
    "com.hdun9.privacydisplay": "PrivacyDisplay",
    "com.hdun9.virtualcam": "VirtualCam"
}

for pkg_id, pkg_name in packages.items():
    depiction = {
        "minVersion": "0.1",
        "class": "DepictionTabView",
        "headerImage": f"https://nekosoftech.github.io/repo/depictions/{pkg_id}/banner.png",
        "tintColor": "#3498db",
        "tabs": [
            {
                "tabname": "Details",
                "class": "DepictionStackView",
                "views": [
                    {
                        "class": "DepictionMarkdownView",
                        "markdown": f"### Welcome to {pkg_name}\n\nExperience a new level of customization with {pkg_name}. This tweak is designed to provide you with seamless and powerful enhancements for your iOS device.",
                        "useSpacing": True
                    },
                    {
                        "class": "DepictionSpacerView",
                        "spacing": 16
                    },
                    {
                        "class": "DepictionHeaderView",
                        "title": "Features",
                        "useBoldText": True
                    },
                    {
                        "class": "DepictionMarkdownView",
                        "markdown": "- Fully optimized for iOS 15 & 16.\n- Lightweight and battery-friendly.\n- Modern and native UI integration.\n- Regular updates and support.",
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
                        "text": "H.DUN9"
                    },
                    {
                        "class": "DepictionTableTextView",
                        "title": "Compatibility",
                        "text": "iOS 14.0 - 16.x"
                    }
                ]
            },
            {
                "tabname": "Changelog",
                "class": "DepictionStackView",
                "views": [
                    {
                        "class": "DepictionHeaderView",
                        "title": "Version 1.0.0",
                        "useBoldText": True
                    },
                    {
                        "class": "DepictionMarkdownView",
                        "markdown": "- Initial release.\n- Added core functionality.\n- Bug fixes and stability improvements.",
                        "useSpacing": True
                    }
                ]
            }
        ]
    }
    
    sileo_path = f"depictions/{pkg_id}/sileo.json"
    base_path = f"depictions/{pkg_id}/base.json"
    
    if os.path.exists(f"depictions/{pkg_id}"):
        with open(sileo_path, "w") as f:
            json.dump(depiction, f, indent=4)
        with open(base_path, "w") as f:
            json.dump(depiction, f, indent=4)

print("Depictions updated successfully.")
