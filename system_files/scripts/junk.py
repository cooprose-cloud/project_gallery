#!/usr/bin/env python3
"""
Photos at an Exposition — Configuration Generator
Walks the user through building a complete photo_config.json file
by scanning their gallery directories and prompting for site details.

Usage:
    python3 generate_photo_config.py                  # interactive wizard
    python3 generate_photo_config.py --user-dir PATH  # pre-set user directory
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import date
from typing import List, Dict, Any

# ── Constants ──────────────────────────────────────────────────────────

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
DEFAULT_CONFIG_FILE = 'photo_config.json'
MAX_SLIDESHOW_PHOTOS = 8
SEP = '─' * 60


# ── Helpers ────────────────────────────────────────────────────────────

def ask(prompt: str, default: str = '') -> str:
    """Prompt the user for input, showing a default value."""
    if default:
        result = input(f"  {prompt} [{default}]: ").strip()
        return result if result else default
    else:
        while True:
            result = input(f"  {prompt}: ").strip()
            if result:
                return result
            print("    (required — please enter a value)")


def ask_yn(prompt: str, default: bool = True) -> bool:
    """Prompt for a yes/no answer."""
    hint = 'Y/n' if default else 'y/N'
    answer = input(f"  {prompt} [{hint}]: ").strip().lower()
    if not answer:
        return default
    return answer.startswith('y')


def ask_int(prompt: str, default: int, min_val: int = 1) -> int:
    """Prompt for an integer."""
    while True:
        raw = input(f"  {prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            val = int(raw)
            if val >= min_val:
                return val
        except ValueError:
            pass
        print(f"    Please enter a whole number >= {min_val}.")


def get_image_files(directory: Path) -> List[str]:
    """Return sorted list of image filenames in a directory."""
    if not directory.exists():
        return []
    return sorted(
        f.name for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    )


def get_notes_file(directory: Path) -> Dict[str, str]:
    """
    Look for an optional notes file in a gallery directory.
    Format (one entry per line):  filename.jpg | Caption text here
    Returns dict: {filename: caption}
    """
    notes = {}
    for candidate in ('notes.txt', 'captions.txt', 'notes.csv'):
        notes_path = directory / candidate
        if notes_path.exists():
            print(f"    Found notes file: {candidate}")
            with open(notes_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '|' in line:
                        parts = line.split('|', 1)
                        fname   = parts[0].strip()
                        caption = parts[1].strip()
                        if fname:
                            notes[fname] = caption
            print(f"    Loaded {len(notes)} caption(s)")
            break
    return notes


# ── Main sections ──────────────────────────────────────────────────────

def collect_site_info() -> Dict[str, str]:
    print(f"\n{SEP}")
    print("  SITE INFORMATION")
    print(SEP)
    year = str(date.today().year)
    return {
        'title':             ask("Website title",            "Photographs by J. Cooper Rose"),
        'subtitle':          ask("Subtitle",                 "A Photographic Journey"),
        'photographer_name': ask("Photographer name",        "J. Cooper Rose"),
        'overview':          ask("Overview / welcome text",  "Welcome to my photographic collection."),
        'date_published':    ask("Date published",           date.today().strftime("%B %Y")),
        'copyright_year':    ask("Copyright year",           year),
    }


def collect_directories(user_dir: Path) -> Dict[str, str]:
    """Collect output and support-files paths."""
    print(f"\n{SEP}")
    print("  DIRECTORIES")
    print(SEP)
    print(f"  User (source) directory: {user_dir}")

    default_output   = str(user_dir.parent / 'website')
    default_support  = str(user_dir / 'support_files')

    output_dir  = ask("Output directory (generated website)", default_output)
    support_dir = ask("Support files directory (css/logo/js)", default_support)

    return {
        'output_directory':         output_dir,
        'support_files_directory':  support_dir,
    }


def collect_galleries(user_dir: Path) -> List[Dict[str, Any]]:
    """
    Scan user_dir for gallery subfolders.
    Each immediate subdirectory that is not 'support_files' or 'slideshow'
    is treated as a potential gallery.
    """
    print(f"\n{SEP}")
    print("  GALLERIES")
    print(SEP)

    SKIP_DIRS = {'support_files', 'slideshow', 'css', 'js', '__pycache__'}

    # Find candidate gallery directories
    candidates = sorted(
        d for d in user_dir.iterdir()
        if d.is_dir() and d.name not in SKIP_DIRS and not d.name.startswith('.')
    )

    if not candidates:
        print("  No subdirectories found. You can add galleries manually.")
        return []

    print(f"  Found {len(candidates)} potential gallery folder(s):")
    for d in candidates:
        n = len(get_image_files(d))
        print(f"    {d.name}  ({n} image{'s' if n != 1 else ''})")

    galleries = []
    for d in candidates:
        photos = get_image_files(d)
        if not photos:
            print(f"\n  Skipping '{d.name}' — no images found.")
            continue

        print(f"\n  Gallery folder: {d.name}  ({len(photos)} photos)")
        include = ask_yn(f"Include '{d.name}' as a gallery?", default=True)
        if not include:
            continue

        gid  = ask("  Gallery ID (no spaces)", d.name.lower().replace(' ', '_'))
        name = ask("  Display name",           d.name.replace('_', ' ').title())
        desc = ask("  Description",            f"Photos from {name}")

        notes = get_notes_file(d)

        gallery: Dict[str, Any] = {
            'id':               gid,
            'name':             name,
            'description':      desc,
            'source_directory': str(d),
            'photos':           photos,
        }
        if notes:
            gallery['notes'] = notes

        galleries.append(gallery)
        print(f"    Added '{name}' with {len(photos)} photo(s).")

    return galleries


def collect_slideshow(galleries: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Pick one photo per gallery for the home-page slideshow."""
    print(f"\n{SEP}")
    print("  SLIDESHOW")
    print(SEP)
    print("  The slideshow on the home page shows one photo from each gallery.")
    print(f"  (Maximum {MAX_SLIDESHOW_PHOTOS} photos)")

    slideshow = []
    for gallery in galleries[:MAX_SLIDESHOW_PHOTOS]:
        gid    = gallery['id']
        photos = gallery['photos']
        print(f"\n  Gallery: {gallery['name']}")
        print(f"  First photo (default): {photos[0]}")

        if len(photos) == 1 or not ask_yn("  Choose a different slideshow photo?", default=False):
            chosen = photos[0]
        else:
            print("  Available photos:")
            for i, p in enumerate(photos):
                print(f"    {i + 1}. {p}")
            idx = ask_int("  Enter photo number", default=1, min_val=1)
            chosen = photos[min(idx - 1, len(photos) - 1)]

        slideshow.append({'gallery_id': gid, 'photo_file': chosen})
        print(f"  Selected: {chosen}")

    return slideshow


def collect_options() -> Dict[str, Any]:
    print(f"\n{SEP}")
    print("  OPTIONS")
    print(SEP)
    thumb_w = ask_int("Thumbnail width  (px)", default=300)
    thumb_h = ask_int("Thumbnail height (px)", default=300)
    ss_secs = ask_int("Slideshow interval (seconds)", default=5)
    captions = ask_yn("Show gallery name captions on slideshow?", default=True)
    return {
        'thumbnail_size':    [thumb_w, thumb_h],
        'slideshow_config':  {
            'interval_seconds': ss_secs,
            'show_captions':    captions,
        }
    }


def write_config(config: Dict[str, Any], output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def print_summary(config: Dict[str, Any], output_file: str):
    print(f"\n{'=' * 60}")
    print(f"  Configuration saved: {output_file}")
    print(f"{'=' * 60}")
    print(f"  Galleries : {len(config['galleries'])}")
    total = sum(len(g['photos']) for g in config['galleries'])
    print(f"  Photos    : {total}")
    print(f"  Slideshow : {len(config['slideshow_photos'])} photo(s)")
    print(f"  Output dir: {config['output_directory']}")
    print()
    print("  Next step — generate your website:")
    print(f"    python3 photos_exposition.py {output_file}")
    print()


# ── Entry point ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Photos at an Exposition — Configuration Generator'
    )
    parser.add_argument(
        '--user-dir', '-u',
        help='Path to your user gallery directory (skips the prompt)',
        default=None
    )
    parser.add_argument(
        '--output', '-o',
        help=f'Config file to write (default: {DEFAULT_CONFIG_FILE})',
        default=DEFAULT_CONFIG_FILE
    )
    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       Photos at an Exposition — Config Generator        ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ── Step 1: user directory
    if args.user_dir:
        user_dir = Path(args.user_dir)
    else:
        print(f"\n{SEP}")
        print("  USER DIRECTORY")
        print(SEP)
        print("  This is the folder where your gallery subfolders live.")
        raw = ask("Path to your gallery directory")
        user_dir = Path(raw).expanduser()

    if not user_dir.exists():
        print(f"\n  ERROR: Directory not found: {user_dir}")
        sys.exit(1)

    # ── Steps 2-6
    site_info  = collect_site_info()
    dirs       = collect_directories(user_dir)
    galleries  = collect_galleries(user_dir)

    if not galleries:
        print("\n  No galleries configured. Exiting.")
        sys.exit(0)

    slideshow  = collect_slideshow(galleries)
    options    = collect_options()

    # ── Assemble config
    config: Dict[str, Any] = {
        'site_info':                site_info,
        'output_directory':         dirs['output_directory'],
        'support_files_directory':  dirs['support_files_directory'],
        'thumbnail_size':           options['thumbnail_size'],
        'slideshow_config':         options['slideshow_config'],
        'galleries':                galleries,
        'slideshow_photos':         slideshow,
    }

    # ── Write and summarise
    write_config(config, args.output)
    print_summary(config, args.output)


if __name__ == '__main__':
    main()
