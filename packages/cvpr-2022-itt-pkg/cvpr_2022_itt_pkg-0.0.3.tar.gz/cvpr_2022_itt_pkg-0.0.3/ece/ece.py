from cvpr_2022_itt_pkg.core import *
from cvpr_2022_itt_pkg.physics import *
import numpy as np


'''
This is basically a laundry list of every ECE thing I want to do but have to use multiple commands for/Google how to 
do it and it is really annoying so I have this instead. Uses the core module.
'''


# ECE Functions
def fft(y, T, pad=0, axis=- 1, norm='dft'):
    """
    A 2-sided (positive and negative) fft that uses numpy's fft as a starting point. Contains normalizations to
    match the dft and cft for assistance in visualization. It is often the case in optical simulations that a 1-way
    fourier transforms is used to compute further *spatial* behavior, so both the sample spacing and amplitude must
    be handled appropriately and not thrown away.

    :param y: ndarray
        Input signal to be fft'd
    :param T: float
        Length of interval in space/time/etc.
    :param pad: int
        Size of TOTAL pad. This means a signal [1, 1] with pad = 2 with be padded to be [0, 1, 1, 0]. This should
        match any ifft you did before!!
    :param axis: tuple
        Specifies which axis should the fft be taken over
    :param norm: {'dft', 'cft'}
        Specifies how the fft should be normalized, to match the dft or cft. See examples for some fine details
    :return: xf: fourier grid; yf: fft signal
    """
    # Just trying to make sure it won't mess up
    N = np.squeeze(np.array(y.shape))

    # Padding the signal according to the specified pad. Note that the pad passed to the function will be divided by
    # 2, and padded to the signal. A signal [1, 1] with pad = 2 with be padded to be [0, 1, 1, 0]
    y = np.pad(y, pad//2, mode='constant')
    xf = np.linspace(-0.5 * N / T, 0.5 * N / T, N+pad)
    yf = 1 / N * np.fft.fftshift(np.fft.fft(np.fft.ifftshift(y, axis=axis), axis=axis), axis=axis)

    # Returning the proper output according to the normalization type specified
    if norm == 'dft':
        return xf[:N+pad], yf[:N+pad]
    if norm == 'cft':
        return xf[:N + pad], T*yf[:N + pad]


def ifft(y, T, pad=0, axis=- 1, norm='dft'):
    """
    A 2-sided (positive and negative) ifft that uses numpy's fft as a starting point. Contains
    normalizations to match the dft and cft for assistance in visualization. It is often the case in optical simulations
    that a 1-way fourier transforms is used to compute further *spatial* behavior, so both the sample spacing and
    amplitude must be handled appropriately and not thrown away.

    :param y: ndarray
        Input signal to be ifft'd
    :param T: float
        Length of interval in fourier space (2 x max_frequency)
    :param pad: int
        Tells the function how to interpret the signal for sample spacing. This should match any fft you did before!!
    :param axis: tuple
        Specifies which axis should the fft be taken over
    :param norm: {'dft', 'cft'}
        Specifies how the fft should be normalized, to match the dft or cft. See examples for some fine details
    :return: xf: inverse-fourier grid; yf: ifft signal
    """
    # Just trying to make sure it won't mess up
    N = np.squeeze(np.array(y.shape))
    ogN = N - pad # The original N value

    xf = np.linspace(-0.5 * N / T, 0.5 * N / T, ogN)
    yf = ogN * np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(y, axis=axis), axis=axis), axis=axis)

    # Returning the proper output according to the normalization type specified
    if norm == 'dft':
        return xf, yf[pad//2:N-pad//2]
    if norm == 'cft':
        return xf, yf[pad//2:N-pad//2]/T


def fft2(y, T, pad=0, axes=(0,1), norm='dft'):
    """
    A function that uses numpy's fft2 as a starting point. Contains normalizations to match the dft and cft for
    assistance in visualization/computation. It is often the case in optical simulations
    that a 1-way fourier transforms is used to compute further *spatial* behavior, so both the sample spacing and
    amplitude must be handled appropriately and not thrown away.

    :param y: ndarray
        Input signal to be fft'd
    :param T: float
        Length of interval in space/time/etc.
    :param pad: int
        Size of TOTAL pad. This means a signal [1, 1] with pad = 2 with be padded to be [0, 1, 1, 0]. This should
        match any ifft you did before!!
    :param axis: tuple
        Specifies which axis should the fft be taken over
    :param norm: {'dft', 'cft'}
        Specifies how the fft should be normalized, to match the dft or cft. See examples for some fine details
    :return: xf: fourier grid; yf: fft signal
    """
    # Just trying to make sure it won't mess up
    N = np.squeeze(np.array(y.shape))

    # Padding the signal according to the specified pad. Note that the pad passed to the function will be divided by
    # 2, and padded to the signal. A signal [1, 1] with pad = 2 with be padded to be [0, 1, 1, 0]
    y = np.pad(y, (pad//2,pad//2), mode='constant')
    if N[0] == N[1]:
        xf = np.linspace(-0.5 * N[0] / T, 0.5 * N[0] / T, N[0]+pad)
        xxf, yyf = np.meshgrid(xf[:N[0]+pad], xf[:N[0]+pad])
        yf = 1.0 / (N[0]*N[1]) * np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(y, axes=axes), axes=axes), axes=axes)

        # Returning the proper output according to the normalization type specified
        if norm == 'dft':
            return xxf, yyf, yf[:N[0]+pad, :N[1]+pad]
        if norm == 'cft':
            return xxf, yyf, yf[:N[0]+pad, :N[1]+pad] * T**2


def ifft2(y, T, pad=0, axes=(0,1), norm='dft'):
    """
    A function that uses numpy's ifft2 as a starting point. Contains normalizations to match the dft and cft for
    assistance in visualization. It is often the case in optical simulations that a 1-way fourier transforms is used
    to compute further *spatial* behavior, so both the sample spacing and amplitude must be handled appropriately
    and not thrown away.

    :param y: ndarray
        Input signal to be ifft'd
    :param T: float
        Length of interval in space/time/etc.
    :param pad: int
        Tells the function how to interpret the signal for sample spacing. This should match any fft you did before!!
    :param axis: tuple
        Specifies which axis should the fft be taken over
    :param norm: {'dft', 'cft'}
        Specifies how the fft should be normalized, to match the dft or cft. See examples for some fine details
    :return: xf, yyf: inverse-fourier grids; yf: ifft signal
    """
    # Just trying to make sure it won't mess up
    N = np.squeeze(np.array(y.shape))
    ogN = N - pad # The original N value
    if N[0] == N[1]:
        xf = np.linspace(-0.5 * N[0] / T, 0.5 * N[0] / T, ogN[0])
        xxf, yyf = np.meshgrid(xf, xf)
        yf = (ogN[0] * ogN[0]) * np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(y, axes=axes), axes=axes), axes=axes)

        # Returning the proper output according to the normalization type specified
        if norm == 'dft':
            return xxf, yyf, yf[pad//2:N[0]-pad//2, pad//2:N[1]-pad//2]
        if norm == 'cft':
            return xxf, yyf, yf[pad//2:N[0]-pad//2, pad//2:N[1]-pad//2] / T**2


def basis_decomp(sig, dA, bases):
    if len(bases.shape) == 2:
        print('TODO')
    if len(bases.shape) == 3:
        if sig.shape == bases[:2]:
            return np.einsum('ij,ijk->k', sig, bases) * dA
        if sig.shape == bases[-2:]:
            return np.einsum('ij,kji->k', sig, bases) * dA


