
NAVIGATION_OBJECTS = {
    "person",
    "chair",
    "bottle",
    "car",
    "bicycle",
    "motorcycle",
    "bus",
    "truck",
    "bench",
    "dog",
    "cat"
}

CONFIDENCE_THRESHOLD = 0.40


def decide(detections, frame_width, frame_height):

    obstacles = [
        obj for obj in detections
        if obj["object"] in NAVIGATION_OBJECTS
        and obj["confidence"] >= CONFIDENCE_THRESHOLD
    ]

    if not obstacles:
        return {
            "action": "GO_FORWARD",
            "voice": "Path clear."
        }

    left_count = 0
    center_count = 0
    right_count = 0

    for obj in obstacles:
        if obj["position"] == "LEFT":
            left_count += 1
        elif obj["position"] == "CENTER":
            center_count += 1
        elif obj["position"] == "RIGHT":
            right_count += 1

    # Obstacle directly ahead
    if center_count > 0:

        if left_count == 0 and right_count == 0:
            return {
                "action": "STOP",
                "voice": "Obstacle ahead. Stop."
            }

        if left_count < right_count:
            return {
                "action": "MOVE_LEFT",
                "voice": "Obstacle ahead. Check left side."
            }

        elif right_count < left_count:
            return {
                "action": "MOVE_RIGHT",
                "voice": "Obstacle ahead. Check right side."
            }

        return {
            "action": "STOP",
            "voice": "Obstacles ahead. Stop."
        }

    # Obstacle on the left
    if left_count > 0 and right_count == 0:
        return {
            "action": "MOVE_RIGHT",
            "voice": "Obstacle on left. Check right side."
        }

    # Obstacle on the right
    if right_count > 0 and left_count == 0:
        return {
            "action": "MOVE_LEFT",
            "voice": "Obstacle on right. Check left side."
        }

    # Obstacles on both sides
    return {
        "action": "STOP",
        "voice": "Obstacles on both sides. Stop."
    }
