#!/usr/bin/env python3
"""Build the public plugin ZIP from the canonical skill without duplicating it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PLUGIN_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PLUGIN_ROOT.parent.parent
SKILL_ROOT = REPO_ROOT / "functional-programming"
SKILL_FILES = (
    "SKILL.md",
    "LICENSE.md",
    "SELF-TEST.md",
    "agents/openai.yaml",
    "references/FOUNDATIONS.md",
    "references/EFFECTS.md",
    "references/ALGEBRA.md",
    "references/SOURCES.md",
)
PACKAGE_FILES = (
    ".codex-plugin/plugin.json",
    "assets/icon.png",
    "assets/logo.png",
    "assets/logo.svg",
    "LICENSE.md",
    "README.md",
)


def read_file(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Package inputs must be regular files inside their root: {path}")
    return path.read_bytes()


def build(output_dir: Path) -> Path:
    files = {name: read_file(PLUGIN_ROOT, name) for name in PACKAGE_FILES}
    manifest = json.loads(files[".codex-plugin/plugin.json"])
    name = manifest["name"]
    version = manifest["version"]
    if name != PLUGIN_ROOT.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Plugin name must match its directory and use lowercase hyphens")
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        raise ValueError("Use a stable MAJOR.MINOR.PATCH version for public releases")
    interface = manifest["interface"]
    for key in ("displayName", "shortDescription"):
        if not isinstance(interface[key], str) or not 1 <= len(interface[key]) <= 30:
            raise ValueError(f"interface.{key} must contain 1–30 characters")
    if not 1 <= len(interface["longDescription"]) <= 4000:
        raise ValueError("interface.longDescription must contain 1–4000 characters")
    prompts = interface["defaultPrompt"]
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("Provide one to three starter prompts")
    if any(not isinstance(p, str) or not 1 <= len(p) <= 128 for p in prompts):
        raise ValueError("Starter prompts must contain 1–128 characters")
    if manifest.get("skills") != "./skills/":
        raise ValueError("This package discovers skills from ./skills/")
    if "apps" in manifest or "mcpServers" in manifest:
        raise ValueError("This builder packages a skills-only plugin")
    for key in ("composerIcon", "logo"):
        if interface[key].removeprefix("./") not in files:
            raise ValueError(f"Missing asset for interface.{key}")

    for relative in SKILL_FILES:
        files[f"skills/functional-programming/{relative}"] = read_file(SKILL_ROOT, relative)

    # Generate the portable format from the same metadata as the Codex overlay.
    portable = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **{key: value for key, value in manifest.items() if key not in {"skills", "interface"}},
        "extensions": {"com.openai": {"interface": interface}},
    }
    files["plugin.json"] = (json.dumps(portable, indent=2) + "\n").encode()

    # Fail on missing local links, including a newly referenced but unbundled file.
    for relative, data in files.items():
        if not relative.endswith(".md"):
            continue
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", data.decode()):
            if link.startswith(("https://", "http://", "#")):
                continue
            link_path = Path(relative).parent / link.split("#")[0]
            parts: list[str] = []
            for part in link_path.parts:
                if part == "..":
                    if not parts:
                        raise ValueError(f"Link escapes package: {relative}: {link}")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            if "/".join(parts) not in files:
                raise ValueError(f"Unbundled link: {relative}: {link}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{name}-{version}.zip"
    # Fixed timestamps, order, and permissions make identical inputs reproducible.
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative, data in sorted(files.items()):
            entry = ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = ZIP_DEFLATED
            bundle.writestr(entry, data, compresslevel=9)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{checksum}  {archive.name}\n")
    print(f"Built {archive} ({len(files)} files)")
    print(f"SHA-256: {checksum}")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "dist")
    args = parser.parse_args()
    build(args.output_dir.resolve())
