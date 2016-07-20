========
Usage
========

To use Hydrogen (HI) Data Emulator in a project execute the following on the command line::

	$ hide --strategy-start=2016-03-21-00:00:00 --strategy-end=2016-03-21-23:59:00 --verbose=True hide.config.bleien7m
	
This will simulate one day of time-ordered-data from the Bleien 7m radio telescope.

To visualize 15 minutes of the generated data run this::

	import matplotlib.pyplot as plt
	import matplotlib
	import h5py
	
	with h5py.File("./2016/03/21/TEST_MP_PXX_20160321_000000.h5", "r") as fp:
	    tod = fp["P/Phase1"].value
	    time = fp["TIME"].value
	    
	plt.imshow(tod, aspect="auto", 
	           extent=(time[0], time[-1],990, 1260), 
	           cmap="gist_earth", norm=matplotlib.colors.LogNorm())
	plt.colorbar()
    
    
.. image:: tod.png
   :alt: simulated Bleien 7m dish data
	