from backend.app.core.ingestion import CardIngest, CardPreprocess
from backend.app.core.preprocessing import CardDetector, CardPerspective, ProcessCard
from backend.app.core.ocr import PaddleOCRWrapper


class IDCardWorker:
    """Owns the reusable components for processing ID cards."""

    def __init__(self):
        self.ingestion = CardIngest()
        self.preprocessor = CardPreprocess()
        self.detector = CardDetector()
        self.perspective = CardPerspective()
        self.processor = ProcessCard()
        self.ocr = PaddleOCRWrapper()