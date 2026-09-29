import numpy as np
import cv2
from backend.app.core.logging import get_logger

logger= get_logger("Preprocessing Pipeline")
class CardPerspective:

    def order_points(self, points):
        points = points.reshape(4, 2)

        ordered = np.zeros((4, 2), dtype="float32")

        s = points.sum(axis=1)

        ordered[0] = points[np.argmin(s)]  # top-left
        ordered[2] = points[np.argmax(s)]  # bottom-right

        diff = np.diff(points, axis=1)

        ordered[1] = points[np.argmin(diff)]  # top-right
        ordered[3] = points[np.argmax(diff)]  # bottom-left
        logger.info(f"Ordered points for perspective transform: {ordered}")
        return ordered

    def four_point_transform(self, image, pts):
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)

        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

class ProcessCard:
    def get_fields(self, ordered_image_points):
        name_region_1 = ordered_image_points[ 80:138,250:580]
        name_region_2 = ordered_image_points[ 125:165,250:580]
        address_region = ordered_image_points[170:250, 320:580 ]
        id_number_region1 = ordered_image_points[ 270:350 , 240:370]
        id_number_region2 = ordered_image_points[ 270:350 , 368:580]
        photo_region = ordered_image_points[ 20:220,30:140]
        factory_number_region = ordered_image_points[ 330:360,20:220]
        logger.info(f"Extracted card fields with shapes: name_region_1: {name_region_1.shape}, name_region_2: {name_region_2.shape}, address_region: {address_region.shape}, id_number_region1: {id_number_region1.shape}, id_number_region2: {id_number_region2.shape}, photo_region: {photo_region.shape}, factory_number_region: {factory_number_region.shape}")
        return name_region_1, name_region_2, address_region, id_number_region1,id_number_region2, photo_region, factory_number_region

class CardDetector:

    def find_card_contour(self, contours, image_shape):

        image_area = image_shape[0] * image_shape[1]

        candidates = []

        for contour in contours:

            area = cv2.contourArea(contour)

            # Ignore tiny contours
            if area < 0.1 * image_area:
                continue


            perimeter = cv2.arcLength(contour, True)

            approx = cv2.approxPolyDP(contour,0.02 * perimeter,True )

            if len(approx) == 4:
                candidates.append((area, approx))

        if not candidates:
            return None

        # Largest quadrilateral
        candidates.sort(key=lambda x: x[0],reverse=True )
        logger.info(f"Found card contour with area: {candidates[0][0]} and points: {candidates[0][1]}")
        return candidates[0][1]