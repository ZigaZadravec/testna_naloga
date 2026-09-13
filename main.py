import cv2

from controller import get_drone_command
from debug_info import (
    select_target,
    calculate_errors,
    draw_tracking,
    draw_information,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT
)
from tracker import (
    find_features,
    track_points,
    get_target_area_ratio,
    update_roi,
    MIN_POINTS
)

VIDEO_PATH = "video.mp4"


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read first frame.")
        cap.release()
        return

    original_height, original_width = frame.shape[:2]
    print(f"Video resolution: {original_width} x {original_height}")

    image_center_x = original_width // 2
    image_center_y = original_height // 2

    roi = select_target(frame)
    if roi is None:
        print("No object selected.")
        cap.release()
        return

    x, y, w, h = roi
    print(f"Selected ROI: x={x}, y={y}, w={w}, h={h}")

    previous_gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    points = find_features(
        previous_gray,
        x,
        y,
        w,
        h
    )

    if points is None:
        print("Could not find feature points.")
        cap.release()
        return

    print(f"Initial feature points: {len(points)}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if points is not None and len(points) >= MIN_POINTS:
            points = track_points(
                previous_gray,
                current_gray,
                points
            )

            if points is not None:
                x, y, w, h = update_roi(
                    points,
                    w,
                    h,
                    original_width,
                    original_height
                )

                target_area_ratio = get_target_area_ratio(
                    points,
                    original_width,
                    original_height
                )
            else:
                target_area_ratio = 0.0
        else:
            target_area_ratio = 0.0

        object_center_x, object_center_y, error_x, error_y = (
            calculate_errors(
                x,
                y,
                w,
                h,
                image_center_x,
                image_center_y
            )
        )

        if points is not None and len(points) >= MIN_POINTS:
            (
                horizontal_command,
                vertical_command,
                distance_command,
                drone_command
            ) = get_drone_command(
                error_x,
                error_y,
                target_area_ratio
            )

        else:
            drone_command = "UNKNOWN"

        draw_tracking(
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
        )

        draw_information(
            frame,
            object_center_x,
            object_center_y,
            error_x,
            error_y,
            target_area_ratio,
            drone_command
        )

        display_frame = cv2.resize(
            frame,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        )

        cv2.imshow(
            "Sparse Optical Flow Tracking",
            display_frame
        )

        key = cv2.waitKey(30) & 0xFF

        if key == 27:
            break

        previous_gray = current_gray.copy()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
