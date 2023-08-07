#!/usr/bin/env python3

"""
** Simply and efficiently apply a warp chain to an image. **
------------------------------------------------------------

In general, this makes it possible to deform an image
in one direction and in the other but also to transfer boundins boxes from one space to another.
You only need to define a few methods to have access to all the transformations,
which considerably reduces the amount of code.
This module is based on opencv for performance issues.
But unlike opencv, this module deals with the following points:

* Transformation in both directions. *usefull for bounding-boxes*
* Translation to avoid cropping the image and automatic resizing to avoid borders.
* Simplification of the calculation when chaining transformations to avoid intermediate images.

Class diagram
-------------

.. figure:: http://python-docs.ddns.net/deformation/classes.png

Examples
--------
>>> import cv2, math
>>> import deformation
>>>
>>> image = cv2.imread('classes.png', cv2.IMREAD_GRAYSCALE)
>>> rot = deformation.Rotation(30*math.pi/180, src_shape=image.shape, crop_and_pad=True)
>>> rot
Rotation(deg2rad(30), center=(372, 1387))
>>> rot.reverse()
Rotation(deg2rad(-30), center=(372, 1387))
>>> example = rot.apply_img_trans(image)
>>> cv2.imwrite('example.png', example)
True
>>>

This gives the following result:

.. figure:: http://python-docs.ddns.net/deformation/example.png
"""

from deformation.base import (
    BaseTransform, Transform,
    IdentityTransform, InverseTransform,
)
from deformation.poly import PolyTransform
from deformation.perspective import PerspectiveTransform
from deformation.affine import AffineTransform
from deformation.rotation import Rotation
from deformation.doc import make_pdoc


__all__ = [
    'BaseTransform', 'Transform',
    'IdentityTransform', 'InverseTransform',
    'PolyTransform',
    'PerspectiveTransform',
    'AffineTransform',
    'Rotation',
]
__author__ = 'Robin RICHARD (robinechuca) <serveurpython.oz@gmail.com>'
__license__ = 'GNU Affero General Public License v3 or later (AGPLv3+)'
__pdoc__ = make_pdoc(__all__, locals())
__version__ = '1.0.0'
