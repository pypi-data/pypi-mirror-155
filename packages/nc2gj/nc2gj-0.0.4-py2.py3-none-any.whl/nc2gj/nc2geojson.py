#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:40:53 2022

@author: mirazoki
"""
import argparse
import datetime
import glob
import os

from shapely.geometry import Point

import geopandas as gpd
import nc2gj.cmems_datasets as dsets
import numpy as np
import pandas as pd
import xarray as xr


def nc2geojson(ncfile, mapd=None, maxdist=0, varout=['zos', 'Vsetup']):
    data = xr.open_dataset(ncfile)
    df = pd.DataFrame()
    df['id'] = [stname.decode("utf-8").lstrip() for stname in data.isel(time=0)['stations'].values]
    timearr = (data.time.values - np.datetime64('1970-01-01')).astype('datetime64[ms]').astype('int')
    timeblock = np.repeat(np.array(timearr).reshape((np.array(timearr).size, 1)), len(df), axis=1).T.tolist()
    df['timestr'] = timeblock
    df = df.set_index('id')
    df['threshold'] = -9999
    if mapd is not None:
    # THRESHOLD assignment

        comst = df.index.intersection(mapd.index)
        df.loc[comst, 'threshold'] = mapd.loc[comst]['thr1'].values
        df['threshold'] = [float('%.5f' % df.loc[ii]['threshold']) for ii in df.index]

    dfvar = data[varout[0]].isel(time=0).to_dataframe()
    df['geometry'] = [Point(float('%.5f' % dfvar.loc[ii]['lon']), float('%.5f' % dfvar.loc[ii]['lat'])) for ii in dfvar.index]

    for vari in varout:
        listvar = np.asarray(np.char.mod("%.5f", data[vari].values), dtype=float).tolist()
        df[vari] = listvar
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    jdat = gdf.to_json()
    odir = os.path.join(os.path.dirname(ncfile), 'geojson')
    if not os.path.exists(odir):
        os.mkdir(odir)
    jsonn = os.path.join(odir, os.path.basename(ncfile).replace('.nc', '.json'))
    fid = open(jsonn, 'w+')  # change name to match that of input netcdf
    fid.write(jdat)
    fid.close()


def main():
    parser = argparse.ArgumentParser("nc2geojson")
    parser.add_argument('-r', '--region', metavar='<region>', required=False, help='Region of interest, one of ARC, BAL, BS. IBI, MED, NWS, GLO. Defaults to all')
    parser.add_argument('-o', '--outputs', metavar='<output_dir>', required=True, help='Absolute path to output data to be checked')
    parser.add_argument('-t', '--t0', metavar='<YYmmdd_HHMMSS>', required=False, help='Start time t0 in the format YYmmdd_HHMMSS')

    args = parser.parse_args()
    maxd = 0.1
    reglist = ['NWS', 'IBI', 'MED', 'BAL', 'BS', 'ARC']
    if args.region is not None:
        reglist = [args.region]
    for reg in reglist:
        if args.t0 == None:
            uptime = dsets.datasets_hydro[reg]["uptime"]
            now = datetime.datetime.now()
            bday = datetime.datetime(now.year, now.month, now.day, int(uptime), int((uptime * 60) % 60), int((uptime * 3600) % 3600))
        else:
            bday = datetime.datetime.strptime(args.t0, "%Y%m%d_%H%M%S")
        
        mapfcf=os.path.join(args.outputs,'trigger','hind2fc.csv')
        if os.path.exists(mapfcf):
           mapfc=pd.read_csv(mapfcf,header=0)
        else:
           mapfc=None
        # write out geojson
        # load data
        listf = glob.glob(os.path.join(args.outputs, reg, 'timeseries', '*b%s*.nc' % (bday.strftime('%Y%m%d%H%M%S'))))
        listf.sort()
        for filei in listf:
            nc2geojson(filei, mapd=mapfc, maxdist=maxd)


if __name__ == "__main__":
    main()
