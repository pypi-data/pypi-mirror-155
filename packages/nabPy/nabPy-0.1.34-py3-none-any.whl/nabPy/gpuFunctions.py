#this file contains the GPU version of the various functions
#it is not always imported. The script basicFunctions determines if this is imported or not

import numpy as np
import sys, os
import dask.array as da

import cupy as cp
import cupyx as cpx
from cupyx.scipy.fft import get_fft_plan
import cupy_backends
from cupy.cuda import cufft
import numba
from numba import vectorize, cuda, jit

from . import basicFunctions as bf

@cuda.jit("(float32[:,:], int32[:], int32, int32, float32, int32, int32, complex64[:])")
def extractTrapResultsGPU(filtered, maxlocs, rise, top, percentage, shift, batchsize, out):
	i = cuda.grid(1)
	if i < batchsize:
		wave = filtered[i]
		wavelen = filtered.shape[1]
		maxloc = maxlocs[i]
		maxval = wave[maxloc]
		threshold = maxval * percentage
		#find upwards cross point
		#iterate from the max location back towards beginning
		i = maxloc
		found = False
		leftCross = None
		rightCross = None
		while i >= maxloc - rise - top and found == False and i >= 0:
			if wave[i] >= threshold and wave[i-1] <= threshold:
				found = True 
				leftCross = i
			i-= 1
		rightCross = None
		found = False
		i = maxloc
		while i <= maxloc + rise + top and found == False and i <= wavelen-1:
			if wave[i-1] >= threshold and wave[i]<= threshold:
				found = True
				rightCross = i
			i+=1
		#now use these to extract the results
		if rightCross is None or leftCross is None:
			out[i] = np.complex64(complex(np.nan, np.nan))
		else:
			midpoint = (leftCross + rightCross)/2
			out[i] = np.complex64(complex(wave[int(midpoint)+shift],  midpoint - top/2 - rise))


def gpuTrapFilterImplementation(waves, rise, top, tau, percentage, pretrigger = 800, shift = 0, hdf5ChunkSize = 100):
	"""
	This is a more efficient form of convolution using the FFTW library. 
	It's more efficient than the standard numpy/scipy/dask implementations
	
	Parameters
	----------
	waves: np.ndarray or dask.ndarray
		Input waveforms
	
	inputFilter: np.ndarray
		The filter input to the function
	
	rise, top, tau: see Nab.bf.defineSingleTrap
	
	percentage: between 0 and 1
		threshold cross percentage used for extraction
	
	pretrigger: int
		length of window of waveform before the daq trigger expected location
	
	shift: int
		energy extraction point
	
	minBatchSize: int
		the smallest a batch can be. Based on the HDF5 chunking behavior. This is the HDF5 chunk size
	"""
	#iterate over the chunks in the dask array
	if type(waves) == np.ndarray:
		waves = da.asarray(waves, chunks = {0: 'auto', 1: -1})
	#now create the various arrays and plans
	#get chunk sizes and waveform length information
	numWaves, waveformLength = waves.shape
	inputFilter = bf.defineSingleTrap(rise, top, tau, rise*2+top)
	filterLength = len(inputFilter)
	padLength = waveformLength + filterLength - 1
	padLength = cpx.scipy.fft.next_fast_len(padLength) #does the clever padding trick to improve performance
	while padLength % 2 != 0:
		padLength = cpx.scipy.fft.next_fast_len(padLength+1)
	daskChunkSize = int(np.max(waves.chunks[0]))
	#need to determine the best size for the GPU, normally this is around 1000 or so at a time
	blockSize = waves.blocks[0].shape[0]
	batch = cpx.zeros_pinned((blockSize, padLength), dtype=waves.dtype)#allocate pinned host memory, size of the original waveforms with padding
	gpuWaves = cp.empty((blockSize, padLength), dtype=waves.dtype) #allocate gpu memory, size of each dask block but with padding             # 
	means = cp.empty(waves.blocks[0].shape[0], dtype=np.float32)
	gpuResults = cp.empty(blockSize, dtype=np.csingle)
	planForward = cpx.scipy.fft.get_fft_plan(gpuWaves, axes=1, value_type='R2C') #create the fft plan
	fftWaves = cp.empty((blockSize, padLength//2+1), dtype=np.complex64) #allocate fft results storage
	planReverse = cpx.scipy.fft.get_fft_plan(fftWaves, axes=1, value_type='C2R') #create the fft plan
	#prep the filter for the GPU
	maxlocs = cp.empty(blockSize, dtype=np.int32)

	paddedFilter = np.zeros(padLength)
	paddedFilter[:filterLength] = inputFilter[:]
	fftFilter = np.transpose(np.fft.rfft(paddedFilter), None)
	fftFilterGPU = cp.array(fftFilter) #move the fft filter over to GPU
	results = cpx.zeros_pinned(len(waves), dtype=np.csingle) #allocate the results storage
	threadsperblock = 32 #set up the blocks
	blockspergrid = int(np.ceil(blockSize/threadsperblock))
	currLoc = 0
	
	for d in waves.blocks: #iterate over the blocks of data in the dask array
		blockSize = d.shape[0] #figure out how many waveforms are here
		blockStart = currLoc
		blockStop = blockStart + blockSize
		batch[:blockSize,:waveformLength] = d.compute()#move into the pinned memory container
		gpuWaves.set(batch) #copy these over, now the full block is on the GPU
		#some of the calculations can be better handled in bulk like this
		cp.mean(gpuWaves[:,:pretrigger], axis = 1, out = means)
		gpuWaves[:,:waveformLength] = cp.subtract(gpuWaves[:,:waveformLength], means[:,None])
		#now the waveforms have been shifted over to have their baselines nicely lined up around 0
		#now iterate within this block
		fftWaves = cpx.scipy.fft.rfft(gpuWaves, plan = planForward) #do the FFT
		#do the multiplication with the filter
		fftWaves *= fftFilterGPU #we are assuming the filter has been normalized doing it this way
		#now do the reverse FFT
		gpuWaves[:] = cpx.scipy.fft.irfft(fftWaves, plan = planReverse)
		#find the max values for the trap filter extraction later
		cp.argmax(gpuWaves, axis=1, out = maxlocs)
		#now with the results of the convolution stored here, do the filtering
		extractTrapResultsGPU[blockspergrid, threadsperblock](gpuWaves, maxlocs, rise, top, percentage, shift, blockSize, gpuResults)
		gpuResults[:blockSize].get(out = results[blockStart:blockStop])
		currLoc=blockStop
	del batch
	del gpuWaves
	del means
	del gpuResults
	del planForward
	del planReverse
	del fftWaves
	del maxlocs
	del paddedFilter
	del fftFilter
	del fftFilterGPU
	return results
