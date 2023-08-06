"""
gengli.glitch_generator
=======================
	Implementation of the class ``glitch_generator``. The class does everything you wish (and more) with the glitch generation...
"""

from .ctgan import model
import os
import torch
import numpy as np
import time
import scipy.signal
from .utils import compute_distance_matrix, compute_snr, read_psd
import warnings
import itertools
from tqdm import tqdm

import os
import ray
import inspect


################################################################################################
################################################################################################

class glitch_generator():
	"""
	Class to generate a glitch. It creates an instance of the network at initialization and offers a number of method to sample random glitches for the network.
	"""
	def __init__(self, detector = None, weight_file = None, input_size = 100):
		"""
		Instantiate the ctgan and initialize a number of useful attributes
		
		Parameters
		----------
		detector: str
			String with the detector name (only used to load a pre-fitted model). Accepted values are "H1" or "L1".
			
		weight_file: str
			Path with a file holding valid weights for the generator
			
		input_size: int
			Input for the random vector. It is **not** advised to change the default value (100).
		"""
		self.allowed_types = ['blip']
		
		if not isinstance(weight_file, str):
			if not isinstance(detector,str):
				raise RuntimeError("If no file for the weights of the generator is given, an iterferometer must be specified to load the proper default model")
			assert str(detector).upper() in ['H1', 'L1'], "`detector` variable must be either 'H1' or 'L1', '{}' given".format(detector)
			dir_weights = os.path.dirname(inspect.getfile(glitch_generator))+"/ctgan/weights/"
			self.weight_file = dir_weights+'blip_'+str(detector).upper()+'_CTGAN_state_G.pth'
		else:
			self.weight_file = weight_file

		# Check cuda device
		if torch.cuda.is_available():
			self.device = torch.device("cuda:0")
		else:
			self.device = torch.device("cpu")

		#TODO: Deal better with all this magic numbers...
		
		# Length of noise
		self.input_size = input_size

		# Number of channels (to be set when loading the model)
		self.num_channel_G = None

		# Setting the D and G with random weigths
		self.load_generator_weights(self.weight_file)
		
		# Some benchmark initialization
		self.benchmark_set = None
		self.benchmark_srate = None
		self.distance_matrix = None
		self.metric_hist = None

		return 

	def load_generator_weights(self, weight_file):
		"""
		Loads the weight of the generator network
		"""
		if not os.path.exists(weight_file):
			msg = "Unable to find the weights for the generator! File '{}' does not exist".format(weight_file)
			raise FileNotFoundError(msg)
		try:
			dict_weights = torch.load(weight_file, map_location = self.device)
			self.num_channel_G = dict_weights['conv5.2.running_var'].shape[0]
		except:
			raise ValueError("The input file for the weights is not valid. Are you sure it is suitable for the generator?")

		self.netG = model.GenerativeNet(self.num_channel_G)
		self.netG.load_state_dict(dict_weights)
		self.netG.eval()
		self.netG = self.netG.to(self.device)
		return

	def _check_type(self, glitch_type):
		"Checks whether the given glitch type is allowed"
		if glitch_type.lower() not in self.allowed_types:
			raise ValueError("Wrong type '{}' for the glitch specified. Allowed types are: '{}'".format(glitch_type,self.allowed_types) )
		return True
	
	def get_raw_glitch(self, n_glitches = 1, srate = 4096., glitch_type='Blip', seed = None):
		"""
		Returns a raw time domain glitch of the given type, as a ``np.array``.
		
		Parameters
		----------
	
		n_glitches: int
			The number of glitches to generate
			
		srate: float
			Sampling rate for the given glitch

		glitch_type:
			Type for the glitch to generate. The available types are available with `glitch_generator.allowed_types`
			
		seed: int
			Seed for the random glitch generation. If `None` no seed is set.
		
		Returns
		-------
	
		glitch: np.ndarray
			An array holding the glitch. Each row holds a different glitch
		"""
		self._check_type(glitch_type)
		
		if isinstance(seed, int): torch.manual_seed(seed)
		
		fixed_noise = torch.randn((n_glitches, 1,
									   self.input_size),
									  device=self.device)
		with torch.no_grad():
			glitch = self.netG(fixed_noise).detach().cpu()
			glitch = np.asarray(np.squeeze(glitch.detach().cpu().numpy()))
		
		if srate != 4096.: glitch = self.resample_glitch(glitch, 4096., srate)
		
		return glitch

	def resample_glitch(self, glitch, srate, new_srate):
		"""
		Convenience wrap to scipy.signal.resample to change the sampling rate of a glitch
		
		Parameters
		----------
		glitch: np.ndarray
			An array holding one or several glitches
			
		srate: float
			Sampling rate of the given glitch
			
		new_srate: float
			Sampling rate at which the new glitch should be evaluated
		
		Returns
		-------
		resampled_glitch: np.ndarray
			New resampled glitch
		
		"""
	
		old_length = glitch.shape[-1]  #(N,D)
		new_length = int(old_length*new_srate/srate)
		# we resample to desired sampling rate with scipy
		resampled_glitch = scipy.signal.resample(glitch, new_length, axis = -1)  # (938, 1) --> (new_length, 1)
		
		return resampled_glitch


	def initialize_benchmark_set(self, n_glitches=100, srate=4096., glitch_type='Blip'):
		"""
		Initialize an internal set of glitches. They will be used to measure the anomaly score of each newly generated glitch

		Parameters
		----------
		n_glitches: int
			Size of the glitch benchmark set (i.e. number of glitch to include in the set)
		
		rate: float
			Sampling rate for the glitch
		
		glitch_type:
			Type for the glitch to generate. The available types are available with `glitch_generator.allowed_types`
		
		Returns
		-------
		fake_set: np.ndarray
			Generated benchmark set for the glitches
		"""
		self._check_type(glitch_type)
			
		self.benchmark_srate = srate

		start = time.time()
		self.benchmark_set = self.get_raw_glitch(n_glitches, srate, glitch_type)
		#print('Initializing data set took {} seconds.'.format(np.round(time.time() - start, 6))) #DEBUG print
		
		ray.init(log_to_driver=False)
		self.distance_matrix = compute_distance_matrix(self.benchmark_set, self.benchmark_set)
		ray.shutdown()
		
			#creating an histogram of distances
			#(ugly, but works...)
		self.metric_hist = np.array([ self.distance_matrix[i,j,:] for i,j in itertools.product(range(n_glitches), range(n_glitches)) if i>j]) #(N*(N-1)/2, 3)
		
		return self.benchmark_set

	def get_len_glitch(self, srate = 4096.):
		"""
		Computes the length of the generated glitch with a given sampling rate
		
		Parameters
		----------
		srate: float
			Sampling rate of the glitch

		Returns
		-------
		length: int
			Length of the time grid th glitch is evaluated at
		"""
		#print(self.get_raw_glitch(n_glitches = 1, srate = srate).shape[0], int(938*srate/4096.)) #to test this...
		#return self.get_raw_glitch(n_glitches = 1, srate = srate).shape[0]
		return int(938*srate/4096.)
	
	def get_fft_grid(self, srate = 4096.):
		"""
		Returns the frequency grid on which the glitch is evaluated after the rfft (as in `np.fft.rfft`)
		Wrapper to `np.fft.rfftfreq`.
		
		Parameters
		----------
		srate: float
			Sampling rate of the glitch

		Returns
		-------
		f_grid: np.ndarray
			Frequency grid on which the frequency domain glitch is evaluated
		"""
		return np.fft.rfftfreq(self.get_len_glitch(srate), 1./srate)

	def colour_glitch(self, glitch, psd, srate = 4096., flow = 30., fhighpass = 250):
		"""
		Given a whithened glitch, it returns the coloured version of it.
		No checks are being done on the PSD, which is assumed to be evaluated on the same grid as `np.fft.rfft`. To generate such PSD from file, it is advisable to use the function `gengli.noise.read_psd`.
		The glitches are strongly highpassed to ensure quality of reconstruction: user is not recommend to change the default value
		
		Parameters
		----------
		glitch: np.ndarray
			Batch of glitches to be coloured
			
		psd: np.ndarray
			A psd suitable for the glitch. It is advisable to generate it with `gengli.noise.read_psd`
		
		srate: float
			Sampling rate for the glitch (it must match the sampling rate of the PSD)
		
		flow: float
			Low frequency cutoff for the PSD
		
		fhighpass: float
			High frequency cutoff for the low pass filter. If ``None``, no filtering will be applied
			The default value of ``250 Hz`` is the standard high frequency cutoff for a blip glitch.
		
		Returns
		-------
		coloured_glitch: np.ndarray
			Batch of couloured glitches, according to the given PSD
		"""
		glitch = np.asarray(glitch)
		
			#Doing FFT
		glitch_fft = np.fft.rfft(glitch, axis =-1) #(N,D')
			#Enforcing low frequency cutoff
		ids_kill = np.where(self.get_fft_grid(srate)<flow)[0]
		glitch_fft[...,ids_kill] = 0. #killing the ids where the glitch should be zero frequency
			#Recolouring
		coloured_glitch = np.fft.irfft(glitch_fft*np.sqrt(psd), axis = -1)
		
			#High-passing (otherwise it's crap)
		order = 3 #order of the filter (is it a good default?)
			#FIXME: how shall we high filter the glitches?
		normal_cutoff = fhighpass/(0.5*srate) #fhigh/nyquist
		b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
		coloured_glitch = scipy.signal.filtfilt(b, a, coloured_glitch, axis = -1)
		
		
		if False: #DEBUG
			import matplotlib.pyplot as plt
			fig, ax = plt.subplots(2,1, sharex = True)
			ax[0].plot(self.get_fft_grid(srate), glitch_fft.T, label = 'original')
			ax[1].set_xscale('log')
			ax[1].loglog(self.get_fft_grid(srate), psd)
		
			plt.show()

		return coloured_glitch

	def get_glitch(self, n_glitches=1, glitch_type='Blip', srate=4096., flow=30., SNR=None, psd=None, confidence_interval=None, alpha_tukey = 0.5, fhighpass = 250, seed = None):
		"""
		Generate a random glitch from the GAN.
		The user can set a sampling rate as well as the glitch SNR and starting frequency. If a PSD object is provided, the glitch will be colored according to the given PSD.
		The glitch will be windowed with a Tukey window, to make it suitable for injection in real data.

		Parameters
		----------
		n_glitches: int
			Number of glitches to generate
				
		glitch_type:
			Type for the glitch to generate. The available types are available with `glitch_generator.allowed_types`
				
		srate: float
			Sampling rate for the glitch
				
		flow: float
			Low frequency of the generated glitches (in Hz). Default and recommended value is 20 Hz

		SNR: float
			SNR of the given glitches. If a list/np.array is given, each entry is understood as the SNR of each glitch.
			If `None`, the glitches will not be scaled
			
		psd: np.ndarray
			A PSD. It will be used to colour the glitch with the given PSD. If None, no colouring will be done.
			If a string is given, it must be one of the analytical psd supported by pycbc (``pycbc.psd.get_lalsim_psd_list``)
			
		confidence_interval: tuple
			An interval of floats, each between 0 and 1. If not `None`, it will generate only glitches with an anomaly score percentile in the given range.
			The anomaly score is computed with `gengli.metric.compute_metrics`.
		
		alpha_tukey: float
			Value (0,1) for the Tukey window alpha parameter (see `scipy.signal.windows.tukey <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.tukey.html#scipy.signal.windows.tukey>`_)
			If `None`, no windowing will be performed.
		
		fhighpass: float
			High frequency cutoff for the low pass filter applied when colouring the glitch. If ``None``, no filtering will be applied.
			If a whithened glitch is returned (``psd = None``), the option has no effect.
			The default value of ``250 Hz`` is the standard high frequency cutoff for a blip glitch.
		
		seed: int
			Seed for the random glitch generation. If `None` no seed is set.
		
		Returns
		-------
		glitches: np.ndarray
			Array keeping the generated glitches
		"""
		if SNR is not None:
			SNR = np.squeeze(np.asarray(SNR))
			assert SNR.shape in ((), (n_glitches,)), "The SNR must be either a float or an array/list with shape (n_glitches, ). Given shape {} but expected {}".format(SNR.shape, (n_glitches,))
		
			#if too many glicthes are required, you should generate them in batches
		n_glitches_max = 1000 #Hardcoded maximum number of glitches to generate at once
		if n_glitches>n_glitches_max:
			glitches = []
			if isinstance(seed, int): torch.manual_seed(seed)
			for i in range(0, n_glitches, n_glitches_max):
				if SNR is not None: SNR_ = SNR[i:i+n_glitches_max] if SNR.ndim>0 else SNR
				else: SNR_ = SNR
				glitches.append(np.atleast_2d(
					self.get_glitch(min(n_glitches_max, n_glitches - n_glitches_max*len(glitches)),
						glitch_type, srate, flow, SNR_, psd, confidence_interval, seed = None)
					))
			return np.concatenate(glitches, axis =0)

		self._check_type(glitch_type)

		start = time.time()
		
			#initializing the benchmark_set (if it is the case AND if it's not already initialized)
		if isinstance(confidence_interval, tuple) and srate != self.benchmark_srate:
			self.initialize_benchmark_set(srate=srate, glitch_type=glitch_type)
		
		glitches = self.get_raw_glitch(n_glitches, srate, glitch_type, seed)
			
			#Computing confidence metric and generating glitches (if it's the case)
		if isinstance(confidence_interval, tuple):
			#raise NotImplementedError("Confidence interval support is not implemented yet! DO IT PLEASE!")
			glitches = np.atleast_2d(glitches)
			
			ray.init(log_to_driver=False)
			glitches_ok = []
			
				#tqdm stuff
			def dummy_it():
				while True:
					yield

			out_str='Generated {}/{} glitches in the confidence interval [{},{}]'
			pbar = tqdm(dummy_it(), desc = out_str.format(0,n_glitches,*confidence_interval))

			for _ in pbar:			
				new_distance_matrix = compute_distance_matrix(self.benchmark_set, glitches) #(N_benchmark, N_glitches, 3)
				
				new_distance_avg = np.mean(new_distance_matrix, axis = 0) #(N_glitches, 3)
				
				percentiles = np.percentile(self.metric_hist, [*confidence_interval], axis =0)#(2,3)
				
				ids_ok = np.logical_and(new_distance_avg>percentiles[0,:], new_distance_avg<percentiles[1,:]) #(N_glitches, 3)
				ids_ok = np.sum(ids_ok, axis =1).astype(bool) #(N_glitches, )
				
				if len(ids_ok)>0:
					glitches_ok.append(glitches[ids_ok,:])
				
				if len(glitches_ok)>0:
					N = np.sum([g.shape[0] for g in glitches_ok])
					pbar.set_description(out_str.format(N,n_glitches, *confidence_interval))
					if N>= n_glitches: break
				
				glitches = np.atleast_2d(self.get_raw_glitch(n_glitches, srate, glitch_type, None))
			
			glitches = np.concatenate(glitches_ok, axis =0)[:n_glitches,:]
			glitches = np.squeeze(glitches)
			
			ray.shutdown()
						
			#Enforcing flow by filtering with scipy.signal.butter
			#Creating an high pass filter
		if flow<30.: warnings.warn("It was asked for a frequency lower than the minimum frequency content of the glitch (30 Hz). The bandpassing will be omitted")
		if flow > 30.:
			order = 3 #order of the filter (is it a good default?)
			nyq = 0.5 * srate
			normal_cutoff = flow / nyq
			b, a = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
			glitches = scipy.signal.filtfilt(b, a, glitches, axis = -1)

			#Colouring according to the given PSD object
		if isinstance(psd, str):
				#reading an analytical PSD from pycbc
			psd = read_psd(psd, srate, glitches.shape[-1], flow = flow)
		if isinstance(psd, np.ndarray):
			window = scipy.signal.windows.tukey(glitches.shape[-1], alpha= 0.5 if alpha_tukey is None else alpha_tukey, sym=True)
			glitches = glitches*window
			glitches = self.colour_glitch(glitches, psd, srate, flow, fhighpass)
		
			#Scaling to the user given SNR
		if isinstance(SNR, np.ndarray):
				 #Computing the actual SNR. For whithened glitches we use np which is wayyy faster
			if psd is None: true_SNR = np.sqrt(2./srate*np.sum(np.square(glitches), axis =-1)) #(N,)
			else: true_SNR = compute_snr(glitches, srate, psd = psd, flow = flow)
			glitches = (glitches.T * SNR/true_SNR).T 
				
				#some old garbage
			#SNR_TD = np.sum(np.square(glitches), axis =-1)
			#SNR_FD = np.sum(np.conj(np.fft.fft(glitches))*np.fft.fft(glitches), axis =-1)/len(glitches)
			#print("FD and TD: ", SNR_FD, SNR_TD)

			#windowing the glitches (no matter what)
		if isinstance(alpha_tukey, float):
			window = scipy.signal.windows.tukey(glitches.shape[-1], alpha=alpha_tukey, sym=True)
			glitches = glitches*window

		return glitches






