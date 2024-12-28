from manga_colorizer.processors.panel_cleaner import PanelCleaner


def test():
    cleaner = PanelCleaner()
    cleaner.display(
        "/Users/davidwen/Repositories/manga-colorizer/manga-raw/color1/manga_one-piece-digital-colored-chapter-1001/03.webp"
    )
