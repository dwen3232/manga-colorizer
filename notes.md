# Manga Colorizer

Some good urls:

- https://ww11.readonepiece.com/manga/one-piece-digital-colored-comics/
    - All chapters up to 1061, though some of the ones towards the end are fan colorings
    - Double page spreads as single image
    - Japanese onomatopoeias
    - CF protected
- https://w29.onepiece-manga-online.net/
    - All the ink chapters up to 1131 (most recent)
    - chapter numbers do not match urls
    - lot's of inconsistencies between pages
    - Japanese onomatopoeias
    - Unprotected
- https://theonepiecemangaonline.com/
    - All the ink chapters up to 1131 (most recent)
    - Images have watermarks :(
    - Double page spreads as single image
    - English onomatopoeias for majority of chapters
    - Unprotected
- https://onepiececolored.online
    - All color chapter up to 1004
    - Japanese onomatopoeias
    - Unprotected
- https://w47.1piecemanga.com
    - All chapters up to 1133
    - English onomatopoeias for majority of chapters
    - Unprotected



Tooling:
### 1. DVC pipelines (for versioning)
```yaml
# dvc.yaml
stages:
  augment:
    cmd: spark-submit augment_data.py
    deps:
      - data/original
      - augment_data.py
    outs:
      - data/augmented
```
maybe something with DVC experiments? https://dvc.org/doc/start/experiments/experiment-pipelines#expand-to-see-the-created-dvcyaml

### 2. Spark for data augmentation
Should use AWS EMR, good excuse to learn it


### 3. Kubeflow for training
Use kubeflow for model training experiments?

