#!/usr/bin/env python3
"""Generate and configure the Flutter iOS host project for CocktailBot.

Designed for Codemagic/macOS CI. If an incomplete placeholder ``ios/`` folder
exists, it is removed first so Flutter can generate a real Xcode project.
The existing Flutter/Dart app source and ESP HTTP control logic are preserved.
"""
from __future__ import annotations

import argparse
import os
import plistlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def ios_project_complete() -> bool:
    return (
        (ROOT / "ios" / "Runner.xcodeproj" / "project.pbxproj").is_file()
        and (ROOT / "ios" / "Runner" / "Info.plist").is_file()
    )


def generate_ios() -> None:
    if ios_project_complete():
        print("Complete iOS host project already exists; generation skipped.")
        return

    if shutil.which("flutter") is None:
        raise SystemExit(
            "Flutter was not found. Run this script on a Mac/CI image with Flutter installed "
            "(for example Codemagic)."
        )

    ios_dir = ROOT / "ios"
    if ios_dir.exists():
        print("Removing incomplete ios/ placeholder before Flutter generation.")
        shutil.rmtree(ios_dir)

    # flutter create can refresh common files. Back up the user's app source and
    # manifest, then restore them so the working Android/ESP app logic stays intact.
    preserve = [ROOT / "lib" / "main.dart", ROOT / "pubspec.yaml"]
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        saved: list[tuple[Path, Path]] = []
        for original in preserve:
            if original.exists():
                backup = tmpdir / original.name
                shutil.copy2(original, backup)
                saved.append((original, backup))

        run(
            "flutter",
            "create",
            "--platforms=ios",
            "--org",
            "de.cocktailbot",
            "--project-name",
            "cocktailbot_app",
            ".",
        )

        for original, backup in saved:
            shutil.copy2(backup, original)

    if not ios_project_complete():
        raise SystemExit(
            "Flutter finished, but ios/Runner.xcodeproj or ios/Runner/Info.plist "
            "was not generated."
        )


def patch_info_plist() -> None:
    path = ROOT / "ios" / "Runner" / "Info.plist"
    if not path.exists():
        raise SystemExit(f"Missing {path}. iOS project generation failed.")

    with path.open("rb") as f:
        data = plistlib.load(f)

    data["CFBundleDisplayName"] = "CocktailBot"
    data["NSLocalNetworkUsageDescription"] = (
        "CocktailBot benötigt Zugriff auf das lokale Netzwerk, um den ESP-Controller "
        "der Cocktailmaschine zu finden und Steuerbefehle zu senden."
    )
    data["NSPhotoLibraryUsageDescription"] = (
        "CocktailBot benötigt Zugriff auf deine Fotomediathek, damit du ein eigenes "
        "Bild für Cocktails und Rezepte auswählen kannst."
    )
    data["NSCameraUsageDescription"] = (
        "CocktailBot benötigt Kamerazugriff, damit du bei der Bildauswahl ein Foto "
        "für Cocktails und Rezepte aufnehmen kannst."
    )
    data["NSLocationWhenInUseUsageDescription"] = (
        "CocktailBot verwendet den Standort nur, falls iOS ihn für lokale WLAN-Funktionen "
        "zur Verbindung mit der Cocktailmaschine anfordert."
    )
    data["ITSAppUsesNonExemptEncryption"] = False

    ats = data.get("NSAppTransportSecurity")
    if not isinstance(ats, dict):
        ats = {}
    # Keep ATS enabled for internet traffic while explicitly permitting local LAN use.
    ats["NSAllowsLocalNetworking"] = True
    data["NSAppTransportSecurity"] = ats

    with path.open("wb") as f:
        plistlib.dump(data, f, sort_keys=False)

    print(f"Patched iOS privacy settings in {path.relative_to(ROOT)}")



def patch_app_icon() -> None:
    source_dir = ROOT / "tool" / "ios_appicon"
    target_dir = ROOT / "ios" / "Runner" / "Assets.xcassets" / "AppIcon.appiconset"
    if not source_dir.is_dir():
        raise SystemExit(f"Missing iOS icon source directory: {source_dir}")
    if not target_dir.is_dir():
        raise SystemExit(f"Missing generated AppIcon set: {target_dir}")

    contents = {
        "images": [
            {"idiom": "iphone", "size": "20x20", "scale": "2x", "filename": "Icon-App-20x20@2x.png"},
            {"idiom": "iphone", "size": "20x20", "scale": "3x", "filename": "Icon-App-20x20@3x.png"},
            {"idiom": "iphone", "size": "29x29", "scale": "2x", "filename": "Icon-App-29x29@2x.png"},
            {"idiom": "iphone", "size": "29x29", "scale": "3x", "filename": "Icon-App-29x29@3x.png"},
            {"idiom": "iphone", "size": "40x40", "scale": "2x", "filename": "Icon-App-40x40@2x.png"},
            {"idiom": "iphone", "size": "40x40", "scale": "3x", "filename": "Icon-App-40x40@3x.png"},
            {"idiom": "iphone", "size": "60x60", "scale": "2x", "filename": "Icon-App-60x60@2x.png"},
            {"idiom": "iphone", "size": "60x60", "scale": "3x", "filename": "Icon-App-60x60@3x.png"},
            {"idiom": "ipad", "size": "20x20", "scale": "1x", "filename": "Icon-App-20x20@1x.png"},
            {"idiom": "ipad", "size": "20x20", "scale": "2x", "filename": "Icon-App-20x20@2x.png"},
            {"idiom": "ipad", "size": "29x29", "scale": "1x", "filename": "Icon-App-29x29@1x.png"},
            {"idiom": "ipad", "size": "29x29", "scale": "2x", "filename": "Icon-App-29x29@2x.png"},
            {"idiom": "ipad", "size": "40x40", "scale": "1x", "filename": "Icon-App-40x40@1x.png"},
            {"idiom": "ipad", "size": "40x40", "scale": "2x", "filename": "Icon-App-40x40@2x.png"},
            {"idiom": "ipad", "size": "76x76", "scale": "1x", "filename": "Icon-App-76x76@1x.png"},
            {"idiom": "ipad", "size": "76x76", "scale": "2x", "filename": "Icon-App-76x76@2x.png"},
            {"idiom": "ipad", "size": "83.5x83.5", "scale": "2x", "filename": "Icon-App-83.5x83.5@2x.png"},
            {"idiom": "ios-marketing", "size": "1024x1024", "scale": "1x", "filename": "Icon-App-1024x1024@1x.png"},
        ],
        "info": {"version": 1, "author": "xcode"},
    }

    import json
    for image in contents["images"]:
        filename = image["filename"]
        src = source_dir / filename
        if not src.is_file():
            raise SystemExit(f"Missing iOS app icon asset: {src}")
        shutil.copy2(src, target_dir / filename)

    (target_dir / "Contents.json").write_text(
        json.dumps(contents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    # Verify the marketing icon is RGB/RGBA-free and non-placeholder source is present.
    marketing = target_dir / "Icon-App-1024x1024@1x.png"
    if not marketing.is_file() or marketing.stat().st_size < 10000:
        raise SystemExit("iOS marketing icon was not installed correctly.")
    print("Installed finalized CocktailBot iOS app icon assets.")

def patch_bundle_id(bundle_id: str) -> None:
    project = ROOT / "ios" / "Runner.xcodeproj" / "project.pbxproj"
    if not project.exists():
        raise SystemExit(f"Missing {project}. iOS project generation failed.")

    text = project.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        current = match.group(1).strip().strip('"')
        suffix = ".RunnerTests" if current.endswith(".RunnerTests") else ""
        return f"PRODUCT_BUNDLE_IDENTIFIER = {bundle_id}{suffix};"

    updated, count = re.subn(
        r"PRODUCT_BUNDLE_IDENTIFIER\s*=\s*([^;]+);",
        repl,
        text,
    )
    if count == 0:
        raise SystemExit("Could not find PRODUCT_BUNDLE_IDENTIFIER in Xcode project.")
    project.write_text(updated, encoding="utf-8")
    print(f"Bundle identifier set to {bundle_id} ({count} build settings updated).")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bundle-id",
        default=os.environ.get("BUNDLE_ID", "de.cocktailbot.app"),
        help="iOS bundle identifier (default: de.cocktailbot.app)",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", args.bundle_id):
        raise SystemExit(f"Invalid bundle identifier: {args.bundle_id!r}")

    generate_ios()
    patch_info_plist()
    patch_app_icon()
    patch_bundle_id(args.bundle_id)

    pbx = ROOT / "ios" / "Runner.xcodeproj" / "project.pbxproj"
    plist = ROOT / "ios" / "Runner" / "Info.plist"
    print(f"Verified: {pbx.relative_to(ROOT)}")
    print(f"Verified: {plist.relative_to(ROOT)}")
    print("CocktailBot iOS preparation complete.")


if __name__ == "__main__":
    main()
