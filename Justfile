scrape-color-1:
    python scripts/scrape_op_images.py \
    https://onepiececolored.online \
    --download_dir ./manga-raw/color1/ \
    --pattern https://onepiececolored.online/manga \
    --img_pattern https://lh3.googleusercontent.com/ \

scrape-ink-1:
    python scripts/scrape_op_images.py \
    https://w47.1piecemanga.com \
    --download_dir ./manga-raw/ink1/ \
    --pattern https://w47.1piecemanga.com/manga \
    --img_pattern "^https://(peak-manga|tensei|imagizer|blogger).*(.jpg|.jpeg|.webp|.png)$|^https://blogger.googleusercontent.com" \

