from PIL import Image
from sentence_transformers import SentenceTransformer

_model = None


def get_clip_encoder():
    global _model
    if _model is None:
        _model = SentenceTransformer("clip-ViT-B-32")
    return _model


