#!/usr/bin/env python3

"""
** Deformation in perspective by 'quadrilateral'. **
----------------------------------------------------

dst(x, y) = src((M11x+M12y+M13)/(M31x+M32y+M33), (M21x+M22y+M23)/(M31x+M32y+M33))

The affine transformation is clearely describe in the cv2 documentation:
https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gaf73673a7e8e18ec6963e3774e6a94b87
"""


import cv2
import numpy as np

from deformation.base import Transform



def get_perspective_transform(src, dst):
    """
    ** Calculates a perspective transform from four pairs of the corresponding points. **

    Works the same as ``cv2.getPerspectiveTransform`` following the numpy(i,j) convention.

    Parameters
    ----------
    src : arraylike
        Coordinates of quadrangle vertices in the source image.
        The pairs (i, j) of points following the numpy convention.
    dst : arraylike
        Coordinates of the corresponding quadrangle vertices in the destination image.

    Returns
    -------
    matrix : np.ndarray
        The 3×3 matrix of a perspective transform. The M33 coefficient is always 1.

    Examples
    --------
    >>> import cv2
    >>> import numpy as np
    >>> from deformation.perspective import get_perspective_transform
    >>> input_pts = [[-200, 100], [-100, 800], [2200, -200], [2100, 1100]]
    >>> output_pts = [[0, 0], [0, 1000], [2000, 0], [2000, 1000]]
    >>> cv2.getPerspectiveTransform(np.float32(input_pts)[:, ::-1], np.float32(output_pts)[:, ::-1])
    array([[ 1.20762685e+00,  1.50953356e-01, -9.05720136e+01],
           [-2.05936366e-01,  1.44155456e+00,  3.08904550e+02],
           [-1.32740990e-04,  3.33730788e-04,  1.00000000e+00]])
    >>> get_perspective_transform(input_pts, output_pts)
    array([[ 1.44155456e+00, -2.05936366e-01,  3.08904550e+02],
           [ 1.50953356e-01,  1.20762685e+00, -9.05720136e+01],
           [ 3.33730788e-04, -1.32740990e-04,  1.00000000e+00]])
    >>> l1, l2, l3 = _
    >>> (m11, m12, m13), (m21, m22, m23), (m31, m32, m33) = l1, l2, l3
    >>> i, j = np.array(input_pts).T
    >>> np.int64(np.round((i*m11 + j*m12 + m13) / (i*m31 + j*m32 + m33)))
    array([   0,    0, 2000, 2000])
    >>> np.int64(np.round((i*m21 + j*m22 + m23) / (i*m31 + j*m32 + m33)))
    array([   0, 1000,    0, 1000])
    >>>

    Notes
    -----
    Unlike the CV2 function, this function compute in float64, not 32.
    """
    src = np.asarray(src, dtype=np.float64)
    dst = np.asarray(dst, dtype=np.float64)
    assert src.shape == dst.shape == (4, 2), (src.shape, dst.shape)

    system = np.vstack([
        [[i_s, j_s, 1, 0, 0, 0, -i_s*i_d, -j_s*i_d], [0, 0, 0, i_s, j_s, 1, -i_s*j_d, -j_s*j_d]]
        for (i_s, j_s), (i_d, j_d) in zip(src, dst)
    ])
    cst = np.vstack([[[i_d], [j_d]] for i_d, j_d in dst])
    cfs = np.linalg.inv(system) @ cst # system @ cfs = cst
    matrix = np.asarray([[cfs[0, 0], cfs[1, 0], cfs[2, 0]],
                         [cfs[3, 0], cfs[4, 0], cfs[5, 0]],
                         [cfs[6, 0], cfs[7, 0], 1     ]])
    return matrix


class PerspectiveTransform(Transform):
    r"""
    ** General perspective transformation. **

    \(
        dst(i, j) = src
        \left(
            \frac{M11 i + M12 j + M13}{M31 i + M32 j + 1},
            \frac{M21 i + M22 j + M23}{M31 i + M32 j + 1}
        \right)
    \)

    Examples
    --------
    >>> import numpy as np
    >>> from deformation.perspective import (
    ...     PerspectiveTransform, get_perspective_transform)
    >>>
    >>> input_pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> output_pts = [[.1, .2], [0, .8], [.9, -.1], [1.1, 1.1]]
    >>> matrix = get_perspective_transform(input_pts, output_pts)
    >>> PerspectiveTransform(matrix)
    PerspectiveTransform([[0.39, -0.1, 0.1], [-0.25, 0.45, 0.2], [-0.45, -0.19, 1.0]])
    >>> _.apply_points_trans(*np.float64(input_pts).T)
    (array([0.1, 0. , 0.9, 1.1]), array([ 0.2,  0.8, -0.1,  1.1]))
    >>>
    """

    def __init__(self, matrix, **kwargs):
        """
        Parameters
        ----------
        matrix : np.ndarray
            The 3x3 perspective transformation matrix in the numpy convention.
        **kwarg : dict
            Passed to initializers of parent classes.
        """
        matrix = np.asarray(matrix, dtype=np.float64)
        assert matrix.shape == (3, 3), matrix.shape
        assert matrix[2, 2] == 1, matrix

        self.matrix = matrix

        super().__init__(**kwargs)

    def __getstate__(self):
        return self.matrix, self.src_shape, self.dst_shape

    def __repr__(self):
        return (
            f'{self.__class__.__name__}'
            f'([{", ".join(map(str, map(list, np.round(self.matrix, 2))))}])'
        )

    def __setstate__(self, state):
        matrix, src_shape, dst_shape = state
        PerspectiveTransform.__init__(self, matrix, src_shape=src_shape, dst_shape=dst_shape)

    def _translation(self, dep_i, dep_j):
        self.matrix[0, :] += dep_i * self.matrix[2, :]
        self.matrix[1, :] += dep_j * self.matrix[2, :]

    def _reverse(self):
        """
        ** Returns the inverse transformation. **

        Examples
        --------
        >>> import numpy as np
        >>> from deformation.perspective import (
        ...     PerspectiveTransform, get_perspective_transform)
        >>>
        >>> input_pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        >>> output_pts = [[.1, .2], [0, .8], [.9, -.1], [1.1, 1.1]]
        >>> matrix = get_perspective_transform(input_pts, output_pts)
        >>> PerspectiveTransform(matrix)
        PerspectiveTransform([[0.39, -0.1, 0.1], [-0.25, 0.45, 0.2], [-0.45, -0.19, 1.0]])
        >>> _.reverse()
        PerspectiveTransform([[3.23, 0.54, -0.43], [1.09, 2.91, -0.69], [1.67, 0.8, 1.0]])
        >>> get_perspective_transform(output_pts, input_pts)
        array([[ 3.23003845,  0.53833974, -0.43067179],
               [ 1.09251301,  2.91336802, -0.6919249 ],
               [ 1.66930559,  0.79846189,  1.        ]])
        >>>
        """
        size = self.src_shape or [1, 1]
        src_points_i = np.asarray([0., 0., size[0], size[0]], dtype=np.float64)
        src_points_j = np.asarray([0., size[1], 0., size[1]], dtype=np.float64)
        src = np.vstack([src_points_i, src_points_j]).T
        dst_points_i, dst_points_j = self.apply_points_trans(src_points_i, src_points_j)
        dst = np.vstack([dst_points_i, dst_points_j]).T
        inv_matrix = get_perspective_transform(src=dst, dst=src)
        return PerspectiveTransform(inv_matrix, src_shape=self.dst_shape, dst_shape=self.src_shape)

    def warp_image_inv(self, image):
        """
        ** apply the inverse image transformation. **

        This function is optional, it just allows to be more efficient.
        """
        dsize = self.src_shape or list(image.shape)
        cv2_matrix = self.matrix[[1, 0, 2], :][:, [1, 0, 2]]
        return cv2.warpPerspective(
            image, cv2_matrix, dsize=dsize[::-1],
            flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_REPLICATE
        )

    def warp_points(self, points_i, points_j):
        """
        ** Apply direct transformation. **
        """
        points_i, points_j, denom = np.squeeze(np.moveaxis(
            np.expand_dims(self.matrix, 0) @ np.moveaxis(
                [[points_i], [points_j], [np.full_like(points_i, 1)]],
            -1, 0), 0, -1), 1)
        return points_i/denom, points_j/denom
