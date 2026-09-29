

import cv2
from backend.app.core.logging import get_logger

logger= get_logger("Extractor Pipeline")

def extract_region_text(region, preprocessor, ocr):
    enhanced_region, binary_region = preprocessor.enhance_text(region)

    ocr_region = cv2.cvtColor(
        enhanced_region,
        cv2.COLOR_GRAY2BGR
    )

    result = ocr.extract_text(ocr_region)

    if not result:
        return ""

    return " ".join(result[0].get("rec_texts", []))

def convert_arabic_to_english(arabic_number):
    arabic_numerals='١٢٣٤٥٦٧٨٩٠'
    english_numerals='1234567890'
    translation_table = str.maketrans(arabic_numerals, english_numerals)
    return arabic_number.translate(translation_table)

