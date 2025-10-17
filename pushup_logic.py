import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle (in degrees) between three 2D points a, b, and c.

    Parameters:
    a, b, c (list/tuple): Coordinates [x, y] for the three points.
                           b is the vertex (the elbow joint, hip, or knee).

    Returns:
    float: The angle in degrees.
    """
    # Convert points to NumPy arrays for vectorized math
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point (Vertex)
    c = np.array(c)  # End point

    # Calculate the angle using arctan2
    # atan2 gives the angle of a vector from the positive x-axis.
    # We subtract the angles of the two vectors (BA and BC) relative to the x-axis.
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(np.degrees(radians))

    # Ensure the angle is the interior angle (less than 180 degrees)
    if angle > 180.0:
        angle = 360 - angle

    return angle
