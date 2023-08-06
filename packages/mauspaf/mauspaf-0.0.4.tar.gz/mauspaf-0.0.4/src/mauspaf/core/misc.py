""" Miscellaneous functions to support the mass properties calculations.
"""
import numpy as np


def rodrigues_rotation(vector, angle):
    """ Returns the Rodrigues' rotation matrix.

    Args:
        vector (list or numpy.ndarray): Rotation axis (3D vector).
        angle (float): Rotation angle (rad).

    Source:
      [1]: https://mathworld.wolfram.com/RodriguesRotationFormula.html

    """
    uv = np.array(vector / np.linalg.norm(vector))
    asm = np.array([[0, -uv[2], uv[1]],
                    [uv[2], 0, -uv[0]],
                    [-uv[1], uv[0], 0]])
    rotation_matrix = np.diag(np.ones(3)) + asm * np.sin(angle) \
        + asm @ asm * (1 - np.cos(angle))
    return rotation_matrix
