# Amount of pixels within which drone should hold position in a given axis
CENTER_TOLERANCE_X = 50
CENTER_TOLERANCE_Y = 50

# Target area ratio: 0.01 means the tracked target should occupy 1% of the frame
TARGET_AREA_RATIO = 0.0005


def calculate_command(
    error_x,
    error_y,
    target_area_ratio
):
    if error_x < -CENTER_TOLERANCE_X:
        horizontal_command = "MOVE LEFT"
    elif error_x > CENTER_TOLERANCE_X:
        horizontal_command = "MOVE RIGHT"
    else:
        horizontal_command = "HOLD X"

    if error_y < -CENTER_TOLERANCE_Y:
        vertical_command = "MOVE UP"
    elif error_y > CENTER_TOLERANCE_Y:
        vertical_command = "MOVE DOWN"
    else:
        vertical_command = "HOLD Y"

    if target_area_ratio < TARGET_AREA_RATIO:
        distance_command = "APPROACH"
    else:
        distance_command = "HOLD DISTANCE"

    return (
        horizontal_command,
        vertical_command,
        distance_command
    )


def get_drone_command(
    error_x,
    error_y,
    target_area_ratio
):
    horizontal, vertical, distance = calculate_command(
        error_x,
        error_y,
        target_area_ratio
    )

    if (
        horizontal == "HOLD X"
        and vertical == "HOLD Y"
        and distance == "HOLD DISTANCE"
    ):
        command = "HOLD POSITION"
    else:
        command = (
            f"{horizontal} | "
            f"{vertical} | "
            f"{distance}"
        )

    return horizontal, vertical, distance, command
