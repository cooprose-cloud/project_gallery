# Photo Slideshow Viewer — User Guide

*Rose Family Archive · GRASP Photo Slideshow Builder*

---

## Opening the Viewer

1. Make sure `slideshow.html` and your `media/` folder are in the same directory.
2. Double-click `slideshow.html` to open it in your default browser.
3. For the best experience, press **F11** to hide the browser's address bar and
   toolbar (press **F11** again to restore them).

> **Firefox tip:** If the sidebar panel (Bookmarks / History) is open,
> press **Ctrl+B** to hide it and recover screen space.

---

## Layout Overview

```
┌─────────────┬──────────────────────────────────────────┐
│  Sidebar    │                                          │
│  ─────────  │         Main Image Stage                 │
│  Gallery 1  │                                          │
│  Gallery 2  │    ‹ prev           next ›               │
│  Gallery 3  │                                          │
│  ...        │   [ Notes banner — shown when enabled ]  │
├─────────────┼──────────────────────────────────────────┤
│             │  [ Thumbnail strip ]                     │
│             ├──────────────────────────────────────────┤
│             │  Gallery name        filename   3 / 47   │
│             ├──────────────────────────────────────────┤
│             │ ⇤  ▶ Play  ⇥  Delay ▾  📝 Notes  ⇄  ⛶  │
└─────────────┴──────────────────────────────────────────┘
```

---

## Sidebar — Gallery List

The left panel lists every gallery (sub-folder from your media directory).

| Action | Result |
|--------|--------|
| Click a gallery name | Switches to that gallery, starting at the first image |
| Scroll the list | Reveals more galleries if they don't all fit |

The active gallery is highlighted with a blue left border.

---

## Navigating Images

### Mouse
| Action | Result |
|--------|--------|
| Click **‹** / **›** arrows on stage | Previous / Next image |
| Click any thumbnail | Jump to that image |
| Double-click the main image | Open fullscreen overlay |

### Keyboard
| Key | Action |
|-----|--------|
| **→** or **↓** | Next image |
| **←** or **↑** | Previous image |
| **Home** | First image in gallery |
| **End** | Last image in gallery |
| **Space** | Play / Pause slideshow |
| **F** | Open / close fullscreen |
| **N** | Toggle notes on / off |
| **Esc** | Close fullscreen |

### Touch (mobile / tablet)
| Gesture | Action |
|---------|--------|
| Swipe left | Next image |
| Swipe right | Previous image |
| Tap thumbnails | Jump to image |

---

## Thumbnail Strip

The row of small images along the bottom of the stage shows every photo in the
current gallery. The active image has a gold border. Thumbnails scroll
automatically to keep the current image in view. Click any thumbnail to jump
directly to it.

---

## Control Bar

The bar at the very bottom of the stage contains:

| Control | Function |
|---------|----------|
| **⇤** (First) | Jump to the first image |
| **▶ Play / ⏸ Pause** | Start or stop automatic slideshow |
| **⇥** (Last) | Jump to the last image |
| **Delay ▾** | Set the time between slides: 2 / 4 / 6 / 10 / 15 seconds |
| **📝 Notes** | Toggle caption notes on or off |
| **⇄ Shuffle** | Randomize the image order in the current gallery |
| **⛶ Full** | Open the fullscreen overlay |

When **Play** is active, the slideshow advances through the current gallery and
then moves automatically to the next gallery when it reaches the last image.

---

## Notes / Captions

If a photo has a caption note entered in `photo_config.json`, it appears as a
dark banner with a gold top border at the bottom of the image.

- Click **📝 Notes** in the control bar (or press **N**) to show or hide all notes.
- Notes that are blank never show, even when Notes is turned on.
- The Notes button turns gold when notes are active.

To add or edit captions, open `photo_config.json` in a text editor and fill in
the `"note"` field for each image, then run:

```bash
python build_slideshow.py build --config photo_config.json --output slideshow.html
```

---

## Fullscreen Overlay

Double-click the main image, press **F**, or click **⛶ Full** to enter
fullscreen overlay mode.

### In fullscreen:
- The image displays with a gold border against a pure black background.
- **‹** and **›** arrow buttons navigate between images.
- Move the mouse to reveal the **auto-play control bar** at the bottom.
- The control bar hides after 2.5 seconds of inactivity.
- Hover over the control bar to keep it visible.

### Fullscreen control bar
| Control | Function |
|---------|----------|
| **▶ Play / ⏸ Pause** | Auto-advance in fullscreen |
| **Delay ▾** | Seconds between each image |
| Position counter | Shows current position, e.g. `12 / 89` |

The fullscreen play is independent of the main-view play — you can run
fullscreen autoplay while the main view is paused, or vice versa.

Press **Esc** or click **✕** to close fullscreen.

---

## Tips & Tricks

- **Best viewing experience:** Press **F11** in your browser to go truly
  fullscreen (hides the browser chrome), then press **F** in the viewer
  to open the image overlay. You get a completely unobstructed view.

- **Recovering from an accidental click:** If the control bar disappears
  in fullscreen, just move the mouse — it reappears immediately.

- **Sorting:** Re-run the `scan` command with `--sort date` to order photos
  by file modification date, or `--sort random` to shuffle on load.

- **Adding new photos:** Drop new images into any gallery sub-folder, then
  re-run `python build_slideshow.py all ...` to regenerate the slideshow.

---

*GRASP Photo Slideshow Builder — Rose Family Archive*
