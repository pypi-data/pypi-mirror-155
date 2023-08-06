"""
Non Periodic-Boundary-Condition Translation Non-Invariance Estimators

Routines in this module:

#   Fourier Space Method

sigma(field1D, estimator_kind=1)                                    = 1st or 2nd kind biased sigma estimator computed in Fourier space
sigma_bias(pspec, estimator_kind=1)                                 = 1st or 2nd kind estimator bias
sigma_which_diagonal(field1D, diagonal=0)                           = finds the desired diagonal of the covariance matrix of field1D
sigma_bias_which_diagonal(pspec, diagonal=0, estimator_kind=1)      = finds the desired diagonal of the 1st or 2nd kind estimator matrix

#   Configuration Space Method
finite_geometric_series(N, n, m, l)                                 = finite geometric series function returns int
geometric_series_matrices(N)                                        = find all geometric matrices by varying n, m, l variables on finite_geometric_series method
sigma_cs(field1D, geometric_matrices, estimator_kind=1)             = 1st or 2nd kind biased sigma estimator computed in configuration space

"""

__all__ = ['sigma', 'sigma_bias', 'sigma_which_diagonal', 'sigma_bias_which_diagonal', 'finite_geometric_series', 'geometric_series_matrices', 'sigma_cs']



import numpy as np
from numpy.fft import fftshift, fftn, ifftshift, fftfreq, ifftn, fft, ifft




################################################################
#################### Fourier space approach ####################
################################################################


#   field1D must be a flattened cosmological field in a 1-D ndarray type
#   estimator_kind takes either 1 or 2, refers to the estimator you want to use to compute non-invariance
def sigma(field1D, estimator_kind=1):
    """

    Compute the desired kind of the biased sigma estimator, given a field, using Fourier space method. 
    
    Parameters
    ----------
    field1D : one-dimensiona complex ndarray
              Input one-dimensional ndarray corresponding 
              to the cosmological field Fourier transformed.
    estimator_kind : int, two-choices, default=1
                     This sets the estimator kind to be computed. 
                     Must be either 1 (1st kind) or 2 (2nd kind).


    Returns
    -------
    ans : one-dimensional complex ndarray
          Returns the desired kind of the biased sigma estimator, using Fourier space method.

    Raises
    ------
    ValueError
        If 'estimator_kind' is not equal to either 1 or 2 (int).

    """

    N = field1D.shape[0]
    ans = np.zeros((N),dtype='complex')

    if estimator_kind == 2:
        field1D = np.abs(field1D)**2

    elif estimator_kind != 1 and estimator_kind != 2:
        raise ValueError("Invalid estimator kind. Must be either 1 or 2.")
    
    for i in range(N):

        ans[i] = (1/(N-i))*np.sum(sigma_which_diagonal(field1D, diagonal=(i))[0])
                
    return ans


def sigma_bias(pspec, estimator_kind=1):
    """

    Compute the bias of the desired estimator kind, given the field power spectrum. 
    
    Parameters
    ----------
    pspec : one-dimensiona ndarray
            Input one-dimensional ndarray corresponding 
            to the cosmological field power spectrum.
    estimator_kind : int, two-choices, default=1
                     This sets the estimator kind to be computed. 
                     Must be either 1 (1st kind) or 2 (2nd kind).

    Returns
    -------
    ans : one-dimensional complex ndarray
          Returns the bias of the desired sigma estimator kind.

    Raises
    ------
    ValueError
        If 'estimator_kind' is not equal to either 1 or 2 (int).

    """

    N = pspec.shape[0]  
    ans = np.zeros((N),dtype='complex')

    if estimator_kind == 1:

        ans[0] = (1/N)*np.sum(sigma_bias_which_diagonal(pspec, diagonal=0)[0])

    elif estimator_kind == 2:

        for i in range(N):
            
            ans[i] = (1/(N-i))*np.sum(sigma_bias_which_diagonal(pspec, diagonal=i, estimator_kind=2)[0])

    else:
        raise ValueError("Invalid estimator kind. Must be either 1 or 2.")
              
    return ans


def sigma_which_diagonal(field1D, diagonal=0):

    """

    Compute the diagonal of the covariance matrix of a , given the field power spectrum. 
    
    Parameters
    ----------
    pspec : one-dimensiona complex ndarray
            Input one-dimensional ndarray corresponding 
            to the cosmological field Fourier transformed.
    diagonal : int, default=0
               the desired diagonal of the covariance matrix to be
               computed.

    Returns
    -------
    ans : One-index object containing a complex ndarray
          Returns the desired diagonal of the covariance matrix of that
          Fourier transformed field input.

    """

    N = field1D.shape[0]
    ans = np.zeros((1),dtype='object')
    
    ans[0] = (1/2)*(field1D[diagonal:]*np.conjugate(field1D[:N-diagonal]) +
                           np.conjugate(field1D[diagonal:]*np.conjugate(field1D[:N-diagonal])))
    return ans


def sigma_bias_which_diagonal(pspec, diagonal=0, estimator_kind=1):
    """

    Compute the diagonal of the bias matrix for the desired sigma estimator kind, given the field power spectrum. 
    
    Parameters
    ----------
    pspec : one-dimensiona complex ndarray
            Input one-dimensional ndarray corresponding 
            to the cosmological field Fourier transformed.
    diagonal : int, default=0
               the desired diagonal of the bias matrix to be
               computed.
    estimator_kind : int, two-choices
                     This sets the estimator kind to be computed. 
                     Must be either 1 (1st kind) or 2 (2nd kind).

    Returns
    -------
    ans : One-index object containing a complex ndarray
          Returns the desired diagonal of the bias matrix of that
          Fourier transformed field input

    """

    N = pspec.shape[0]
    ans = np.zeros((1),dtype='object')
    Id = np.identity(N)
    Ide = np.zeros((N,N))

    if estimator_kind == 1:
        ans[0] = pspec

    elif estimator_kind == 2:
        for j in range(N):
            Ide[:,j] = Id[:,-j]

        ans[0] = pspec[:N-diagonal]*pspec[diagonal:] + (pspec[:N-diagonal]**2)*(np.diagonal(Ide,offset=diagonal)**2) + (pspec[:N-diagonal]**2)*(np.diagonal(Id,offset=diagonal)**2)

    else:
        raise ValueError("Invalid estimator kind. Must be either 1 or 2.")
    
    return ans


######################################################################
#################### Configuration space approach ####################
######################################################################


def finite_geometric_series(N, n, m, l):
    """

    Compute the finite  geometric series with bounded by N - n - 1 of the summation term exp(-2 * i * pi * sum_index * (m - l) / N).
    
    Parameters
    ----------
    N : int > 0
        Corresponds to the cosmological field ndarray length.
    n : int <= N
        Corresponds to haw many diagonals far from the main diagonal
        you want to truncate the sum.
    m : int <= N - 1
        The first field vector mode location.
    l : int <= N - 1
        The second field vector mode location.

    Returns
    _______
    ans : int
          The correspondent result of the sum.

    Math
    ----
    The equation we are summing can be expressed as:

    Sum[exp(-2 * pi * p * (m - l) / N), from p = 0 to p = N - n -1].

    """

    if m == l:
        return N - n
    
    elif n == 0:
        return 0
    
    
    ans = (1 - np.exp(-(1 - n/N) * 2 * np.pi * 1j * (m - l)))/(1 - np.exp(-2 * np.pi * 1j * (m - l) / N))
    return ans


def geometric_series_matrices(N):
    """

    Compute all the possible results of the geometric series function by varying the n, l and m parameters and store the result in ndarray.
    
    Parameters
    ----------
    N : int > 0
        Corresponds to the cosmological field ndarray length.

    Returns
    -------
    geometric_matrices : 3-D complex ndarray
                         The output is a 3-D python array_like type where its idices are represented by all [n, m, l] such that
                         0 <= n <= N, 0 <= m, l <= N - 1.

    """

    geometric_matrices = np.zeros((N, N, N), dtype='complex')
    
    for n in range(N):
        for m in range(N):
            for l in range(N):

                geometric_matrices[n, m, l] = finite_geometric_series(N, n, m, l) * np.exp(2 * np.pi * 1j * l * n / N)

    return geometric_matrices


def sigma_cs(field1D, geometric_matrices, estimator_kind=1):
    """

    Compute the desired kind of the biased sigma estimator, given a field, using configuration space method. 
    
    Parameters
    ----------
    field1D : one-dimensiona complex ndarray
              Input one-dimensional ndarray corresponding 
              to the cosmological field Fourier transformed.
    geometric_matrices : 3-D complex ndarray
                         The resultant geometric_matrices for a field array with length N
    estimator_kind : int, two-choices, default=1
                     This sets the estimator kind to be computed. 
                     Must be either 1 (1st kind) or 2 (2nd kind).

    Returns
    -------
    ans : one-dimensional complex ndarray
          Returns the desired kind of the biased sigma estimator, using configuration space method.

    Raises
    ------
    ValueError
        If 'estimator_kind' is not equal to either 1 or 2 (int).

    """

    N = field1D.shape[0]
    ans = np.zeros((N), dtype='complex')

    if estimator_kind == 1:
 

        for n in range(N):

            transformed_field = np.dot(geometric_matrices[n, :, :], field1D)
            ans[n] = (1 / (2*N - 2*n) ) * ( np.dot(field1D, transformed_field) + np.dot(field1D, np.transpose(np.conjugate(transformed_field))) )



    elif estimator_kind == 2:

        field1D = ifftn(np.abs(fftn(field1D))**2)
        field1D_conjugate = np.conjugate(field1D)


        for n in range(N):

            transformed_field = np.dot(geometric_matrices[n, :, :], field1D_conjugate)
            ans[n] = (1/(N-n)) * (np.dot(field1D, transformed_field))

    else:
        raise ValueError("Invalid estimator kind. Must be either 1 or 2.")

    
    return ans



