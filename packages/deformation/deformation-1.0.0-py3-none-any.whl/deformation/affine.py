#!/usr/bin/env python3

"""
** Used to manipulate affine transformations. **
------------------------------------------------

dst(x, y) = src(M11x+M12y+M13, M21x+M22y+M23)

The affine transformation is clearely describe in the cv2 documentation:
https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html
"""


import cv2
import numpy as np

from deformation.perspective import PerspectiveTransform


class AffineTransform(PerspectiveTransform):
    """
    ** General affine transformation. **

    Examples
    --------
    >>> import numpy as np
    >>> from deformation.affine import AffineTransform
    >>> i_src, j_src = np.meshgrid(np.arange(10), np.arange(10), indexing='ij')
    >>> AffineTransform([[1, 0, 2], [1, 2, -2]])
    AffineTransform([[1.0, 0.0, 2.0], [1.0, 2.0, -2.0]])
    >>> i_dst, j_dst = _.apply_points_trans(i_src, j_src)
    >>> i_dst
    array([[ 2,  2,  2,  2,  2,  2,  2,  2,  2,  2],
           [ 3,  3,  3,  3,  3,  3,  3,  3,  3,  3],
           [ 4,  4,  4,  4,  4,  4,  4,  4,  4,  4],
           [ 5,  5,  5,  5,  5,  5,  5,  5,  5,  5],
           [ 6,  6,  6,  6,  6,  6,  6,  6,  6,  6],
           [ 7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
           [ 8,  8,  8,  8,  8,  8,  8,  8,  8,  8],
           [ 9,  9,  9,  9,  9,  9,  9,  9,  9,  9],
           [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
           [11, 11, 11, 11, 11, 11, 11, 11, 11, 11]])
    >>> j_dst
    array([[-2,  0,  2,  4,  6,  8, 10, 12, 14, 16],
           [-1,  1,  3,  5,  7,  9, 11, 13, 15, 17],
           [ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18],
           [ 1,  3,  5,  7,  9, 11, 13, 15, 17, 19],
           [ 2,  4,  6,  8, 10, 12, 14, 16, 18, 20],
           [ 3,  5,  7,  9, 11, 13, 15, 17, 19, 21],
           [ 4,  6,  8, 10, 12, 14, 16, 18, 20, 22],
           [ 5,  7,  9, 11, 13, 15, 17, 19, 21, 23],
           [ 6,  8, 10, 12, 14, 16, 18, 20, 22, 24],
           [ 7,  9, 11, 13, 15, 17, 19, 21, 23, 25]])
    >>>
    """

    def __init__(self, matrix, **kwargs):
        """
        Parameters
        ----------
        matrix : np.ndarray
            The 2x3 affine transformation matrix in the numpy convention (i, j).
        **kwarg : dict
            Passed to initializers of parent classes.
        """
        matrix = np.asarray(matrix, dtype=np.float64)
        assert matrix.shape == (2, 3), matrix.shape

        matrix_33 = np.zeros((3, 3), dtype=matrix.dtype.type)
        matrix_33[:2, :] = matrix
        matrix_33[2, 2] = 1
        super().__init__(matrix_33, **kwargs)

    def __getstate__(self):
        return self.matrix[:2, :], self.src_shape, self.dst_shape

    def __repr__(self):
        return (
            f'{self.__class__.__name__}([{list(self.matrix[0])}, {list(self.matrix[1])}])'
        )

    def __setstate__(self, state):
        matrix, src_shape, dst_shape = state
        AffineTransform.__init__(self, matrix, src_shape=src_shape, dst_shape=dst_shape)

    def _reverse(self):
        """
        ** Returns the inverse transformation. **

        Examples
        --------
        >>> from deformation.affine import AffineTransform
        >>> AffineTransform([[1, .5, 0], [0, 2, 3]])
        AffineTransform([[1.0, 0.5, 0.0], [0.0, 2.0, 3.0]])
        >>> _.reverse()
        AffineTransform([[1.0, -0.25, 0.75], [0.0, 0.5, -1.5]])
        >>>
        """
        inv_matrix = np.linalg.inv(self.matrix)[:2, :]
        inv = self.__class__.__new__(self.__class__)
        AffineTransform.__init__(
            inv, inv_matrix, src_shape=self.dst_shape, dst_shape=self.src_shape
        )
        return inv

    def warp_image_inv(self, image):
        """
        ** apply the inverse image transformation. **

        This function is optional, it just allows to be more efficient.
        """
        dsize = self.src_shape or list(image.shape)
        cv2_matrix = np.asarray([[self.matrix[1, 1], self.matrix[1, 0], self.matrix[1, 2]],
                                 [self.matrix[0, 1], self.matrix[0, 0], self.matrix[0, 2]]])
        return cv2.warpAffine(
            image, cv2_matrix, dsize=dsize[::-1],
            flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_REPLICATE
        )
