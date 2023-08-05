
# Jaesub Hong (jhong@cfa.harvard.edu)

import cjson
from collections import OrderedDict

import pandas
import astropy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize, LogNorm
import matplotlib.cm	 as cm
import matplotlib		 as mpl
from matplotlib.patches		import Circle
from matplotlib			import rc,rcParams
from matplotlib.ticker		import LogLocator
#from mpl_toolkits.axes_grid1  import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import tabletool as tt
import numpy as np
import math

from astropy.io import fits

from scipy import optimize as opt
from scipy import ndimage

from os		import path
from functools	import wraps

from IPython	import embed

def help_rcParams():
	text=OrderedDict()
	text["figure.figsize"       ] ="changes the figure size; keeps the font size the same"
	text["figure.dpi"		    ] ="changes the figure size; keep relative size of font to figure the same"
	text["font.size"		    ] ="change the font size; keeps the figure size the same"

	text["axes.labelsize"	    ] ="Fontsize of the x and y labels"
	text["axes.titlesize"	    ] ="Fontsize of the axes title"
	text["figure.titlesize"	    ] ="Size of the figure title (Figure.suptitle())"
	text["xtick.labelsize"	    ] ="Fontsize of the tick labels"
	text["ytick.labelsize"	    ] ="Fontsize of the tick labels"
	text["legend.fontsize"	    ] ="Fontsize for legends (plt.legend(), fig.legend())"
	text["legend.title_fontsize"] ="Fontsize for legend titles, None sets to the same as the default axes."
	return text

def help_text(param):
	if param != None:
		if param == "basics":
			print("rcParams:")
			cjson.show(help_rcParams(),  notype=True)
			print("e.g., -*#rcParams:figure.figsize '12,10'")
		else:
			print("available help words: basics")
		exit()

#----------------------------------------------------------------------------------------
class LogNorm_mid(LogNorm):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		LogNorm.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [np.log(self.vmin), np.log(self.mid), np.log(self.vmax)], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(np.log(value), x, y))

class Norm_mid(Normalize):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		Normalize.__init__(self,vmin=vmin, vmax=vmax, clip=clip)
		self.mid=mid
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.mid, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

#----------------------------------------------------------------------------------------
def read(infile, x=None, y=None, hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True):
	if type(data).__name__ == "NoneType":
		if infile == None: 
			print("input data or file is required.")
			return None, None, None, None, None 

		if not path.isfile(infile):
			print("cannot read the file:", infile)
			return None, None, None, None, None

		data=tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if x == None or y == None:
		if   type(data) is pandas.core.frame.DataFrame: colnames=data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames=data.colnames
		else: print('need to know column names or provide -x and -y')

#		colnames=data.colnames
		if x == None: x=colnames[0]
		if y == None: y=colnames[1]
	
	# default label
	if xlabel == None:
		xlabel = x 
		if hasattr(data[x],'info'):
			if hasattr(data[x].info,'unit'):
				xunit=data[x].info.unit
				if xunit != None: xlabel = xlabel +' ('+str(xunit)+')'

	if ylabel == None:
		ylabel = y 
		if hasattr(data[y],'info'):
			if hasattr(data[y].info,'unit'):
				yunit=data[y].info.unit
				if yunit != None: ylabel = ylabel +' ('+str(yunit)+')'

	return data, x, y, xlabel, ylabel
	
def minmax(data, nonzero=False):
	if nonzero: 
		data=np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

def set_range(data, margin=None, 
		dr=None, # data range
		scale='linear', drawdown=None):

#	embed()
	if type(dr) is list: 
		if dr[0] == None: dr = None
	
	if type(dr).__name__ == 'NoneType': dr= minmax(data, nonzero= scale != 'linear')

	if margin != None:
		dr = add_margin(dr, margin=margin, scale=scale, drawdown=drawdown)

	return dr

def set_range_2D(xdata, ydata, margin=None, xr=None, yr=None, 
		xscale='linear', yscale='linear', drawdown=None):

#	embed()
	if type(xr) is list: 
		if xr[0] == None: xr = None
	if type(yr) is list: 
		if yr[0] == None: yr = None
	
	if type(xr).__name__ == 'NoneType': xr= cjson.minmax(xdata, nonzero= xscale != 'linear')
	if type(yr).__name__ == 'NoneType': yr= cjson.minmax(ydata, nonzero= yscale != 'linear')

	if margin != None:
		if type(margin) is not list:
			xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
		elif len(margin) == 2:
			xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
		elif len(margin) == 4:
			xr = add_margin(xr, margin=margin[0:1], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[2:3], scale=yscale, drawdown=drawdown)

	return xr, yr

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0],10), math.log(vr[1],10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin == None     : margin=[0.2,0.2]
	elif np.isscalar(margin): margin=[margin, margin]
	if scale == 'linear':
		diff=prange[1]-prange[0]
		prange=[prange[0]-margin[0]*diff,prange[1]+margin[1]*diff]
	else:
		if prange[0] <= 0.0:
			if drawdown == None: drawdown = 1.e-5
			prange[0]=prange[1]*drawdown

		logpr = [math.log(v,10) for v in prange]
		diff = logpr[1]-logpr[0]
		logpr=[logpr[0]-margin[0]*diff,logpr[1]+margin[1]*diff]
		prange=[10.0**v for v in logpr]

	return prange

def filter_by_range(xdata, ydata, xr, yr, weights=None):
#	embed()
#	xdata=np.array(xdata)
#	ydata=np.array(ydata)
	mask = (xdata >= xr[0]) & (xdata <= xr[1]) & (ydata >= yr[0]) & (ydata <= yr[1]) 
	xdata=xdata[mask]
	ydata=ydata[mask]

	if type(weights).__name__ != 'NoneType':
		weights=weights[mask]
#	if filter:
#		 data=data[data[x] >= xr[0]]
#		 data=data[data[x] <= xr[1]]
#		 data=data[data[y] >= yr[0]]
#		 data=data[data[y] <= yr[1]]

	return xdata, ydata, weights

def val2pix(val, vr=None, pr=None):
	# value to pixel
	slope=(pr[1]-pr[0])/(vr[1]-vr[0])
	if type(val) is not list:
		return int(slope*(val-vr[1])+pr[0])
	return [int(slope*(v-vr[1])+pr[0]) for v in val]

def pix2val(pix, vr=None, pr=None):
	# pixel to value
	slope=(vr[1]-vr[0])/(pr[1]-pr[0])
	if type(pix) is not list:
		return slope*(pix-pr[0])+vr[0]
	return [slope*(p-pr[0])+vr[0] for p in pix]

#----------------------------------------------------------------------------------------
def set_rcParams(rcParams=None, verbose=0):
	if rcParams == None: return
	for key, val in rcParams.items():
		if verbose >=2: print(key,val)
		plt.rcParams[key] = val
	
def set_fig_basics(figsize=None, dpi=None, fontsize=None, 
		legendsize=None, titlesize=None):
	# changes the figure size; keeps the font size the same
	if figsize != None: 
		plt.rcParams["figure.figsize"] = (float(figsize[0]), float(figsize[1]))

	# changes the figure size; keep relative size of font to figure the same
	if dpi != None: 
		plt.rcParams["figure.dpi"] = int(dpi)

	# change the font size; keeps the figure size the same
	if fontsize != None:
		plt.rcParams["font.size"] = float(fontsize)

	# xx-small, x-small, small, medium, large, x-large, xx-large, smaller, larger.

	if legendsize != None:
		plt.rcParams["legend.fontsize"] = legendsize

	if titlesize != None:
		plt.rcParams["axes.titlesize"] = titlesize

#----------------------------------------------------------------------------------------
def wrap(plt, xr, yr, xlabel, ylabel, 
		title="", xscale='linear', yscale='linear', outfile=None, 
		grid=None,
		y_title=1.0, rect=[0,0,1,1],
		label=True, display=True, ion=False):

	if label:
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
#		print('rect',rect)
		# this needs a clean up
		plt.title(title, y=y_title)

	if grid != None: plt.grid()
	plt.xlim(xr)
	plt.ylim(yr)
	plt.xscale(xscale)
	plt.yscale(yscale)
	plt.tight_layout(rect=rect)
	if not ion: 
		if outfile != None: 
			plt.savefig(outfile)
			plt.close("all")
		else: 
			if display: plt.show()

def colorbar(cbar, im, ax, fig, orientation=None, ticks_position=None):
	cax = ax.inset_axes(cbar) #, transform=ax.transAxes)
	fig.colorbar(im, 
			orientation=orientation,
			cax=cax)
	if ticks_position != None:
		if ticks_position == 'left' or ticks_position == 'right':
			cax.yaxis.set_ticks_position(ticks_position)
		if ticks_position == 'bottom' or ticks_position == 'top':
			cax.xaxis.set_ticks_position(ticks_position)

def colorbar_set(cbar, im, ax, fig, 
		xlabel=None, ylabel=None, title=None,
		off=None, width=None, length=None, rect=[0.,0.,1.,1.],
		orientation=None, outside=False):

	if not outside:
		if off    == None: off    = 0.03
		if width  == None: width  = 0.03
		if length == None: length = 0.5-off
		loff = 1.0-length-off
		woff = 1.0-width-off
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'lower,right':
				rect=[woff,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				rect=[off,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,left':
				rect=[off,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'lower,right':
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,right':
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
	else:
		if width  == None: width  = 0.03
		if length == None: length = 0.5
		if off    == None: off    = -0.10 - width
		loff = 0.5
		woff = 1.02
		y=rect[3]+(rect[3]-1)*20.
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='top')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='bottom')
			elif cbar == 'lower,right':
				rect=[woff,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			ax.set_title(title, y=y)
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				ax.set_xlabel(xlabel,loc='right')
				ax.set_title(title, y=y)
				rect=[0,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,left':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='right')
				rect=[0,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'lower,right':
				ax.set_xlabel(xlabel, loc='left')
				ax.set_title(title,y=y)
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,right':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='left')
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			ax.set_ylabel(ylabel)

def despine_axes(ax, despine):
	if despine == None: despine = False
	if type(despine) is bool:
		if despine:
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
	else:
		for each in despine.split(','):
			ax.spines[each].set_visible(False)

#----------------------------------------------------------------------------------------
def hist2line(edges, values):
	x, y = [edges[0]], [values[0]]
	for i in range(1, len(values)):
		x.append(edges[i])
		x.append(edges[i])
		y.append(values[i-1])
		y.append(values[i])
	x.append(edges[-1])
	y.append(values[-1])
	return x, y

#----------------------------------------------------------------------------------------
def prep_data_deco(func):

	@wraps(func)
	def prep_data(*args, xdata=None, ydata=None, weights=None,
			data=None, image=None, infile=None, x=None, y=None, xlabel=None, ylabel=None, 
			xr=None, yr=None, margin=0.0, drawdown=None, filter=False,
			xscale=None, yscale=None, xlog=False, ylog=False, 
			rcParams=None, figsize=None, dpi=None, 
			clip=None,  # pixel coordinates
			fontsize=None, legendsize=None, titlesize=None, verbose: int=0,
			ftype=None, hdu=None, help=None, **kwargs):

		help_text(help)

		loaded = None

		# try loading an image
		if type(image) is bool:
			if image:
				# read image
				# assume fits image for now
				hdul=fits.open(infile)
				if hdu == None: hdu=0
#				image=np.transpose(hdul[hdu].data)
				image=hdul[hdu].data
				loaded='image'
		elif type(image).__name__ != "NoneType":
			loaded='image'

		# make sure 2-d image and clip if requested
		if loaded == "image":
			ndim = image.ndim
			if ndim == 3: 
				image = image.sum(axis=0)
			image=np.transpose(image)
			#print(image.shape)

			if type(clip) is list:
				# x and y seem to be swapped
				#image=image[clip[2]:clip[3],clip[0]:clip[1]]
				image=image[clip[0]:clip[1],clip[2]:clip[3]]

			nbinx, nbiny=image.shape
			#print(nbinx,nbiny)
			if type(clip) is not list:
				if xr == None: xr=[0,nbinx]
				if yr == None: yr=[0,nbiny]
			else:
				if xr == None: xr=[clip[0],clip[1]]
				if yr == None: yr=[clip[2],clip[3]]

		# if there is no image then try loading a table
		if type(xdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
					xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
			if type(data).__name__ == "NoneType": return False

			xdata=data[x]
			ydata=data[y]
			loaded='table'

		if xscale == None: 
			xscale = 'log' if xlog else 'linear'
		if yscale == None: 
			yscale = 'log' if ylog else 'linear'

		xr, yr =  set_range_2D(xdata, ydata, xr=xr, yr=yr, 
				margin=margin, drawdown=drawdown,
				xscale=xscale, yscale=yscale)

		if filter:
#			if loaded == 'table':
			if type(xdata).__name__ != 'NoneType':
				xdata, ydata, weights = filter_by_range(xdata, ydata, xr, yr, weights=weights)
				# need to clip the image

		set_rcParams(rcParams, verbose=verbose)
		set_fig_basics(figsize=figsize, dpi=dpi, fontsize=fontsize, 
				legendsize=legendsize, titlesize=titlesize)

		return func(*args, xdata=xdata, ydata=ydata, weights=weights,
			data=data, image=image, xlabel=xlabel, ylabel=ylabel, 
			xr=xr, yr=yr, xscale=xscale, yscale=yscale, 
			margin=margin, drawdown=drawdown,
			verbose=verbose, help=None, **kwargs)

	return prep_data

#----------------------------------------------------------------------------------------
@prep_data_deco
def plot1d(xdata=None, ydata=None, data=None, 
		xr=None, yr=None, 
		outfile=None, 
		xscale='linear', yscale='linear',
		xlabel=None, ylabel=None,  
		marker='.', linestyle='None', color=None,
		display=True,
		help=None, hold=False, verbose: int= 0, **kwargs):
	"""Plot 1-D from input table
	"""

	def show(ion=True):
		if ion: plt.ion()
		plt.plot(xdata, ydata,
				color=color,
				marker=marker, linestyle=linestyle)

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				display=display, ion=ion)

	show(ion=False)
	if hold: embed()

	return plt

@prep_data_deco
def dplot(xdata=None, ydata=None, image=None, data=None,
		xr=None, yr=None, zr=None,
		zmin=None, zmax=None, zoff=None,
		zmid=None,
		zlthresh=None, zlscale=None,
		outfile=None, 
		xscale=None, yscale=None,
		xedges=None, yedges=None,
		xlabel=None, ylabel=None, title=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, cmap='Blues', aspect='auto',
		interpolation=None, display=True, weights=None,
		cbar=True, cb_orientation='vertical', cb_ticks_position='right', cb_outside=False,
		cb_off=None, cb_width=None, cb_length=None, zclip=False,
		xhist=False, xh_height=0.15, xh_scale=None, 
		yhist=False, yh_height=0.15, yh_scale=None, 
		xslice=None, yslice=None, # data coordinateslike xr or yr (not necessarily pixels)
		halpha=0.3, hcolor="darkblue", hgap=0.04, hheight: float=0.15,
		despine=None, margin=0.0, drawdown=None,
		noplot=False,
		help=None, hold=False, verbose:int= 0):
	""" 2-d density plot 
	"""

	if type(image).__name__ == 'NoneType':
		# data points
		if binsize != None:  binx,  biny = binsize, binsize
		if nbin    != None: nbinx, nbiny = nbin,    nbin

		if binx==None:  binx = (xr[1]-xr[0])/nbinx
		else:          nbinx = int((xr[1]-xr[0])/binx)

		if biny==None:  biny = (yr[1]-yr[0])/nbiny
		else:          nbiny = int((yr[1]-yr[0])/biny)
		doimage=False
	else:
		# image input
		# assume xr, and yr is given, and probably no log scale for x and y axes?
		nbinx, nbiny = image.shape
#		ndim = image.ndim
#		if   ndim == 2: nbinx, nbiny = image.shape
#		elif ndim == 3: 
#			nbinz, nbinx, nbiny = image.shape
#			image = image.sum(axis=0)
		if zmax == None: zmax = np.max(image)
		if zmin == None: zmin = np.min(image)
		binx = (xr[1]-xr[0])/nbinx
		biny = (yr[1]-yr[0])/nbiny
		doimage=True


	if type(xedges).__name__ == 'NoneType':
		xedges = nbinx
		if xscale == 'log': xedges = get_log_edges(xr, nbinx)

	if type(yedges).__name__ == 'NoneType':
		yedges = nbiny
		if yscale == 'log': yedges = get_log_edges(yr, nbiny)

	bins = [xedges, yedges]

	if not doimage:
		# to get zmax
		heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins, weights=weights)
		if zmax == None: zmax=np.max(heatmap.T)
		if zmin == None: zmin=np.min(heatmap.T)

		if noplot: return heatmap.T, xedges, yedges
#		weights = None
	else:
		if type(xedges) is not list:
			xedges_ = [ii*binx+xr[0]+binx*0.5 for ii in range(0,nbinx)]
		else:
			xedges_ = [(v+w)*0.5 for v, w in zip(xedges[:-1:], xedges[1::])]

#		xdata   = xedges_ * nbiny
		xdata   = [[v]  * nbiny for v in xedges_]
		xdata   = np.array(xdata).flatten()

		if type(xedges) is not list:
			yedges_ = [ii*binx+yr[0]+binx*0.5 for ii in range(0,nbiny)]
		else:
			yedges_ = [(v+w)*0.5 for v, w in zip(yedges[:-1:], yedges[1::])]
#		ydata   = [[v]  * nbinx for v in yedges_]
#		ydata   = np.array(ydata).flatten()
		ydata   = yedges_ * nbinx

		weights = image.flatten()
		if zmax == None: zmax=np.max(weights)
		if zmin == None: zmin=np.min(weights)

	def show(ion=True):

		nonlocal zmin,zmax, zoff
		nonlocal zmid
		nonlocal zlthresh, zlscale
		nonlocal zclip
		fig, ax = plt.subplots()

		if ion: plt.ion()
		if not zlog:
			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

			if zmid != None:
#				norm=colors.TwoSlopeNorm(zmid, vmin=zmin, vmax=zmax)
#				print(zmin)
#				norm=Norm_mid(zmid, vmin=zmin, vmax=zmax)
				norm=colors.CenteredNorm(zmid) #, vmin=zmin, vmax=zmax)
			else:
				norm=colors.Normalize(vmin=zmin, vmax=zmax)

			image, xedges, yedges, im = ax.hist2d(xdata, ydata, bins=bins, 
					norm=norm,
					cmap=cmap, weights=weights)
			ax.set_aspect(aspect)
		else:
			# log, with negative

			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

			if zlog:
				zclip=True
#				zmin= 0.5 if zmin <= 0 else zmin

				# this only works when weights are auto-gen by image, 
				# but not true weight
#				if type(weights).__name__ != 'NoneType':
#					if doimage:
#						weights[weights<zmin]=zmin
				if zmin > 0:
					lognorm=colors.LogNorm(vmin=zmin, vmax=zmax, clip=zclip)
				elif zmin < 0:
					if zlthresh == None: zlthresh=-zmin
					if zlscale  == None: zlscale=-zmin/zmax
					lognorm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
#					lognorm=colors.PiecewiseNorm(flist=['linear','log'],refpoints_cm=[0.1], refpoints_data=[0.0], vmin=zmin, vmax=zmax, clip=zclip)
#					print(zoff,zmin,zmax)
#					if zoff  == None: zoff=zmax/1.e3
#					lognorm=colors.FuncNorm((lambda x: np.log10(x-zmin+zoff)-np.log10(zoff),
#							lambda x: zoff*(10.**x-1)+zmin), vmin=zmin, vmax=zmax, clip=zclip)
				else:
					if zlthresh == None: zlthresh=zmax/1.e3
					if zlscale  == None: zlscale=0.2
					lognorm=colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
#					lognorm=LogNorm_mid_offset(vmin=zmin, vmax=zmax, clip=clip, mid=zmid, offset=zoff)
#					print('zmin',zmin)
#					print('zmax',zmax)
#					print('zoff',zoff)
#					print('zmid',zmid)

#			norm = colors.LogNorm(vmin=zmin_, vmax=zmax)
			image, xedges, yedges, im = ax.hist2d(xdata, ydata, weights=weights,
#					norm=colors.LogNorm(vmin=zmin, vmax=zmax, clip=clip),
					norm=lognorm,
					bins=bins,  cmap=cmap)
			ax.set_aspect(aspect)
#			cm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

		if noplot: return image

		nonlocal cbar, despine, cb_outside, margin, xslice, yslice

		if xhist or yhist:
			if despine == None: despine=True
		despine_axes(ax, despine)

		y_title=1.0
		if xhist:
			nonlocal xh_height, xh_scale
			xax= ax.inset_axes([0,1.+hgap,1,hheight] , transform=ax.transAxes, sharex=ax)
			if yslice != None:
				if type(yslice) is not list: 
					p2v=pix2val([0,1], vr=yr, pr=[0,nbiny])
					p2v=p2v[1]-p2v[0]
					yslice=[yslice,yslice+p2v]
				pix_yslice=val2pix(yslice, vr=yr, pr=[0,nbiny])
				if pix_yslice[0] == pix_yslice[1]: pix_yslice[1]=pix_yslice[1]+1
				ax.plot([xr[0],xr[0]],yslice, marker='D', clip_on=True, color='black')
				ax.plot([xr[1],xr[1]],yslice, marker='D', clip_on=True, color='black')
				xh = image[:,pix_yslice[0]:pix_yslice[1]].sum(axis=1)
				if not doimage:
					pick = (ydata >= yslice[0]) & (ydata <= yslice[1])
					xdata_=xdata[pick]
					weights_=weights[pick]
					# something is wrong here
				#	xh = np.histogram(xdata_, bins=xedges)
				else:
					xdata_=xdata
					weights_=weights
			else:
				xh = image.sum(axis=1)
				xdata_=xdata
				weights_=weights

			xl, yl = hist2line(xedges, xh)
#			xax.plot(xl, yl,
			if not doimage:
				# can this be done in one shot?
				xh, xedges, _ = xax.hist(xdata_, bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, weights=weights_,
						alpha=halpha)
				xh, xedges, _ = xax.hist(xdata_, bins=xedges, histtype='step', 
						weights=weights_,
						edgecolor=hcolor)
			else:
				xh, xedges, _ = xax.hist(xdata[::nbiny], bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, weights=xh,
						alpha=halpha)
				xh, xedges, _ = xax.hist(xdata[::nbiny], bins=xedges, histtype='step', 
						weights=xh,
						edgecolor=hcolor)


			xax.set_xlim(xr)
			xax.set_xscale(xscale)
#			xax.set_xticklabels([])
			plt.setp(xax.get_xticklabels(), visible=False)
			plt.setp(xax.get_xlabel(), visible=False)

			if xh_scale == None:
				if zlog: 
					xax.set_yscale('log')
					xh_scale='log'
			else:
				xax.set_yscale(xh_scale)

#			print('margin',margin)
#			print('xh_height',xh_height)
#			xh_yr =  set_range(xh, 
#				margin=margin/pow(xh_height,0.3), drawdown=drawdown,
#				scale=xh_scale)
#			xax.set_ylim(xh_yr)

			despine_axes(xax, despine)

		if yhist:
			nonlocal yh_height, yh_scale
			if yh_height == None: yh_height=0.15
			yax= ax.inset_axes([1.+hgap,0.0,hheight,1] , transform=ax.transAxes, sharey=ax)
			yh = image.sum(axis=0)
			if xslice != None:
				if type(xslice) is not list: 
					p2v=pix2val([0,1], vr=xr, pr=[0,nbinx])
					p2v=p2v[1]-p2v[0]
					xslice=[xslice,xslice+p2v]
				pix_xslice=val2pix(xslice, vr=xr, pr=[0,nbinx])
				if pix_xslice[0] == pix_xslice[1]: pix_xslice[1]=pix_xslice[1]+1
				yh = image[pix_xslice[0]:pix_xslice[1],:].sum(axis=0)
				ax.plot(xslice,[yr[0],yr[0]], marker='D', clip_on=True, color='black')
				ax.plot(xslice,[yr[1],yr[1]], marker='D', clip_on=True, color='black')
				if not doimage:
					pick = (xdata >= xslice[0]) & (xdata <= xslice[1])
					ydata_=ydata[pick]
					weights_=weights[pick]
				else:
					ydata_=ydata
					weights_=weights
			else:
				yh = image.sum(axis=0)
				ydata_=ydata
				weights_=weights

			xl, yl = hist2line(yedges, yh)
#			yax.plot(xl,yl,
			if not doimage:
				yh, yedges, _ = yax.hist(ydata_, bins=yedges, 
						weights=weights_,
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yh, yedges, _ = yax.hist(ydata_, bins=yedges, 
						weights=weights_,
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')
			else:
				yh, yedges, _ = yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yh, yedges, _ = yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')

			yax.set_ylim(yr)
			yax.set_yscale(yscale)
			plt.setp(yax.get_yticklabels(), visible=False)
			if yh_scale == None:
				if zlog: 
					yax.set_xscale('log')
					yh_scale='log'
			else:
				yax.set_xscale(yh_scale)

#			yh_yr =  set_range(yh, 
#				margin=margin/pow(yh_height,0.3), drawdown=drawdown,
#				scale=yh_scale)

#			yax.set_xlim(yh_yr)
#			xax.axes.xaxis.set_visible(False)
#			xax.plot(xedges[1:], xh)
			despine_axes(yax, despine)

			if type(cbar) is bool:
				if cbar: 
#					if xhist or (title != None and title != ''):
					if xhist:
						cbar='lower,left'
						cb_orientation = 'vertical'
						cb_outside=True
					else:
						cbar = [0.0, 1.01, 1.0, 0.05]
#						cb_outside=True
						cb_orientation = 'horizontal'
						cb_ticks_position = 'top'
						y_title = 1.15


		hsize=hheight+hgap
		if xhist: 
			yhsize=0.05*hsize
			y_title=1.0+hsize
		else: yhsize=0.0
		if yhist: xhsize=0.05*hsize
		else: xhsize=0.0
		rect=[0,0,1.+xhsize, 1.0+yhsize]
		

		if type(cbar) is bool:
			if cbar: 
				if zlog:
					if zmin <=0:
#						lloc=LogLocator(subs=range(10))
#						lloc.tick_values(vmin=zlthresh,vmax=zmax)
						cb=fig.colorbar(im, pad=0.01)
#						cb.ax.yaxis.set_minor_locator(lloc)
					else:
						cb=fig.colorbar(im, pad=0.01)
				else:
					cb=fig.colorbar(im, pad=0.01)
#			cb.ax.minorticks_on()
#			print('here')
		elif type(cbar) is list:
			cbar=[float(v) for v in cbar]
			colorbar(cbar, im, ax, fig, 
					orientation=cb_orientation, 
					ticks_position=cb_ticks_position)
		elif type(cbar) is str:
			colorbar_set(cbar, im, ax, fig, 
					off=cb_off, width=cb_width, length=cb_length,
					xlabel=xlabel, ylabel=ylabel, title=title, rect=rect,
					orientation=cb_orientation, outside=cb_outside)
	
		wrap(plt, xr, yr, xlabel, ylabel, title=title, label=not cb_outside,
				rect=rect, y_title=y_title,
				xscale=xscale, yscale=yscale, 
				outfile=outfile, 
				ion=ion, display=display)
		return image

	image = show(ion=False)
	if hold: embed()

	return image, xedges, yedges

#----------------------------------------------------------------------------------------
@prep_data_deco
def collect_data(xdata=None, ydata=None, 
		xr=None, yr=None, 
		title=None,
		marker='.', linestyle='None', color=None,
		help=None, hold=False, verbose: int= 0, **kwargs):
	"""for multiple data set
	"""

#	print(xdata)

	return xdata, ydata, xr, yr, title, marker, linestyle, color

def mplot1d(xdata, ydata, xr, yr, title, marker, linestyle, color, 
		xlabel=None, ylabel=None, outfile=None, verbose=1,
		xscale='linear', yscale='linear',
		xexpr=None, yexpr=None, grid=True,
		display=True, ion=False, hold=False):
	"""Multiple Plot 1-D from input table
	"""

	pcolor = ["black","red","green","blue","purple","magenta","brown"]
	icolor = 0
	lcolor = len(pcolor)
	
	for key in xdata:
		if 'xrf' not in locals(): xrf=xr[key]
		if 'yrf' not in locals(): yrf=yr[key]

#		if verbose >2: print(key, icolor)
		if xrf[0] > xr[key][0]: xrf[0] = xr[key][0]
		if xrf[1] < xr[key][1]: xrf[1] = xr[key][1]
		if yrf[0] > yr[key][0]: yrf[0] = yr[key][0]
		if yrf[1] < yr[key][1]: yrf[1] = yr[key][1]

		if color[key] == None:
			color[key] = pcolor[icolor]
			icolor = (icolor+1) % lcolor

#		print(key, len(xdata[key]), xr[key], yr[key], 
#				title[key], marker[key], linestyle[key], color[key])

	if verbose >1: print("range:",xrf, yrf)

	def show(ion=True):
		if ion: plt.ion()

		for key in xdata:
#			if verbose >2: print(key, color[key], title[key])
			x=xdata[key]
			y=ydata[key]

			if xexpr != None: x=eval(xexpr)
			if yexpr != None: y=eval(yexpr)

			plt.plot(x,y,
					color=color[key], label=title[key],
					marker=marker[key], linestyle=linestyle[key])

		plt.legend(loc='best', labelcolor='linecolor', 
				frameon=False, 
				ncol=1)

		wrap(plt, xrf, yrf, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				grid=grid, 
				display=display, ion=ion)

	show(ion=False)
	if hold: embed()

	return plt

def rplot1d(xdata, ydata, xr, yr, title, marker, linestyle, color, 
		xlabel=None, ylabel=None, outfile=None, verbose=1,
		xscale='linear', yscale='linear',
		xexpr=None, yexpr=None, grid=True,
		display=True, ion=False, hold=False):
	"""Reference Plot 1-D from input table
	"""

	pcolor = ["black","red","green","blue","purple","magenta","brown"]
	icolor = 0
	lcolor = len(pcolor)
	
	keys = xdata.keys()
	ref = list(keys)[0]

	xref=xdata.pop(ref)
	yref=ydata.pop(ref)
	xr=xr[ref]
	yr=yr[ref]

	for key in xdata:
		if color[key] == None:
			color[key] = pcolor[icolor]
			icolor = (icolor+1) % lcolor

	def show(ion=True):

		nonlocal xref, yref

		if ion: plt.ion()

		for key in xdata:
#			if verbose >2: print(key, color[key], title[key])
			x=xdata[key]
			y=ydata[key]

			if xexpr != None: x=eval(xexpr)
			if yexpr != None: y=eval(yexpr)

			plt.plot(x,y,
					color=color[key], label=title[key],
					marker=marker[key], linestyle=linestyle[key])

		plt.legend(loc='best', labelcolor='linecolor', 
				frameon=False, 
				ncol=1)

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, 
				grid=grid, 
				display=display, ion=ion)

	show(ion=False)
	if hold: embed()

	return plt

