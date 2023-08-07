
******************************************************
Simply and efficiently apply a warp chain to an image!
******************************************************


Description
-----------

This module is based on opencv for performance issues.
But unlike opencv, this module deals with the following points:

* Transformation in both directions. *usefull for bounding-boxes*
* Translation to avoid cropping the image and automatic resizing to avoid borders.
* Simplification of the calculation when chaining transformations to avoid intermediate images.

Basic example
-------------

.. code:: python

    >>> import deformation
    >>> deformation.Rotation(30*math.pi/180, src_shape=image.shape, crop_and_pad=True)
    Rotation(deg2rad(30), center=(372, 1387))
    >>> _.reverse()
    Rotation(deg2rad(-30), center=(372, 1387))
    >>>

* See the `documentation <http://python-docs.ddns.net/deformation/>`_ for more details and examples.
