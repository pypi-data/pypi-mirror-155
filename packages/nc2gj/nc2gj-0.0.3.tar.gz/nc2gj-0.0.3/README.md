## Introduction
Conversion of the ecfas nc coastal TWL time-series to geojson format, with the addition of the trigger threshold for coastal flood warning. It therefore requires that the ecfas workflow and trigger have been run first such. If this is not the case, a dummy threshold is introduced (-9999).

## Conda dependencies
geopandas==0.10.2

## usage
Specify the following mandatory arguments:
- -o <outputdir>: Output directory where the daily regional netcdf time-series forecasts are saved.

Optional arguments:
- -r <region> : Region, matching the 6 Copernicus Marine Service regional domains. Defaults to all ['NWS','IBI','MED','BAL','BS','ARC']
- -t <%Y%m%d_%H%M%S>: Bulleting date for the forecast data. Default: Forecast update time of execution day

Example usage: `nc2geojson -o <outputdir> [-r <region>] -t [<%Y%m%d_%H%M%S>]`

Output: geojson files (*.geojson), written out to the same directory as the netcdf folder (<outputdir> argument to command). The name of the file is kept the same as the the original netcdf filenames, just the extension changes.
