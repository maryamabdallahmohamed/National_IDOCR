import cv2
import imutils
import numpy as np
from backend.app.core.logging import get_logger

logger= get_logger("Ingestion Pipeline")

class CardIngest:
    
    def process_image(self, image_bytes: bytes):

        image_array = np.frombuffer(image_bytes,dtype=np.uint8)

        image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Invalid image")

        image = imutils.resize(image,width=800)

        logger.info(f"Processed image with shape of {image.shape}")

        return image


class CardPreprocess:

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.normalize(gray, None,0,255, cv2.NORM_MINMAX)


        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        return blurred

    def enhance_text(self, image):
        if len(image.shape) == 2:
            gray = image.copy()
        elif image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif image.shape[2] == 4:
            gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            raise ValueError(f"Unsupported image shape: {image.shape}")

        gray = cv2.resize(
            gray,
            None,
            fx=5,
            fy=5,
            interpolation=cv2.INTER_CUBIC
        )

        clahe = cv2.createCLAHE(
            clipLimit=2.5,
            tileGridSize=(3, 3)
        )
        contrast = clahe.apply(gray)

        blurred = cv2.GaussianBlur(contrast, (0, 0), 2)
        sharpened = cv2.addWeighted(
            contrast, 1.8,
            blurred, -0.8,
            0
        )

        _, binary = cv2.threshold(
            sharpened,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        logger.info(f"Enhanced text region with shape of {sharpened.shape}")

        return sharpened, binary

    def find_contours(self, image):
        edges = cv2.Canny(image,50,150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        return contours, edges
    def intensify_black(self, image, threshold=150, strength=1.5):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        gray_float = gray.astype(np.float32)

        # Darken dark pixels progressively
        enhanced = np.where(
            gray_float < threshold,
            gray_float * (1 - (strength - 1) *
                        (threshold - gray_float) / threshold),
            gray_float
        )

        logger.info(f"Intensified black regions in image with shape of {enhanced.shape}")

        return np.clip(enhanced, 0, 255).astype(np.uint8)

    