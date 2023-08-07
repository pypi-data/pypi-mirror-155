#!/usr/bin/env python3

"""
** Performs extensive tests on image transformations. **
--------------------------------------------------------
"""


import pickle
import time

import context_verbose
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytest

from deformation.base import Transform
from deformation.poly import TorchPoly, PolyTransform
from deformation.perspective import PerspectiveTransform, get_perspective_transform
from deformation.affine import AffineTransform
from deformation.rotation import Rotation


DISPLAY = False
IMG = cv2.imread('data_example/validation/x02.jpg', cv2.IMREAD_GRAYSCALE)



def apply_direct_and_reverse_img(trans, *, src_img=IMG):
    """
    ** Applies the transformation to the images. **

    Parameters
    ----------
    trans : Transform
        The transformation function.
    src_img : np.ndarray
        The source picture.

    Returns
    -------
    src_img : np.ndarray
        The original picture.
    trans_img : np.ndarray
        The directe transformation of the input image.
    bis_img : np.ndarray
        The reverse of the directe transformation (identity).
    """
    assert isinstance(trans, Transform), trans.__class__.__name__
    assert isinstance(src_img, np.ndarray), src_img.__class__.__name__
    assert 2 <= src_img.ndim <= 3, src_img.shape

    with context_verbose.printer(f'Apply image {trans}...'):
        if DISPLAY:
            plt.title(repr(trans))
            plt.subplot(1, 3, 1)
            plt.title('original')
            plt.imshow(src_img, cmap='gray')
        t_1 = time.time()
        trans_img = trans.apply_img_trans(src_img)
        t_2 = time.time()
        context_verbose.printer.print(f'img direct {1000*(t_2-t_1):.2f} ms')
        if DISPLAY:
            plt.subplot(1, 3, 2)
            plt.title('direct_trans(original)')
            plt.imshow(trans_img, cmap='gray')
        t_1 = time.time()
        bis_img = trans.reverse().apply_img_trans(trans_img)
        t_2 = time.time()
        context_verbose.printer.print(f'img reverse {1000*(t_2-t_1):.2f} ms')
        if DISPLAY:
            plt.subplot(1, 3, 3)
            plt.title('inv_trans(direct_trans(original))')
            plt.imshow(bis_img, cmap='gray')
            plt.show()

    return src_img, trans_img, bis_img

def check_points_bij(trans, *, boundaries=(-1, 1, -1, 1)):
    """
    ** Apply a direct and inverse transformation to a set of points. **

    Parameters
    ----------
    boundaries : tuple
        The limits imin, imax, jmin and jmax.
    """
    i_points, j_points = np.meshgrid(
        np.linspace(boundaries[0], boundaries[1], 21, dtype=np.float64),
        np.linspace(boundaries[2], boundaries[3], 21, dtype=np.float64),
        indexing='ij'
    )
    i_trans, j_trans = trans.apply_points_trans(i_points, j_points)
    i_final, j_final = trans.reverse().apply_points_trans(i_trans, j_trans)
    assert np.all(np.abs(i_points - i_final) < 1e-3), np.max(np.abs(i_points - i_final))
    assert np.all(np.abs(j_points - j_final) < 1e-3), np.max(np.abs(j_points - j_final))

def check_pickle(trans):
    """
    ** Looks if the object is grately pickelable. **
    """
    repr_trans = repr(trans)
    trans_bis = pickle.loads(pickle.dumps(trans))
    repr_trans_bis = repr(trans_bis)
    assert repr_trans == repr_trans_bis
    assert trans.__class__ == trans_bis.__class__

def test_missing_definition():
    """
    ** Examples of tests where the user does not define enough methods. **
    """
    class Neant(Transform):
        """Transformation not sufficiently defined."""

    neant = Neant()
    with pytest.raises(NotImplementedError):
        apply_direct_and_reverse_img(neant)


class General(Transform):
    """General example."""
    def warp_points(self, points_i, points_j):
        return points_i + np.cos(points_j), points_j
    def warp_points_inv(self, points_i, points_j):
        return points_i - np.cos(points_j), points_j


def test_general():
    """
    ** Testing arbitrary transformation examples. **
    """
    general = General()
    check_points_bij(general)
    check_pickle(general)

def test_poly():
    """
    ** Performs tests on the polynomials. **
    """
    id_poly = PolyTransform(src_shape=IMG.shape)
    poly_i = TorchPoly(2)
    poly_i[1, 0] = .5
    poly_i[0, 0] = -.1
    poly_i[0, 2] = .2
    simple_poly = PolyTransform(poly_i=poly_i, src_shape=IMG.shape)
    simple_poly_n = PolyTransform(poly_i=poly_i, src_shape=IMG.shape, crop_and_pad=True)
    poly_j = TorchPoly(3)
    poly_j[0, 1] = .5
    poly_j[1, 1] = .15
    complex_poly = PolyTransform(poly_i=poly_i, poly_j=poly_j, src_shape=IMG.shape)
    complex_poly_n = PolyTransform(
        poly_i=poly_i, poly_j=poly_j, src_shape=IMG.shape, crop_and_pad=True
    )
    for poly in [id_poly, simple_poly, simple_poly_n, complex_poly, complex_poly_n]:
        src, _, dst = apply_direct_and_reverse_img(poly)
        assert src.shape == dst.shape
        check_pickle(poly)

def test_perspective():
    """
    ** Performs tests on the polynomials. **
    """
    shape = IMG.shape
    input_pts = [[0, 0], [0, shape[1]], [shape[0], 0], [shape[0], shape[1]]]
    output_pts = [[700, 0], [500, 600], [2300, -300], [2700, 900]]
    id_trans = PerspectiveTransform(get_perspective_transform(input_pts, input_pts))
    matrix = get_perspective_transform(input_pts, output_pts)
    complex_trans = PerspectiveTransform(matrix)
    complex_trans_n = PerspectiveTransform(matrix.copy(), src_shape=IMG.shape, crop_and_pad=True)

    for trans in [id_trans, complex_trans, complex_trans_n]:
        src, _, dst = apply_direct_and_reverse_img(trans)
        assert src.shape == dst.shape
        check_points_bij(trans, boundaries=(0, shape[0], 0, shape[1]))
        check_pickle(trans)

def test_affine():
    """
    ** Perfoms tests on the affine transformation. **
    """
    id_trans = AffineTransform([[1, 0, 0], [0, 1, 0]])
    complex_trans = AffineTransform([[1, .1, 500], [.2, 1, -200]])
    complex_trans_n = AffineTransform(
        [[1, .1, 500], [.2, 1, -200]], src_shape=IMG.shape, crop_and_pad=True
    )

    for trans in [id_trans, complex_trans, complex_trans_n]:
        src, _, dst = apply_direct_and_reverse_img(trans)
        assert src.shape == dst.shape
        check_points_bij(trans)
        check_pickle(trans)

def test_rotation():
    """
    ** Performs tests on the rotation transformation. **
    """
    id_trans = Rotation()
    complex_trans = Rotation(np.deg2rad(20), scale=.5)
    complex_trans_n = Rotation(np.deg2rad(20), scale=.5, src_shape=IMG.shape, crop_and_pad=True)

    for trans in [id_trans, complex_trans, complex_trans_n]:
        src, _, dst = apply_direct_and_reverse_img(trans)
        assert src.shape == dst.shape
        check_points_bij(trans)
        check_pickle(trans)


if __name__ == '__main__':
    DISPLAY = True

    with context_verbose.printer('Transformation Tests...'):
        for name, test_func in locals().copy().items():
            if name.startswith('test_rot'):
                context_verbose.printer.print(name)
                test_func()
