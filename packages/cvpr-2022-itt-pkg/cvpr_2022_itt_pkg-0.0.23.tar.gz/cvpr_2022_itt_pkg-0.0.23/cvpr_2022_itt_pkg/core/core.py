import numpy as np


# Basic Functions
def linspace(starts, stops, nums):
    """
    2/23/22 VERIFIED

    A modified version of NumPy's linspace. Input start and endpoints can be single integers or a list (though not a
    mismatch). The outputs can be collected as a, b, c, ... = linspace(...) if lists are given as input. If integers
    are given as input, np.linspace is called directly.

    :param starts: int or list
        Starting points of the linspace arrays
    :param stops: int or list
        End points of the linspace arrays
    :param nums: int or list
        Number of steps in each array

    :return: output : ndarray
        The array(s) evaluated generated from the modified linspace

    --------
    Examples
    --------
    a, b = linspace([1, 3], [2, 4], [8, 5]) <--- two arrays with 8 and 5 entries, starting at 1 and 3, ending at 2
                                                    and 4 respectively
    a, b = linspace([1, 3], [2, 4], [8]) <--- two arrays with 8 entries, starting at 1 and 3, ending at 2 and 4
                                                respectively
    a = linspace([1], [2], [8]) <--- For consistency to above cases (though a standard numpy call is possible)
    a = linspace(1, 2, 8) <--- Looks like the standard numpy call!
    """
    if isinstance(starts, list) and isinstance(stops, list) and isinstance(nums, list):
        # Getting the lengths of the inputs that at this point are all lists.
        min_len, max_len, num_len = min([len(starts), len(stops)]), max([len(starts), len(stops)]), len(nums)

        # Finding the amount of unique lengths. 3 doesn't make sense, so it is a failure case.
        if len({min_len, max_len, num_len}) == 3:
            print('Unable to interpret ez.linspace inputs (3 lists of different sizes where given')
            return None
        # If the amount of unqiue lengths is 1, then the default numpy call is returned
        elif len({min_len, max_len, num_len}) == 1:
            return np.linspace(starts[0], stops[0], num=nums[0])
        # If the amount of unique lengths is 2, then the modified numpy call is returned
        else:
            # Converting all the lists to np arrays of the same size
            ones_len = max([max_len, num_len])
            starts = np.ones(ones_len) * starts
            stops = np.ones(ones_len) * stops
            nums = np.ones(ones_len) * nums
            steps = (stops - starts) / (nums - 1)
            a = list()
            # Collecting all the linspace calls, we use np.arange here because why not
            for i in range(ones_len):
                a.append(np.arange(nums[i]) * steps[i] + starts[i])
            return a
    else:
        # If everything passed was an integer, just do the default numpy linspace call
        return np.linspace(starts, stops, num=nums)


def meshgrid(array_1d, dim=2, indexing='xy'):
    """
    2/23/22 VERIFIED

    A modified version of meshgrid that only requires 1 input array. Often, we are just wanting square grids,
    so this is just a shortcut where the input array_1d is a single linspace that can be upped to a meshgrid via the
    dim value.

    :param array_1d: ndarray or list
        The array you want to replicated multiple times to form a meshgrid
    :param dim: int
        The number of dimensions you want a meshgrid over
    :param indexing:
        The indexing. Cartesian is default and preferred
    :return: output: default 'xy' or optionally 'ij'
        The output meshgrid

    --------
    Examples
    --------
    a, b, c = meshgrid([-10, -5, 0, 5, 10], 3)
    aa, bb = meshgrid(ez.linspace(-10, 10, 30), 2)
    """
    # It's that easy!
    return np.meshgrid(*list(array_1d for i in range(dim)), indexing=indexing)


def normgrid(arr_1d, dim=2, indexing='xy', ord=None):
    """
    2/23/22 VERIFIED

    Performs a meshgrid over the arr_1d according to ez.meshgrid, then computes the norm = sqrt(x1**2 + x2**2 + ...).

    :param arr_1d: ndarray or list
        The input array/list over which to perform a meshgrid
    :param dim: int
        The number of dimensions
    :param indexing: default 'xy' or 'ij'
        The indexing. Cartesian is default and preferred
    :param ord: None or str
        The type of norm, default is None which gives 2-norm, specify according to np otherwise
    :return: output: ndarray
        The result of the p-norm applied to a meshgrid with p specified by the ord parameter

    --------
    Examples
    --------
    normy = normgrid(ez.linspace(-10, 10, 31), 3) <--- A 3d normgrid
    norm_macdonald = normgrid(ez.linspace(-10, 10, 30), 2) <--- A 2d normgrid

    "I think there's nothing cooler than being a lone wolf. Except at wolf-picnics when you don't have a partner for the
    wolf-wheelbarrow races."
    """
    return np.linalg.norm(meshgrid(arr_1d, dim, indexing=indexing), axis=0, ord=ord)


def shape_mask(arr, r=1, dim=2, shape='circle'):
    """
    2/23/2022 VERIFIED

    A function that produces a circle/square mask based off of an array. The most meaningful way to use this function is
    likely with arr = ez.linspace(-a, a, N).

    :param arr: ndarray (1d array)
        The input array which is is compared to the radius value, just 1d
    :param r: float
        The radius value to compare against (radius of a square = half the width or height in this case)
    :param dim: int
        The dimensionality of the shape mask
    :param shape: {'circle', 'square'}
        The type of shape -- for now just square or circle.
    :return: output: ndarray
        The output mask, a ndarray of bool values
    """
    if shape=='circle':
        norm_arr = normgrid(arr, dim=dim, ord=None)
        return norm_arr <= r
    elif shape=='square':
        norm_arr = normgrid(arr, dim=dim, ord=np.inf)
        return np.abs(norm_arr) <= r


def mesh_spread_2d(x):
    """
    A simple function that just gives the range of a 2d array

    :param x: ndarray
    :return: the range of the array
    """
    return np.amax([abs(x[0,:] - x[-1,:]), abs(x[:,0] - x[:,-1])])