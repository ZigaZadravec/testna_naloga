import cv2
import numpy as np


MAX_CORNERS = 100
QUALITY_LEVEL = 0.3
MIN_DISTANCE = 7
MIN_POINTS = 3


def find_features(grayscale, x, y, w, h):
    mask = np.zeros_like(grayscale)

    cv2.rectangle(
        mask,
        (x, y),
        (x + w, y + h),
        255,
        -1
    )

    return cv2.goodFeaturesToTrack(
        grayscale,
        maxCorners=MAX_CORNERS,
        qualityLevel=QUALITY_LEVEL,
        minDistance=MIN_DISTANCE,
        mask=mask
    )


def track_points(previous_gray, current_gray, points):
    if points is None or len(points) < MIN_POINTS:
        return None

    new_points, status, _ = cv2.calcOpticalFlowPyrLK(
        previous_gray,
        current_gray,
        points,
        None
    )

    if new_points is None:
        return None

    good_new = new_points[status == 1]

    if len(good_new) < MIN_POINTS:
        return None

    return good_new.reshape(-1, 1, 2)


def get_point_bounds(points):
    coordinates = points.reshape(-1, 2)

    min_x = int(np.min(coordinates[:, 0]))
    max_x = int(np.max(coordinates[:, 0]))
    min_y = int(np.min(coordinates[:, 1]))
    max_y = int(np.max(coordinates[:, 1]))

    return min_x, max_x, min_y, max_y


def get_target_area_ratio(points, image_width, image_height):
    min_x, max_x, min_y, max_y = get_point_bounds(points)

    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)

    tracked_area = width * height
    image_area = image_width * image_height

    return tracked_area / image_area


def update_roi(
    points,
    roi_width,
    roi_height,
    image_width,
    image_height
):
    min_x, max_x, min_y, max_y = get_point_bounds(points)

    center_x = (min_x + max_x) // 2
    center_y = (min_y + max_y) // 2

    x = center_x - roi_width // 2
    y = center_y - roi_height // 2

    x = max(0, min(x, image_width - roi_width))
    y = max(0, min(y, image_height - roi_height))

    return x, y, roi_width, roi_height
