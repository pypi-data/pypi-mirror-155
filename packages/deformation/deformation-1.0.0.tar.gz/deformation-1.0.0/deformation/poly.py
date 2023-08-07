#!/usr/bin/env python3

"""
** Polynomial transformation of order n. **
-------------------------------------------

dst(i, j) = src(poly_i(i, j), poly_y(i, j))
"""


import numbers

import sympy
import torch

from deformation.base import Transform



class TorchPoly(torch.nn.Module):
    r"""
    ** Polynomial surface. **

    \(
        P(i, j) = \sum\limits_{k=0}^N{
            \sum\limits_{l=0}^N{
                \alpha_{kl} i^k j^l
            }
        }
    \)

    Attributes
    ----------
    coeffs : torch.Tensor
        The matrix of the polynomial coeficients.
    order : int
        The order of the polynomial.

    Examples
    --------
    >>> import torch
    >>> from deformation.poly import TorchPoly
    >>> poly = TorchPoly(order=3)
    >>> i, j = torch.meshgrid(torch.arange(
    ...     4, dtype=torch.float32), torch.arange(4, dtype=torch.float32), indexing='ij')
    >>> i
    tensor([[0., 0., 0., 0.],
            [1., 1., 1., 1.],
            [2., 2., 2., 2.],
            [3., 3., 3., 3.]])
    >>> j
    tensor([[0., 1., 2., 3.],
            [0., 1., 2., 3.],
            [0., 1., 2., 3.],
            [0., 1., 2., 3.]])
    >>> poly.coeffs = torch.nn.Parameter(torch.tensor([[1., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.]]))
    >>> poly(i, j) # out = 1 * i**0*j**0
    tensor([[1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]], grad_fn=<SumBackward1>)
    >>> poly.coeffs = torch.nn.Parameter(torch.tensor([[0., 0., 0., 0.],
    ...                                                [1., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [1., 0., 0., 0.]]))
    >>> poly(i, j) # out = 1 * i**1*j**0 + 1 * i**3*j**0
    tensor([[ 0.,  0.,  0.,  0.],
            [ 2.,  2.,  2.,  2.],
            [10., 10., 10., 10.],
            [30., 30., 30., 30.]], grad_fn=<SumBackward1>)
    >>> poly.coeffs = torch.nn.Parameter(torch.tensor([[0., 1., 0., 1.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.]]))
    >>> poly(i, j) # out = 1 * i**0*j**1 + 1 * i**0*j**3
    tensor([[ 0.,  2., 10., 30.],
            [ 0.,  2., 10., 30.],
            [ 0.,  2., 10., 30.],
            [ 0.,  2., 10., 30.]], grad_fn=<SumBackward1>)
    >>> poly.coeffs = torch.nn.Parameter(torch.tensor([[0., 0., 0., 0.],
    ...                                                [0., 0., 0., 0.],
    ...                                                [0., 0., 1., 0.],
    ...                                                [0., 0., 0., 0.]]))
    >>> poly(i, j) # out = 1 * i**2*j**2
    tensor([[ 0.,  0.,  0.,  0.],
            [ 0.,  1.,  4.,  9.],
            [ 0.,  4., 16., 36.],
            [ 0.,  9., 36., 81.]], grad_fn=<SumBackward1>)
    >>>

    Notes
    -----
    Input/output is not checked because this class
    is not intended to be directly used by the user.
    It is an internal variable which allows to help the detortion of the image.
    """

    def __init__(self, order):
        """
        Parameters
        ----------
        order : int
            The order of the polynomial, ie the highest power.
            So there are ``(order+1)**2`` parameters in the model.
        """
        assert isinstance(order, numbers.Integral), order.__class__.__name__
        assert order > 0

        super().__init__()

        self.coeffs = torch.nn.Parameter(torch.zeros((order+1), (order+1)), requires_grad=False)
        power = torch.arange(order+1, device=self.coeffs.device, dtype=self.coeffs.dtype)
        i_power, j_power = torch.meshgrid(power, power, indexing='ij')
        self.i_power, self.j_power = i_power.ravel(), j_power.ravel()

    def __getstate__(self):
        """
        ** Retrieve the coefficients. **
        """
        return self.coeffs.detach().cpu().clone(), self.coeffs.requires_grad, self.coeffs.device

    def __repr__(self):
        """
        ** Offers meaningful but non-evaluable representation. **

        Examples
        --------
        >>> from deformation.poly import TorchPoly
        >>> TorchPoly(order=3)
        TorchPoly(0)
        >>> _[0, 0] = 1
        >>> _
        TorchPoly(1.00000000000000)
        >>> _[1, 0] = 2
        >>> _
        TorchPoly(2.0*i + 1.0)
        >>> _[0, 3] = 3
        >>> _
        TorchPoly(2.0*i + 3.0*j**3 + 1.0)
        >>> _[2, 2] = -1
        >>> _
        TorchPoly(-1.0*i**2*j**2 + 2.0*i + 3.0*j**3 + 1.0)
        >>>
        """
        i_sym, j_sym = sympy.symbols('i j', real=True)
        expr = sum(
            self.coeffs.detach().cpu().numpy().ravel()
            * i_sym**self.i_power.detach().cpu().numpy().astype(int)
            * j_sym**self.j_power.detach().cpu().numpy().astype(int)
        )
        return f'{self.__class__.__name__}({expr})'

    def __setitem__(self, item, value):
        """
        ** Simplifies the handling of coeffs by avoiding the ``RuntimeError`` error. **

        Syntax shortcut for ``self[item] = value``.
        Because ``self.coeffs[item] = value`` raises:
        RuntimeError: a view of a leaf Variable that requires grad
        is being used in an in-place operation.

        Examples
        --------
        >>> from deformation.poly import TorchPoly
        >>> poly = TorchPoly(order=3)
        >>> poly.coeffs
        Parameter containing:
        tensor([[0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.]])
        >>> poly[0, 0] = 1
        >>> poly.coeffs
        Parameter containing:
        tensor([[1., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 0., 0.]])
        >>>
        """
        coeffs_copy = self.coeffs.detach()
        coeffs_copy[item] = value
        self.coeffs = torch.nn.Parameter(coeffs_copy, requires_grad=self.coeffs.requires_grad)

    def __setstate__(self, state):
        """
        ** Reinjects the coefficients. **
        """
        coeffs, requires_grad, device = state
        TorchPoly.__init__(self, coeffs.shape[0]-1)
        self.coeffs = torch.nn.Parameter(
            coeffs.to(device=device), requires_grad=requires_grad
        )

    def copy(self):
        """
        ** Returns a clone of the polynomial. **

        Examples
        --------
        >>> from deformation.poly import TorchPoly
        >>> poly = TorchPoly(1)
        >>> poly[1, 0] = 1
        >>> poly
        TorchPoly(1.0*i)
        >>> poly_bis = poly.copy()
        >>> poly_bis
        TorchPoly(1.0*i)
        >>> poly_bis[0, 1] = 1
        >>> poly_bis
        TorchPoly(1.0*i + 1.0*j)
        >>> poly # not modified
        TorchPoly(1.0*i)
        >>>
        """
        poly_copy = TorchPoly(order=self.order)
        poly_copy.__setstate__(self.__getstate__())
        return poly_copy

    def diff(self, axis):
        r"""
        ** Returns the first derivative of the polynomial on an axis. **

        \(
            \frac{\partial P(i, j)}{\partial i} =
            \frac{\partial \sum\limits_{k=0}^N\sum\limits_{l=0}^N \alpha_{kl} i^k j^l}{\partial i} =
            \sum\limits_{k=1}^N\sum\limits_{l=0}^N k \alpha_{kl} i^{k-1} j^l =
            \sum\limits_{k=0}^{N-1}\sum\limits_{l=0}^N (k+1) \alpha_{k+1,l} i^k j^l =
            \sum\limits_{k=0}^N\sum\limits_{l=0}^N \beta_{kl} i^k j^l
        \)

        or

        \(
            \frac{\partial P(i, j)}{\partial j} =
            \frac{\partial \sum\limits_{k=0}^N\sum\limits_{l=0}^N \alpha_{kl} i^k j^l}{\partial j} =
            \sum\limits_{k=0}^N\sum\limits_{l=1}^N l \alpha_{kl} i^k j^{l-1} =
            \sum\limits_{k=0}^N\sum\limits_{l=0}^{N-1} (l+1) \alpha_{k,l+1} i^k j^l =
            \sum\limits_{k=0}^N\sum\limits_{l=0}^N \beta_{kl} i^k j^l
        \)

        according to the chosen axis

        Parameters
        ----------
        axis : str
            'i' or 'j', the derivation variable.

        Returns
        -------
        TorchPoly
            The polynomial \(P^{\prime}\), derives from ``self`` along the ``axis`` axis.

        Examples
        --------
        >>> import torch
        >>> from deformation.poly import TorchPoly
        >>> poly = TorchPoly(order=4)
        >>> poly[:, :] = torch.tensor([[1., 0., 0., 2., 0.],
        ...                            [0., 0., 0., 0., 0.],
        ...                            [0., 0., 1., 0., 0.],
        ...                            [0., 0., 0., 0., 0.],
        ...                            [2., 0., 0., 0., 0.]])
        >>> poly
        TorchPoly(2.0*i**4 + 1.0*i**2*j**2 + 2.0*j**3 + 1.0)
        >>> poly.diff('i')
        TorchPoly(8.0*i**3 + 2.0*i*j**2)
        >>> poly.diff('i').diff('i')
        TorchPoly(24.0*i**2 + 2.0*j**2)
        >>> poly.diff('j')
        TorchPoly(2.0*i**2*j + 6.0*j**2)
        >>>
        """
        assert isinstance(axis, str), axis.__class__.__name__
        assert axis in {'i', 'j'}, axis

        diff = TorchPoly(order=self.order)
        ref_coeffs = self.coeffs if axis == 'i' else self.coeffs.T

        coeffs = torch.zeros_like(diff.coeffs)
        coeffs[:-1, :] = (
            ref_coeffs * torch.arange(
                diff.coeffs.shape[0],
                device=diff.coeffs.device,
                dtype=diff.coeffs.dtype
            ).reshape(-1, 1)
        )[1:, :]
        diff.coeffs = torch.nn.Parameter(coeffs)

        if axis == 'j':
            diff.coeffs = torch.nn.Parameter(diff.coeffs.T)
        return diff

    def forward(self, i_tensor, j_tensor):
        """
        ** Eval the surface at the positions i and j. **

        Returns
        -------
        z_tensor : torch.Tensor
            The evaluation of the function at the given points.
            The shape is the same as input.
        """
        return torch.sum(
            (
                self.coeffs.ravel().unsqueeze(0)
                * i_tensor.unsqueeze(-1)**self.i_power.unsqueeze(0)
                * j_tensor.unsqueeze(-1)**self.j_power.unsqueeze(0)
            ),
            axis=-1
        )

    @property
    def order(self):
        """
        ** The polynomial order. **
        """
        return self.coeffs.shape[0] - 1


class PolyTransform(torch.nn.Module, Transform):
    """
    ** Any polynomial transformation. **

    Attributes
    ----------
    poly_i : TorchPoly
        The provide polynomial.
    poly_j : TorchPoly
        The provide polynomial.

    Examples
    --------
    >>> from deformation.poly import TorchPoly, PolyTransform
    >>> poly_i = TorchPoly(2)
    >>> poly_i[0, 2] = 1
    >>> PolyTransform(poly_i=poly_i, src_shape=(1, 4))
    PolyTransform(TorchPoly(1.0*j**2), TorchPoly(1.0*j))
    >>> _.apply_points_trans([0., 0., 0., 0., 0.], [0., 1., 2., 3., 4.])
    (array([1.   , 0.625, 0.5  , 0.625, 1.   ]), array([0., 1., 2., 3., 4.]))
    >>>
    """

    def __init__(self, poly_i=None, poly_j=None, src_shape=None, **kwargs):
        """
        Parameters
        ----------
        poly_i : TorchPoly
            The deformation field along the i axis.
        poly_j : TorchPoly
            The deformation field along the j axis.
        src_shape : tuple
            See ``deformation.base.BaseTransform``.
            This parameter is essential because the coordinates
            of the image are brought back between -1 and 1 to limit the risk of divergence.
        **kwarg : dict
            Passed to initializers of parent transformation classes.
        """
        if poly_i is None:
            poly_i = TorchPoly(order=1)
            poly_i[1, 0] = 1
        if poly_j is None:
            poly_j = TorchPoly(order=1)
            poly_j[0, 1] = 1
        assert isinstance(poly_i, TorchPoly), poly_i.__class__.__name__
        assert isinstance(poly_j, TorchPoly), poly_j.__class__.__name__
        assert src_shape is not None, 'you must provide this value'

        torch.nn.Module.__init__(self)

        self.poly_i = poly_i.copy()
        self.poly_j = poly_j.copy()

        Transform.__init__(self, src_shape=src_shape, **kwargs)

    def __getstate__(self):
        return self.poly_i, self.poly_j, self.src_shape, self.dst_shape

    def __repr__(self):
        return f'{self.__class__.__name__}({self.poly_i}, {self.poly_j})'

    def __setstate__(self, state):
        poly_i, poly_j, src_shape, dst_shape = state
        PolyTransform.__init__(self, poly_i, poly_j, src_shape=src_shape, dst_shape=dst_shape)

    def _translation(self, dep_i, dep_j):
        dep_rel_i, dep_rel_j = 2*dep_i/self.src_shape[0], 2*dep_j/self.src_shape[1]
        self.poly_i[0, 0] = self.poly_i.coeffs[0, 0] + dep_rel_i
        self.poly_j[0, 0] = self.poly_j.coeffs[0, 0] + dep_rel_j

    def forward(self, field_i, field_j):
        """
        ** Like 'apply_points_trans' but differentiable torch. **

        Parameters
        ----------
        field_i : torch.Tensor
            The coordinates along the i axis.
        field_j : torch.Tensor
            The coordinates along the j axis.

        Returns
        -------
        out_fields : tuple
            The fields of the new i and j values.
        """
        assert isinstance(field_i, torch.Tensor), field_i.__class__.__name__
        assert isinstance(field_j, torch.Tensor), field_j.__class__.__name__
        return self.poly_i(field_i, field_j), self.poly_j(field_i, field_j)

    def _reverse(self, *, order=None):
        """
        ** Approximation of the inverse field by minimisation of reverse distance. **

        Parameters
        ----------
        order : int
            The order of the reversed polynomes. By default, the same order is used.

        Returns
        -------
        PolyTransform
            An approximation of the inverse deformation field.

        Examples
        --------
        >>> from torch import tensor
        >>> from torch.nn import Parameter
        >>> from deformation.poly import TorchPoly, PolyTransform
        >>> poly_i = TorchPoly(2)
        >>> poly_j = TorchPoly(2)
        >>> poly_i[...] = tensor([[0., 0., .5],
        ...                       [1., 0., 0.],
        ...                       [0., 0., 0.]])
        >>> poly_j[...] = tensor([[0., 1., 0.],
        ...                       [0., 0., 0.],
        ...                       [.5, 0., 0.]])
        >>> trans = PolyTransform(poly_i, poly_j, src_shape=(1, 1))
        >>> i_src, j_src = torch.meshgrid(
        ...     torch.linspace(-1, 1, 5),
        ...     torch.linspace(-1, 1, 5),
        ...     indexing='ij')
        >>> i_dst, j_dst = trans(i_src, j_src)
        >>> i_fin, j_fin = trans._reverse(order=1)(i_dst, j_dst)
        >>> i_fin
        tensor([[-0.6231, -0.9794, -1.1098, -1.0058, -0.6590],
                [-0.1630, -0.5106, -0.6343, -0.5257, -0.1765],
                [ 0.2898, -0.0511, -0.1689, -0.0550,  0.2988],
                [ 0.7437,  0.4074,  0.2949,  0.4146,  0.7751],
                [ 1.2072,  0.8733,  0.7653,  0.8917,  1.2610]])
        >>> j_fin
        tensor([[-0.6231, -0.1630,  0.2898,  0.7437,  1.2072],
                [-0.9794, -0.5106, -0.0511,  0.4074,  0.8733],
                [-1.1098, -0.6343, -0.1689,  0.2949,  0.7653],
                [-1.0058, -0.5257, -0.0550,  0.4146,  0.8917],
                [-0.6590, -0.1765,  0.2988,  0.7751,  1.2610]])
        >>> i_fin, j_fin = trans._reverse(order=2)(i_dst, j_dst)
        >>> i_fin
        tensor([[-0.8030, -1.0027, -0.9553, -0.9339, -1.1798],
                [-0.4167, -0.5578, -0.5394, -0.4772, -0.5097],
                [-0.0148, -0.0195, -0.0150,  0.0261,  0.0848],
                [ 0.4200,  0.5234,  0.4937,  0.4805,  0.5970],
                [ 1.0020,  1.0756,  0.9494,  0.8703,  1.0901]])
        >>> i_fin, j_fin = trans._reverse(order=3)(i_dst, j_dst)
        >>> i_fin
        tensor([[-0.8546, -0.9852, -0.9846, -1.0273, -0.9549],
                [-0.4799, -0.5408, -0.5033, -0.4925, -0.5332],
                [ 0.0065,  0.0030,  0.0159,  0.0087,  0.0054],
                [ 0.5365,  0.4978,  0.4948,  0.4797,  0.5529],
                [ 0.9926,  1.0516,  1.0332,  0.9646,  0.9879]])
        >>>
        """
        if order is None:
            order = max(self.poly_i.order, self.poly_j.order)
        assert isinstance(order, numbers.Integral), order.__class__.__name__
        assert order > 0

        # creation of the new polynomials
        q_i = TorchPoly(order)
        q_i[0, 0] = -self.poly_i.coeffs[0, 0]
        q_i[1, 0] = 1 / self.poly_i.coeffs[1, 0]
        q_i.coeffs.requires_grad = True
        q_j = TorchPoly(order)
        q_j[0, 0] = -self.poly_j.coeffs[0, 0]
        q_j[0, 1] = 1 / self.poly_j.coeffs[0, 1]
        q_j.coeffs.requires_grad = True

        # precomputing
        i_src_rel, j_src_rel = torch.meshgrid(
            torch.linspace(-1, 1, 21),
            torch.linspace(-1, 1, 21),
            indexing='ij',
        )
        i_dst_rel = (
            (self.src_shape[0]*(1 + self.poly_i(i_src_rel, j_src_rel)) - self.dst_shape[0])
            / self.dst_shape[0]
        )
        j_dst_rel = (
            (self.src_shape[1]*(1 + self.poly_j(i_src_rel, j_src_rel)) - self.dst_shape[1])
            / self.dst_shape[1]
        )

        # fit for minimize the loss
        optimizer = torch.optim.Adam([q_i.coeffs, q_j.coeffs], lr=5e-3)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=.5, patience=3)
        for _ in range(400*order):
            loss_i = torch.mean(
                (
                    (self.dst_shape[0]*(1 + q_i(i_dst_rel, j_dst_rel)) - self.src_shape[0])
                    / self.src_shape[0]
                    - i_src_rel
                )**2
            )
            loss_j = torch.mean(
                (
                    (self.dst_shape[1]*(1 + q_j(i_dst_rel, j_dst_rel)) - self.src_shape[1])
                    / self.src_shape[1]
                    - j_src_rel
                )**2
            )
            loss = loss_i + loss_j
            scheduler.step(loss)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_([q_i.coeffs, q_j.coeffs], 1)
            optimizer.step()
            # print(loss.item(), optimizer.param_groups[0]['lr'])

        # instanciation of the reversed polynome
        q_i.coeffs.requires_grad = False
        q_j.coeffs.requires_grad = False
        return PolyTransform(
            poly_i=q_i, poly_j=q_j, src_shape=self.dst_shape, dst_shape=self.src_shape
        )

    def warp_points(self, points_i, points_j):
        """
        ** Apply direct transformation. **

        The values are reduced between -1 and 1, the internal unit is therefore no longer in pxl.

        Examples
        --------
        >>> import torch
        >>> from deformation.poly import TorchPoly, PolyTransform
        >>> poly_i = TorchPoly(order=2)
        >>> poly_i[2, 0] = 1
        >>> ptsi = ptsj = torch.arange(5, dtype=torch.float32)
        >>> poly_i(ptsi, ptsj)
        tensor([ 0.,  1.,  4.,  9., 16.])
        >>> PolyTransform(poly_i=poly_i, src_shape=(4, 1)).apply_points_trans(ptsi, ptsj)[0]
        tensor([4.0000, 2.5000, 2.0000, 2.5000, 4.0000])
        >>> PolyTransform(poly_i=poly_i, src_shape=(16, 1)).apply_points_trans(ptsi, ptsj)[0]
        tensor([16.0000, 14.1250, 12.5000, 11.1250, 10.0000])
        >>> # there are no consequences on the linear term
        >>> PolyTransform(src_shape=(4, 1)).apply_points_trans(ptsi, ptsj)[0]
        tensor([0., 1., 2., 3., 4.])
        >>> PolyTransform(src_shape=(16, 1)).apply_points_trans(ptsi, ptsj)[0]
        tensor([0., 1., 2., 3., 4.])
        >>>
        """
        points_i, points_j = torch.from_numpy(points_i), torch.from_numpy(points_j)
        points_i, points_j = 2*(points_i/self.src_shape[0])-1, 2*(points_j/self.src_shape[1])-1
        points_i, points_j = self.forward(points_i, points_j)
        points_i, points_j = .5*(points_i+1)*self.src_shape[0], .5*(points_j+1)*self.src_shape[1]
        points_i, points_j = points_i.detach().cpu().numpy(), points_j.detach().cpu().numpy()
        return points_i, points_j
