
from paddleocr import PaddleOCR
from backend.app.core.logging import get_logger

logger= get_logger("OCR Pipeline")

class PaddleOCRWrapper:
    def __init__(self):
        self.model=  PaddleOCR(use_angle_cls=True,lang='ar')
        logger.info("PaddleOCR model initialized")


    def extract_text(self, image):
        results = self.model.predict(image,use_doc_orientation_classify=False,use_doc_unwarping=False, use_textline_orientation=True)
        logger.info(f"Extracted text from image: {results}")
        return results
