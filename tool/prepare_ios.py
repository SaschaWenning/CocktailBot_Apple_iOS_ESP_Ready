#!/usr/bin/env python3
"""Generate and configure the Flutter iOS host project for CocktailBot.

This script is designed for Codemagic/macOS CI. It keeps the existing Flutter
app source intact, generates the missing ios/ host project with Flutter, and
adds the privacy/network settings required to talk to a local ESP controller.
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


def generate_ios() -> None:
    runner = ROOT / "ios" / "Runner" / "Info.plist"
    if runner.exists():
        print("iOS host project already exists; generation skipped.")
        return

    if shutil.which("flutter") is None:
        raise SystemExit(
            "Flutter was not found. Run this script on a Mac/CI image with Flutter installed "
            "(for example Codemagic)."
        )

    # flutter create may refresh common project files. Preserve the app files
    # supplied by the user so the Android/web functionality is not replaced.
    preserve = [ROOT / "lib" / "main.dart", ROOT / "pubspec.yaml"]
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        saved: list[tuple[Path, Path]] = []
        for src in preserve:
            if src.exists():
                dst = tmpdir / src.name
                shutil.copy2(src, dst)
                saved.append((src, dst))

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

        for dst, src in saved:
            shutil.copy2(src, dst)


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

    ats = data.get("NSAppTransportSecurity")
    if not isinstance(ats, dict):
        ats = {}
    # Keep ATS enabled for the internet; only local networking is allowed.
    ats["NSAllowsLocalNetworking"] = True
    data["NSAppTransportSecurity"] = ats

    with path.open("wb") as f:
        plistlib.dump(data, f, sort_keys=False)

    print(f"Patched local-network privacy settings in {path.relative_to(ROOT)}")


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
    patch_bundle_id(args.bundle_id)
    print("CocktailBot iOS preparation complete.")


if __name__ == "__main__":
    main()
