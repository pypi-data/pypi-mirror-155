"""
gengli.utils
============

	Some utilities required by the glicth generator.
	It has some functions to measure the distance (discrepancy) between glitches. Morevore it implements an nice handler for the PSD `read_psd`. 
	For benchmark, it also implements a pycbc-based SNR computation (although not used internally).
"""
import itertools
from scipy.stats import wasserstein_distance
import pycbc.psd
from pycbc.filter import match
from pycbc.types import TimeSeries
import numpy as np
import ray

import random
import os

#############################################################################################################
#############################################################################################################

@ray.remote
def metrics(fake1, fake2):
	"""
	Computes the similarity betweek glitch fake1 and fake2. It uses ray to parellelize and speed up the computations. It assumes that `ray.init()` has been already called.
	The similarity is computed using three different metrics:
	
	- Wasserstein distance
	- Mismatch (as standard in GW data analysis)
	- Mis-correlation (1-normalized correlation)
	
	All the three are returned.
	
	Input
	-----
	fake1: np.ndarray
		First GAN-generated glitch (sampled at 4096 Hz)
	fake2: np.ndarray
		Second GAN-generated glitch (sampled at 4096 Hz)
	
	Returns
	-------
	wass_value: float
		Wasserstein distance between the two glitches
	match_value: float
		Match between the two glitches
	ccor_value: float
		Correlation between the two glitches
		
	"""
	# To avoid dtype problems
	fake1 = np.asarray(fake1, dtype=np.float64) #asarray, avoids copies, when necessary
	fake2 = np.asarray(fake2, dtype=np.float64)

	# Correlation
	ccov = np.correlate(fake1 - fake1.mean(),
						fake2 - fake2.mean(),
						mode='full') #Maybe dropping mode full and keeping valid might help in speeding up??
	ccor = ccov / (len(fake1) * fake1.std() * fake2.std())
	ccor_value = max(np.abs(ccor))

	# PyCBC match
	data_points = len(fake1)
	samp_freq = 4096

	F1 = TimeSeries(fake1, delta_t=data_points/samp_freq, epoch=0)
	F2 = TimeSeries(fake2, delta_t=data_points/samp_freq, epoch=0)

	match_value = match(F1, F2)[0]

	# Wasserstein distance

	wass_value = wasserstein_distance(fake1, fake2)
	return wass_value, 1-match_value, 1-ccor_value

@ray.remote
def ray_dummy():
	return np.nan, np.nan, np.nan
	

def compute_distance_matrix(set1, set2):
	"""
	It computes the distance matrix between each pairs of two sets of glitches. The metric consists in 3 different quantities:
	
	- Wasserstein distance
	- Match (as standard in GW data analysis)
	- Correlation

	If the input are two sets of N and M glitches, the distance matrix will be a `(N,M,3)` matrix, where the the ij elements holds the 3 dimensional distances between the i-th element of the first set and the j-th element of the second set.
	

	Input
	-----
	
	set1: np.ndarray
		First set of glitches (shape `(N,D)`)
	
	set2: np.ndarray
		Second set of glitches (shape `(M,D)`)
	
	Returns
	-------
	
	distance_matrix: np.ndarray
		Distance matrix with shape `(N,M,3)`
	"""
	assert isinstance(set1, np.ndarray) and  isinstance(set2, np.ndarray), "Glitch sets must be arrays"
	set1, set2 = np.atleast_2d(set1), np.atleast_2d(set2)
	assert set1.ndim == set2.ndim == 2, "Glitch sets must be two dimensional"
	assert set1.shape[1] == set2.shape[1], "Glitch sets must be evaluated on the a grid of the same size. {} and {} given".format(set1.shape[1], set2.shape[1])
	
	same_set = np.allclose(set1, set2) if (set1.shape == set2.shape) else False 
	
	if same_set:
		distance_matrix = [metrics.remote(s1,s2) if i>=j else ray_dummy.remote() for (i,s1), (j,s2) in itertools.product(enumerate(set1), enumerate(set2)) ]
	else:
		distance_matrix = [metrics.remote(s1,s2) for s1, s2 in itertools.product(set1, set2)]
	distance_matrix = np.array(ray.get(distance_matrix)).reshape((set1.shape[0], set2.shape[0], 3))

	if same_set:
		ids_ = np.triu_indices(distance_matrix.shape[0])
		for i,j in zip(*ids_): distance_matrix[i,j,:] = distance_matrix[j,i,:]
	
	return distance_matrix

#############################################################################################################
#############################################################################################################

def read_psd(psd_file, srate, length, flow = 30., asd = False, ifo = None):
	"""
	Wrapper to `pycbc.psd.read`: for more info see the pycbc `doc page <https://pycbc.org/pycbc/latest/html/pycbc.psd.html>`_.
	Read the psd from a txt or xml file and interpolates it to the frequency grid suitable for a glitch with given length and sampling rate.
	The PSD returned will be the same grid on which `np.fft.rfft` generates the glitch in frequency domain.
	
	Parameters
	----------
	
	psd_file: str/bytes
		File to read the PSD from. If it is not an xml file it is understood to be a txt file.
		User can also give the name of an analytic PSD available in lal.
		If a byte object is given, it is understood that each line of the byte is an entry (f_i, PSD(f_i)). That is equivalent to reading a regular csv file in binary mode.
	
	srate: float
		Sampling rate of the glitch
		
	length: float
		Length of the time grid the glitch is evaluated at
		
	flow: float
		Lower frequency for the PSD

	asd: bool
		Whether the file keeps an ASD, rather than a PSD
		
	ifo: str
		The interferometer which to load the PSD of. Only applies to xml format

	Returns
	-------

	psd: np.ndarray
		Numpy array holding the PSD 
	"""
		#setting vars
	dt = 1/srate
	df = srate/length
	len_f = length // 2 + 1

		#checking for problems
	if isinstance(psd_file, bytes):
		psd_file = np.loadtxt(psd_file.split(b'\n'))
		if asd: psd_file[:,1] = np.square(psd_file[:,1])
	elif not isinstance(psd_file,str): raise ValueError("The psd_file should be a string!")

		#reading PSD
	if isinstance(psd_file, np.ndarray):
		psd = pycbc.psd.read.from_numpy_arrays(psd_file[:,0], psd_file[:,1], len_f, df, flow)
	elif psd_file in pycbc.psd.get_lalsim_psd_list():
		psd = pycbc.psd.from_string(psd_file, len_f, df, flow)
	elif psd_file.endswith('xml') or psd_file.endswith('xml.gz'):
		psd = pycbc.psd.read.from_xml(psd_file, len_f, df, flow, ifo_string=ifo)
	else:
		psd = pycbc.psd.read.from_txt(psd_file, len_f, df, flow, is_asd_file=asd)

		#This is nice to make the PSD to behave nicely...
	psd = pycbc.psd.estimate.inverse_spectrum_truncation(psd, len_f, low_frequency_cutoff=flow, trunc_method='hann').numpy()

	return psd
	
	#f, psd = np.loadtxt(psd_file)[:,:2].T
	#if asd: psd = np.square(psd) 	
	#new_grid = np.linspace(0, len_f*df, len_f)
	#return new_grid, np.interp(new_grid, f, psd)

def compute_snr(glitch, srate, psd = None, flow = None):
	"""
	It computes the SNR of a glitch using pycbc package.
	It is a wrapper to `pycbc.filter.sigmasq`
	
	Parameters
	----------
	glitch: np.ndarray
		A glitch to compute the SNR of. The array can be one-dimensional or two-dimensional
		
	srate: float
		Sampling rate for the glitch	
		
	psd: np.ndarray
		A psd to compute the SNR, suitable for the glitch. It is advisable to generate it with `gengli.utils.read_psd`. If `None`, no psd will be used
	
	flow: float
		Low frequency cutoff for the SNR computation
		
	Returns
	-------
	snr: np.ndarray
		Signal-to-noise ratio of the glitch
	"""
		#handling PSD
	if psd is not None: psd = pycbc.types.timeseries.FrequencySeries(psd, delta_f = srate/glitch.shape[-1])
	
	glitch = np.atleast_2d(glitch)
	
	snr = np.zeros((glitch.shape[0],))
	for i, g in enumerate(glitch):
		# Cast template to pycbc timeseries
		template = pycbc.types.timeseries.TimeSeries(g, delta_t=1.0/srate, dtype='double')

		# and compute the matched_filter
		sigmasq = pycbc.filter.sigmasq(template, psd=psd,
										 low_frequency_cutoff=flow)
		snr[i] = np.sqrt(sigmasq)
		
	return np.squeeze(snr)

#############################################################################################################
#############################################################################################################



