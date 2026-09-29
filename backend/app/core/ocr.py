
from paddleocr import PaddleOCR


class PaddleOCRWrapper:
    def __init__(self):
        self.model=  PaddleOCR(use_angle_cls=True,lang='ar')


    def extract_text(self, image):
        results = self.model.predict(image,use_doc_orientation_classify=False,
    use_doc_unwarping=False, use_textline_orientation=True)
        return results
