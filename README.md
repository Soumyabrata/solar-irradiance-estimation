# Estimation of solar irradiance using ground-based whole sky imagers 

With the spirit of reproducible research, this repository contains all the codes required to produce the results in the manuscript: S. Dev, F. M. Savoy, Y. H. Lee, S. Winkler, Estimation of solar irradiance using ground-based whole sky imagers, *Proc. IEEE International Geoscience and Remote Sensing Symposium (IGARSS)*, 2016. 

Please cite the above paper if you intend to use whole/part of the code. This code is only for academic and research purposes.

## Manuscript
The author version of this manuscript is `manuscript.PDF`. 

## Code Organization
All codes are written in python.

### Helper Scripts
* `CalculateLuminance.py` Calculates the luminance of the sky/cloud image, based on the sun location in the image and crop dimension.
* `cmask.py` Generates the mask of the sky/cloud image with a given center position and radius.
* `findCorrelation.py` Calculates the correlation value for various crop dimensions.
* `findSelectedFiles.py` Selects a set of images for luminance computation. In case of High Dynamic Range (HDR) mode, it selects the lowest exposure image; otherwise it selects the normal Low Dynamic Range (LDR) image.
* `import_WS.py` Imports the weather station data with its various meteorological sensor measurements.
* `import_WS_CI.py` Imports the weather station data, and also calculates the clearness index value for the location of our sky camera.
* `nearest.py` Finds the nearest timestamp in a presorted list of timestamps.
* `normalize_array.py` Normalizes a given numpy array.
* `SG_model.py` Calculates the clear-sky irradiance value for Singapore.
* `sun_positions_day_files.py` Computes the sun-position in a set of sky/cloud images.

### Weather Data
The folder `./weatherData` contains the weather data for the month of December 2015.

### Pre-computed Files
In this repository, we also share all the pre-computed luminance files that is necessary to reproduce the results.

### Generated Files
The ouput files are kept in the folder `./outputFiles`.

### Reproducibility 
The program `./main.ipynb` is the main script, that reproduces all the results. It uses different helper scripts stored in the folder `./helperScripts`. It also reproduces the figures in this associated paper.
