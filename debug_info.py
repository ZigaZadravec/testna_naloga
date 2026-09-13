import cv2

from tracker import MIN_POINTS, get_point_bounds


DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720


def select_target(frame):
    display_frame = cv2.resize(
        frame,
        (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    )

    bbox = cv2.selectROI(
        "Select target",
        display_frame,
        fromCenter=False,
        showCrosshair=True
    )

    cv2.destroyWindow("Select target")

    x, y, w, h = bbox

    if w == 0 or h == 0:
        return None

    original_height, original_width = frame.shape[:2]

    scale_x = original_width / DISPLAY_WIDTH
    scale_y = original_height / DISPLAY_HEIGHT

    x = int(x * scale_x)
    y = int(y * scale_y)
    w = int(w * scale_x)
    h = int(h * scale_y)

    return x, y, w, h


def calculate_errors(
    x,
    y,
    w,
    h,
    image_center_x,
    image_center_y
):
    object_center_x = x + w // 2
    object_center_y = y + h // 2

    error_x = object_center_x - image_center_x
    error_y = object_center_y - image_center_y

    return (
        object_center_x,
        object_center_y,
        error_x,
        error_y
    )


def get_text_color(frame, x, y, width=500, height=30):
    frame_height, frame_width = frame.shape[:2]

    x1 = max(0, x)
    y1 = max(0, y - height + 5)
    x2 = min(frame_width, x + width)
    y2 = min(frame_height, y + 5)

    region = frame[y1:y2, x1:x2]

    if region.size == 0:
        return (255, 255, 255)

    gray = cv2.cvtColor(
        region,
        cv2.COLOR_BGR2GRAY
    )

    brightness = gray.mean()

    if brightness < 128:
        return (255, 255, 255)

    return (0, 0, 0)


def draw_tracking(
    frame,
    x,
    y,
    w,
    h,
    points,
    object_center_x,
    object_center_y,
    image_center_x,
    image_center_y
):
    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        3
    )

    if points is not None and len(points) >= MIN_POINTS:
        min_x, max_x, min_y, max_y = get_point_bounds(points)

        point_center_x = (min_x + max_x) // 2
        point_center_y = (min_y + max_y) // 2

        cv2.rectangle(
            frame,
            (min_x, min_y),
            (max_x, max_y),
            (255, 0, 255),
            2
        )

        cv2.circle(
            frame,
            (point_center_x, point_center_y),
            7,
            (0, 255, 0),
            -1
        )

        for point in points:
            px, py = point.ravel()

            cv2.circle(
                frame,
                (int(px), int(py)),
                4,
                (0, 0, 255),
                -1
            )

    cv2.circle(
        frame,
        (object_center_x, object_center_y),
        8,
        (255, 0, 0),
        -1
    )

    cv2.circle(
        frame,
        (image_center_x, image_center_y),
        8,
        (0, 255, 255),
        -1
    )

    cv2.line(
        frame,
        (object_center_x, object_center_y),
        (image_center_x, image_center_y),
        (255, 0, 255),
        2
    )


def draw_information(
    frame,
    object_center_x,
    object_center_y,
    error_x,
    error_y,
    target_area_ratio,
    drone_command
):
    lines = [
        f"Object center: ({object_center_x}, {object_center_y})",
        f"Error X: {error_x}  Error Y: {error_y}",
        f"Target area: {target_area_ratio * 100:.2f}%",
        f"COMMAND: {drone_command}"
    ]

    y_positions = [40, 70, 110, 145]

    for text, y in zip(lines, y_positions):
        text_color = get_text_color(
            frame,
            20,
            y
        )

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8 if y != 145 else 0.7,
            text_color,
            2
        )
