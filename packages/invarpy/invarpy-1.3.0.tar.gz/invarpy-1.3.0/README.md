# invarpy package v1.3.0

- Package that includes several methods to compute statistical translation non-invariance of primarly, but not limitted to, scalar
cosmological fields.

## Updates on v1.3.0

- New method called invarpy.py that calculates the first kind estimator and its bias
through pbc configuration space method for a three-dimensional field.

## Older versions updates

## Updates on v1.2.1

- All 1D methods are working;
- Removed unnecessary package functools;
- Now every method takes the same input. This means that for a configuration space routine, input
field is the field in configuration space, whereas for a Fourier space routine, input field is
the Fourier transform of the field in configuration space. For the bias routines, input must be
the field power spectrum not-normalized. The common.py method computes the power spectrum without
normalizing it. Normalization happens inside the routines of nopbc_estimators or pbc_estimators
methods.

### Minor Bug fixes on v1.2.0

- Fixed sigma estimator if statement on nopbc_estimators method;
- nopbc_estimators method is working correctly.

### Major Bug fixes on v1.1.2

- Fixed configuration space on pbc_estimators method normalization factor for the estimator bias;
- Fourier space and configuration space for pbc_estimator.py is working correctly.

### Minor Bug fixes on v1.1.1

- Fixed bug of 'unexpected keyword argument estimator_kind' on sigma_which_diagonal routine of pbc_estimator.py method. 

### Major Bug fixes on v1.1.0

- Fixed second and first kind estimator bias in pbc_estimators.py method.
- Fixed second kind estimator bias in pbc_estimators.py method;
- Fixed bugs on common.py.






