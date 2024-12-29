from pathlib import Path

from manga_colorizer.processors.panel_cleaner import PanelCleaner

color_path = Path("./manga-raw/color1/")
color_img_paths = [
    path
    for chapter_path in color_path.iterdir()
    if chapter_path.is_dir()
    if chapter_path.is_dir() and "1001" in chapter_path.name
    for path in chapter_path.iterdir()
]


def test_display_ink_images():
    ink_path = Path("./manga-raw/ink1/")
    ink_img_paths = [
        path
        for chapter_path in ink_path.iterdir()
        if chapter_path.is_dir()
        if chapter_path.is_dir() and "1001" in chapter_path.name
        for path in chapter_path.iterdir()
    ]
    cleaner = PanelCleaner()

    for path in ink_img_paths:
        cleaner.display(path)
