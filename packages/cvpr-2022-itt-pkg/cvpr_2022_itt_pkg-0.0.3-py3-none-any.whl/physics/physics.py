from cvpr_2022_itt_pkg.core import *
from cvpr_2022_itt_pkg.ece import *
from cvpr_2022_itt_pkg.prob import *
import numpy as np
import math
import matplotlib.pyplot as plt


# Optics Functions
def fraunhofer(wave, T, D, wvl=500e-9, z=10000, mask='circle', pad=0):
    """
    Fraunhofer diffraction. IMPORTANT NOTE: THIS WILL NOT GIVE YOU THE PSF
    FORMATION! IT WILL GIVE YOU FRAUNHOFER DIFFRACTION WITHOUT A LENS.

    For PSF formation with a lens, you have to use one of the ___2psf()
    functions.

    :param wave: ndarray
        The wave over the grid of lengths T x T.
    :param T: float
        The length of one dimension of the grid (assumed to be square grid)
    :param D: float
        Diameter of the aperture. Optionally set to D=np.inf for plane wave (though, you will get aliasing)
    :param wvl: float
        Wavelength of light (for a general incoherent visible light simulation, choose 555e-9 or something in this
        range)
    :param z: float
        Propagation distance
    :param mask: {'circle', 'square'}
        The mask shape.
    :return: the sample spacing grid; the output wave
    """
    aperture = shape_mask(linspace(-T/2, T/2, wave.shape[0]), r=D/2, dim=2, shape=mask)
    if len(wave.shape) == 3:
        xx, yy, wave_out = fft2(wave * aperture[:,:,np.newaxis], T, pad=pad)
    else:
        xx, yy, wave_out = fft2(wave * aperture, T, pad=pad)
    xx *= (wvl * z)
    yy *= (wvl * z)

    return xx, yy, wave_out


def fresnel(wave, T, D, wvl=500e-9, z=10000, mask='circle'):
    """
    Fresnel diffraction. IMPORTANT NOTE: THIS WILL NOT GIVE YOU THE PSF
    FORMATION! IT WILL GIVE YOU Fresnel DIFFRACTION WITHOUT A LENS.

    For PSF formation with a lens, you have to use one of the ___2psf()
    functions.

    :param wave: ndarray
        The wave over the grid of lengths T x T.
    :param T: float
        The length of one dimension of the grid (assumed to be square grid)
    :param D: float
        Diameter of the aperture
    :param wvl: float
        Wavelength of light (for a general incoherent visible light simulation, choose 555e-9 or something in this
        range)
    :param z: float
        Propagation distance
    :param mask: {'circle', 'square'}
        The mask shape. Later implementations will likely remove this or have it as optional
    :return: the sample spacing grid; the output wave
    """
    if mask=='circle':
        aperture = shape_mask(linspace(-T/2, T/2, wave.shape[0]), r=D/2, dim=2)
    else:
        aperture = shape_mask(linspace(-T/2, T/2, wave.shape[0]), r=D/2, dim=2, shape=mask)
    xprime = normgrid(np.linspace(-T/2, T/2, wave.shape[0]))
    xx, yy, wave_out = fft2(wave * aperture * np.exp(1j*np.pi/(wvl * z) * xprime**2), T)
    xx *= (wvl * z)
    yy *= (wvl * z)

    return xx, yy, wave_out * np.exp(1j * 2*np.pi/wvl * z) / \
           (1j * wvl * z) * np.exp(1j*np.pi * (xx**2 + yy**2) / (wvl * z))


def sph_wave(N, T, L, wvl=500e-9):
    """
    Returns a spherical wave of size NxN over a TxT (m^2) spatial area. There is no amplitude, but you can easily
    multiply the return value

    :param N: int
        Size of the input array in elements (will give output NxN)
    :param T: float
        Metric length of a single dimension (assumes TxT area)
    :param L: float
        Distance of plane at which spherical wave is returned
    :param wvl: float
        The wavelength
    :return: ndarray
        The spherical wave
    """
    xx, yy = meshgrid(linspace(-T/2, T/2, N), dim=2)
    k = 2 * np.pi / wvl
    return np.exp(1j * k * np.sqrt(xx**2 + yy**2 + L**2)) / np.sqrt(xx**2 + yy**2 + L**2)



def phase2psf(phase, T, D, f, wvl=500e-9, L=-1, mask='circle'):
    """
    PSF formation using the phase of the wave directly. Calls upon Fraunhofer and is evaluated at the focal distance,
    with the option of the distance being provided to the function to know the PSF size in terms of the dimensions
    of the source object. Otherwise, dimensions returned will be in focal plane.

    :param phase: ndarray
        The phase of the wave. Often in this simulation package, only the phase matters, so this is a
        straightforward way of going from phase to space
    :param T: float
        Length of the input grid in meters
    :param D: float
        Diameter of the aperture in meters
    :param f: float
        Focal length in meters
    :param wvl: float
        Wavelength of the incident wave in meters
    :param L: float
        Propagation distance in meters
    :return: spatial grid; psf = abs(wave_out)**2
    """
    xx, yy, wave_out = fraunhofer(np.exp(1j * phase), T=T, D=D, wvl=wvl, z=f, mask=mask)
    psf = np.abs(wave_out)**2
    if L == -1:
        return xx, yy, psf
    else:
        return xx*(L/f), yy*(L/f), psf


def wave2psf(wave, T, D, f, wvl=500e-9, L=-1, mask='circle'):
    """
    PSF formation using the wave. Calls upon Fraunhofer and is evaluated at the focal distance, with the option of
    the distance being provided to the function to know the PSF size in terms of the dimensions of the source object.

    :param wave: ndarray
        The phase of the wave. Often in this simulation package, only the phase matters, so this is a
        straightforward way of going from phase to space
    :param T: float
        Length of the input grid in meters
    :param D: float
        Diameter of the aperture in meters
    :param f: float
        Focal length in meters
    :param wvl: float
        Wavelength of the incident wave in meters
    :param L: float
        Propagation distance in meters
    :return: spatial grid; psf = abs(wave_out)**2
    """
    xx, yy, wave_out = fraunhofer(wave, T, D, wvl=wvl, z=f, mask=mask)
    psf = np.abs(wave_out)**2
    if L == -1:
        return xx, yy, psf
    else:
        return xx * (L / f), yy * (L / f), psf


def otf_calc(pup_fun, T, D, f, wvl):
    '''
    A function that accepts the generalized pupil function and returns the otf with frequency components

    :param pup_fun: ndarray
        The generalized pupil array. Use in the form aperture_shape * np.exp(1j * phase_distortion)
    :param T: float
        The measure of the window of the pupil function [meters]
    :param D: float
        The size of the aperture [meters]
    :param f: float
        The focal length [meters]
    :param wvl: float
        The wavelength [meters]
    :return: (ndarray, ndarray, ndarray)
        The normalized OTF with frequency meshgrid
    '''
    w = D/2
    f_cutoff = w / (wvl * f)
    a, a, P = fft2(pup_fun, 1)
    a, a, otf = np.abs(ifft2(P * P, 1))
    xx, yy = meshgrid(linspace(-1/2, 1/2, pup_fun.shape[0]))
    scaling = 2*D/T * f_cutoff
    return xx/scaling, yy/scaling, otf/np.amax(otf)


def zern_phase_rep(phase, num_zern=36):
    print('hi')


def defocus_abgen(norm_grid, L_true, L_selected, wvl=500e-9):
    '''
    A function that returns a defocus (difference of spheres) abberation in radians. By default, there will be no
    aperture size given and the aberration will be at the size of the input meshgrid. With aperture specified,
    the mask will be applied accordingly.

    :param xx: ndarray
        input norm_grid (this function will square the input -- the argument should measure distance i.e. sqrt(
        something)
    :param L_true: float
        the true distance of the point source to the camera
    :param L_selected: float
        the selected distance of the point source (the "wrong" focus distance)
    :param wvl: float
        wavelength of the light
    :return: ndarray
        the output defocus aberration in radians
    '''
    return -1/2 * (1/L_selected - 1/L_true) * norm_grid**2 * (2*np.pi/wvl)

def genZernikeCoeff(num_zern, D_r0, num_vecs = 1):
    '''
    Just a simple function to generate random coefficients as needed, conforms to Noll's Theory. The nollCovMat()
    function is at the heart of this function.

    A note about the function call of nollCovMat in this function. The input (..., 1, 1) is done for the sake of
    flexibility. One can call the function in the typical way as is stated in its description. However, for
    generality, the D/r0 weighting is pushed to the "b" random vector, as the covariance matrix is merely scaled by
    such value.

    :param num_zern: This is the number of Zernike basis functions/coefficients used. Should be numbers that the pyramid
    rows end at. For example [1, 3, 6, 10, 15, 21, 28, 36]
    :param D_r0:
    :return:
    '''
    C = nollCovMat(num_zern, 1, 1)
    a = gen_rand_vec(C, num_vecs) * D_r0 ** (5.0/6.0)

    return a


def nollCovMat(Z, D, fried):
    """
    This function generates the covariance matrix for a single point source. See the associated paper for details on
    the matrix itself.

    :param Z: int
        Number of Zernike basis functions/coefficients, determines the size of the matrix.
    :param D: float
        The diameter of the aperture (meters)
    :param fried: float
        The Fried parameter value
    :return: the Noll covariance matrix
    """
    C = np.zeros((Z,Z))
    for i in range(Z):
        for j in range(Z):
            ni, mi = nollToZernInd(i+1)
            nj, mj = nollToZernInd(j+1)
            if (abs(mi) == abs(mj)) and (np.mod(i - j, 2) == 0):
                num = math.gamma(14.0/3.0) * math.gamma((ni + nj - 5.0/3.0)/2.0)
                den = math.gamma((-ni + nj + 17.0/3.0)/2.0) * math.gamma((ni - nj + 17.0/3.0)/2.0) * \
                      math.gamma((ni + nj + 23.0/3.0)/2.0)
                coef1 = 0.0072 * (np.pi ** (8.0/3.0)) * ((D/fried) ** (5.0/3.0)) * np.sqrt((ni + 1) * (nj + 1)) * \
                        ((-1) ** ((ni + nj - 2*abs(mi))/2.0))
                C[i, j] = coef1*num/den
            else:
                C[i, j] = 0
    C[0,0] = 1
    return C


def zernikeGen(N, coeff, axis=-1):
    """
    NEED TO UPDATE

    Generating the Zernike phase representation from specified coefficients.

    :param N: int
        1d length of array, the phase will be NxN
    :param coeff: ndarray
        The coefficient array, there can be multiple vectors, resulting in the output being 4d
    :param axis: int
        The axis over which the coefficient array is used to compute the phase components
    :return: the phase realization
    """

    num_coeff = coeff.shape[axis]

    # Setting up 2D grid
    x_grid, y_grid = np.meshgrid(np.linspace(-1, 1, N, endpoint=True), np.linspace(-1, 1, N, endpoint=True))

    zern_out = np.zeros((N,N,num_coeff))
    for i in range(num_coeff):
        zern_out[:,:,i] = coeff[i]*genZernPoly(i+1, x_grid, y_grid)

    return zern_out


def nollToZernInd(j):
    """
    This function maps the input "j" to the (row, column) of the Zernike pyramid using the Noll numbering scheme.

    Authors: Tim van Werkhoven, Jason Saredy
    See: https://github.com/tvwerkhoven/libtim-py/blob/master/libtim/zern.py
    """
    if (j == 0):
        raise ValueError("Noll indices start at 1, 0 is invalid.")
    n = 0
    j1 = j-1
    while (j1 > n):
        n += 1
        j1 -= n
    m = (-1)**j * ((n % 2) + 2 * int((j1+((n+1)%2)) / 2.0 ))

    return n, m


def genZernPoly(index, x_grid, y_grid):
    """
    This function generates overall Zernike polynomials according to Noll's definition, which is a modified Zernike
    polynomial.

    :param index: int
        The Zernike index under consideration
    :param x_grid: ndarray
        The x_grid over which the Zernike polynomials are computed
    :param y_grid: ndarray
        The y_grid over which the Zernike polynomials are computed
    :return: the Zernike polynomial
    """
    n,m = nollToZernInd(index)
    radial = radialZernike(x_grid, y_grid, (n,m))
    if m == 0:
        return np.sqrt(n+1)*radial
    if np.mod(index,2) == 0:
        return np.multiply(np.sqrt(n+1)*radial, np.sqrt(2)*np.cos(m * np.arctan2(y_grid, x_grid)))
    if np.mod(index,2) == 1:
        return np.multiply(np.sqrt(n+1)*radial, np.sqrt(2)*np.sin(m * np.arctan2(y_grid, x_grid)))
    '''
    if m < 0:
        return np.multiply(np.sqrt(n+1)*radial, np.sqrt(2)*np.sin(-m * np.arctan2(y_grid, x_grid)))
    else:
        return np.multiply(np.sqrt(n+1)*radial, np.sqrt(2)*np.cos(m * np.arctan2(y_grid, x_grid)))
    '''

def radialZernike(x_grid, y_grid, z_ind):
    """
    Generating the individual radial polynomial component of the Zernike polynomial.

    :param x_grid: ndarray
        The x_grid over which the Zernike polynomials are computed
    :param y_grid: ndarray
        The y_grid over which the Zernike polynomials are computed
    :param z_ind: tuple
        The (radial,angular) pair that parameterizes the Zernike representation.
    :return:
    """

    rho = np.sqrt(x_grid ** 2 + y_grid ** 2)
    radial = np.zeros(rho.shape)
    n = z_ind[0]
    m = np.abs(z_ind[1])

    for k in range(int((n - m)/2 + 1)):
        temp = (-1) ** k * np.math.factorial(n - k) / (np.math.factorial(k) * np.math.factorial((n + m)/2 - k)
                                                       * np.math.factorial((n - m)/2 - k))
        radial += temp * rho ** (n - 2*k)
    return radial