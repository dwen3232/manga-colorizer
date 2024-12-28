from huggingface_hub import hf_hub_download
from ultralytics import YOLO

_model = None


# https://huggingface.co/kitsumed/yolov8m_seg-speech-bubble/tree/main
def get_speech_bubble_segmenter() -> YOLO:
    global _model  # noqa: PLW0603
    if _model is None:
        model_path = hf_hub_download(
            "kitsumed/yolov8m_seg-speech-bubble",
            filename="model.pt",
        )
        _model = YOLO(model_path)
    return _model
