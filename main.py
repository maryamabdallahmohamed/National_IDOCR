from backend.app.core.ingestion import CardIngest, CardPreprocess
from backend.app.core.preprocessing import CardDetector,CardPerspective,ProcessCard
from backend.app.core.ocr import PaddleOCRWrapper
from backend.app.core.extractor import extract_region_text, convert_arabic_to_english
from backend.app.core.models import IDCardData
def extract_id_card(image_bytes):

    # Initialize components
    ingestion = CardIngest()
    preprocessor = CardPreprocess()
    detector = CardDetector()
    perspective = CardPerspective()
    processor = ProcessCard()
    ocr = PaddleOCRWrapper()

    # 1. Load image
    image = ingestion.process_image(image_bytes)

    # 2. Preprocess image for contour detection
    blurred = preprocessor.preprocess_image(image)

    blurred = preprocessor.intensify_black(
        blurred,
        threshold=190,
        strength=2
    )

    # 3. Detect card
    contours, edges = preprocessor.find_contours(blurred)

    card_contour = detector.find_card_contour(
        contours,
        image.shape
    )

    # 4. Correct perspective
    ordered_points = perspective.four_point_transform(
        image,
        card_contour
    )

    # 5. Extract card fields
    (
        name_region_1,
        name_region_2,
        address_region,
        id_number_region1,
        id_number_region2,
        photo_region,
        factory_number_region
    ) = processor.get_fields(ordered_points)

    # 6. OCR each text region
    name_1 = extract_region_text( name_region_1, preprocessor, ocr)

    name_2 = extract_region_text(name_region_2, preprocessor, ocr)


    address = extract_region_text(address_region, preprocessor, ocr)

    id_1 = extract_region_text(id_number_region1, preprocessor, ocr)

    id_2 = extract_region_text(id_number_region2, preprocessor, ocr)

    factory_number = extract_region_text(factory_number_region, preprocessor, ocr)
    

    # 7. Combine text from multiple regions
    name = " ".join(filter(None, [name_1, name_2]))
    id_number = "".join(filter(None, [id_1, id_2]))
    id_number_english= convert_arabic_to_english(id_number)
    if id_number_english[0] == '2':
        year = '19' + id_number_english[1:3]
    else:
        year = '20' + id_number_english[1:3]

    month = id_number_english[3:5]
    day = id_number_english[5:7]
    birth_date = f"{year}/{month}/{day}"
    gender_digit = int(id_number_english[12:13])
    gender = 'male' if gender_digit % 2 else 'female'
    # 8. Return structured data
    return IDCardData(
        name=name,
        address=address,
        id_number=id_number,
        factory_number=factory_number,
        photo=photo_region,
        gender= gender,
        birth_date= birth_date,
        english_id_number=id_number_english)