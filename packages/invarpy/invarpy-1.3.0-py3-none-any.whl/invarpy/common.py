"""
Common statistics

Routines in this module:

spectrum_estimate(field1D, pixel_size=1, shift_origin=False)	= power spectrum estimate from a 1D cosmological scalar field
split_spectrum(field1D, pixel_size=1, origin_shift=False)		= split spectra of an even length 1D cosmological scalar field 

"""

__all__ = ['spectrum_estimate', 'split_spectrum']


import numpy as np
from numpy.fft import fftshift, fftn, ifftshift, fftfreq, ifftn, fft, ifft




def spectrum_estimate(field1D, shift_origin=False):
	"""

	"""

	if shift_origin == True:

		field1D = ifftshift(field1D)

		field_fft = fftshift(fftn(field1D))

		ans = np.abs(field_fft)**2

	else:

		field_fft = fftn(field1D)

		ans = np.abs(field_fft)**2 

	return ans




def split_spectrum(field1D, shift_origin=False):
	"""

	"""

	N = field1D.shape[0]

	if N % 2 != 0:
		raise ValueError("Length of field1D ndarray must be even.")

	n = int(N/2)

	field_L, field_R = field1D[:n], field1D[n:]

	pspec_L = spectrum_estimate(field_L, shift_origin=shift_origin)
	pspec_R = spectrum_estimate(field_R, shift_origin=shift_origin)

	return pspec_L, pspec_R




	
