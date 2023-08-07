#!/usr/bin/env python3

"""
** Allows manipulation of rotations. **
---------------------------------------
"""


import math
import numbers

import numpy as np

from deformation.affine import AffineTransform


class Rotation(AffineTransform):
    """
    ** A rotation coupled with a change of scale. **

    Examples
    --------
    >>> import numpy as np
    >>> from deformation.rotation import Rotation
    >>> Rotation(np.pi/3, scale=2)
    Rotation(deg2rad(60), scale=2)
    >>> _.apply_points_trans([0., -1., 0.], [0., 0., 1.])
    (array([ 0.        , -1.        , -1.73205081]), array([ 0.        , -1.73205081,  1.        ]))
    >>>
    >>> Rotation(angle=np.deg2rad(20), scale=2, center=(0, 10)).reverse()
    Rotation(deg2rad(-20), scale=0.5, center=(0, 10))
    >>>
    """

    def __init__(self, angle=0, scale=1, center=(0, 0), **kwargs):
        """
        Parameters
        ----------
        angle : float
            The rotation angle in radian. Positive values mean counter-clockwise.
        scale : float
            The ratio of the distances from the destination image to the src image.
        center : tuple
            The coordinates of the center of rotation.
            If the 'pad_and_crop' option is activated,
            then the center of rotation is recalculated.
            The supplied value is then ignored.
            The convention used is the numpy convention (i, j).
        **kwargs : dict
            Passed to initializers of parent classes.
        """
        assert isinstance(angle, numbers.Number), angle.__class__.__name__
        assert isinstance(scale, numbers.Number), scale.__class__.__name__
        assert scale != 0
        assert hasattr(center, '__iter__'), f'{center} is not iterable'
        center = list(center)
        assert len(center) == 2, len(center)
        assert isinstance(center[0], numbers.Number), center[0].__class__.__name__
        assert isinstance(center[1], numbers.Number), center[1].__class__.__name__

        alpha = scale * math.cos(angle)
        beta = scale * math.sin(angle)
        matrix = [[alpha, -beta, (1-alpha)*center[0] + beta*center[1]],
                  [ beta, alpha, -beta*center[0] + (1-alpha)*center[1]]]
        super().__init__(matrix, **kwargs)

    def __repr__(self):
        angle, scale, center = self.angle, self.scale, self.center
        args = [
            f'deg2rad({round(180*angle/np.pi)})' if angle else None,
            f'scale={scale:.3g}' if scale != 1 else None,
            f'center=({round(center[0])}, {round(center[1])})' if center != (0, 0) else None,
        ]
        args = [a for a in args if a is not None]
        return f'{self.__class__.__name__}({", ".join(args)})'

    def __getstate__(self):
        return self.angle, self.scale, self.center

    def __setstate__(self, state):
        angle, scale, center = state
        Rotation.__init__(self, angle=angle, scale=scale, center=center)

    @property
    def angle(self):
        """
        ** The angle of rotation in radians counterclockwise. **
        """
        alpha = self.matrix[0, 0] / self.scale # cos(angle)
        beta = self.matrix[1, 0] # zoom * sin(angle)
        angle = math.acos(alpha) * np.sign(beta)
        return angle

    @property
    def center(self):
        """
        ** The center of rotation of the image. **
        """
        alpha = self.matrix[0, 0] # scale * cos(angle)
        beta = self.matrix[1, 0] # scale * sin(angle)
        mat_cen = np.asarray([[1-alpha, beta], [-beta, 1-alpha]]) # mat[:, 2] = mat_cen @ center
        try: # center = mat_center**-1 @ mat[:, 2]
            center = np.linalg.inv(mat_cen) @ [[self.matrix[0, 2]], [self.matrix[1, 2]]]
        except np.linalg.LinAlgError: # if angle == 0 and scale == 1
            center = (0, 0)
        else:
            center = (center[0, 0], center[1, 0])
        return center

    @property
    def scale(self):
        """
        ** The zoom factor. **
        """
        alpha = self.matrix[0, 1] # zoom * cos(angle)
        beta = self.matrix[0, 0] # zoom * sin(angle)
        zoom = math.sqrt(alpha**2 + beta**2) # cos**2 + sin**2 = 1
        return zoom
