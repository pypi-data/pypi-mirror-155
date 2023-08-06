from cvpr_2022_itt_pkg.ece import *
from cvpr_2022_itt_pkg.physics import *

# Random Functions
def pdf(x):
    """
    Generating the probability density function (pdf) with auto bin widths. This function integrates to 1, but does not
    SUM to one, with the exception of bins are of width 1.

    :param x: ndarray
        Random Samples to plot pdf over
    :return: pdf values; center of bin locations; bin widths
    """

    vals, bins = np.histogram(x, bins='auto', density=True)
    midbins = (bins[1:] + bins[:-1]) / 2
    return vals, midbins, np.abs(midbins[0] - midbins[1])


def cdf(x):
    """
        Generating the probability density function (pdf) with auto bin widths. This function integrates to 1, but does not
        SUM to one, with the exception of bins are of width 1.

        :param x: ndarray
            Random Samples to plot pdf over
        :return: cdf values; center of bin locations
        """
    vals, midbins, dx = pdf(x)
    return np.cumsum(vals)*dx, midbins


def gen_dist(x, cdf, n_samp):
    """
    Generating a distribution from its cdf. The cdf in this case can be empirical or theoretical.

    :param x: ndarray
        This should be the x-locations of the bins, i.e. cdf = f(x).
    :param cdf:
        The cdf values itself. They should go from 0 to 1, there is an additional check for that within this function.
    :param n_samp:
        The number of samples desired to be generated.
    :return: the n_samp random samples
    """
    cdf[0] = 0
    cdf[-1] = 1
    seed = np.random.rand(n_samp)
    vals = np.interp(seed, cdf, x) #Intentionally swapped from how you'd think! (Inverse CDF rule)
    return vals


def gen_rand_vec(R, n_samp, mu=0, mode='chol'):
    """
    Generating a random vector according to an covariance matrix.

    :param R: ndarray
        Covariance matrix
    :param n_samp: int
        Number of samples desired
    :param mu: float
        Mean value of the random vector
    :param mode: {'chol', 'eig'}
        Different generation approaches, Cholesky by default
    :return: the n_samp desired random vectors
    """

    if mode == 'chol':
        L = np.linalg.cholesky(R)
        return L @ np.random.randn(R.shape[1], n_samp) + mu
    if mode == 'eig':
        vals, vecs = np.linalg.eig(R)
        print(vecs)
        return (vecs @ np.diag(np.sqrt(vals))) @ np.random.randn(R.shape[1], n_samp) + mu


def emp_cov(vecs, force_symm=False):
    """
    Computing the empirical covariance matrix. Can force the result to by positive semidefinite if desired.

    :param vecs:
    :param force_symm: bool
        Not done yet
    :return:
    """

    emp_mu = np.mean(vecs, axis=-1)
    emp_mu = np.expand_dims(emp_mu, axis=-1)
    return (vecs - emp_mu) @ (vecs - emp_mu).T / vecs.shape[-1]


def gen_rand_2dfield_psd(psd, T=1, N=1):
    """
    Generating N 2d random fields from its PSD. The default value of T = 1, representing the distance in the Fourier
    space, however, can be provided different value giving the resultant spatial sampling in the outputs.

    :param psd: ndarray
        Power spectral density
    :param T: float
        1d length in the Fourier space that the PSD is generated over
    :param N: int
        Number of output random fields
    :return: the output random fields and spatial grids
    """
    a,a,temp = fft2(np.random.randn(*(psd.shape + (N,))) + 1j * np.random.randn(*(psd.shape + (N,))), T, norm='dft')
    return ifft2(temp * np.sqrt(psd.shape[0]*psd.shape[1]) * np.sqrt(psd[:,:,np.newaxis]), T, norm='dft')


def gen_rand_2dfield_cov(cov, T=1, N=1):
    """
    Generating N 2d random fields from its covariance matrix. The default value of T = 1, representing the distance in
    the spatial domain, however, can be provided different value giving the resultant spatial sampling in the
    outputs.

    :param psd: ndarray
        Power spectral density
    :param T: float
        1d length in the Fourier space that the PSD is generated over
    :param N: int
        Number of output random fields
    :return: the output random fields and spatial grids
    """
    x, y, psd = fft2(cov, T, norm='dft')
    x, y, fields = gen_rand_2dfield_psd(np.abs(psd), mesh_spread_2d(x), N)
    return x, y, fields/np.sqrt(2)
