#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 17:05:48 2022

@author: mirazoki
"""

import argparse
import datetime
import glob
import os
import sys

import ecfas.cmems_datasets as dsets
import ecfas.functions_trigger as trigg
import ecfas.utils as utils
import pandas as pd
import xarray as xr
import numpy as np


def execute_workflow(args):
    # Read config file
    try:
        config = utils.read_config(args.config)
    except Exception as e:
        print('Failed to read config file: ' + str(e))
        sys.exit(1)   
        
    fcdir = config['outdir']
    hindir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thresholds')
    outdir = os.path.join(fcdir, 'trigger')
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    #user options(fixed now)=============================================================
    fclim = 3  # days
    maxd = 0.1
    vart = 'TriggeringThreshold'
    vard = 'DurationThreshold'
    reglist = ['NWS', 'IBI', 'MED', 'BAL', 'BS', 'ARC']
    
    # ===========================================================================    
    bdaylst = dict()
    for reg in reglist:
        if args.t0 == None:
            uptime = dsets.datasets_hydro[reg]["uptime"]
            now = datetime.datetime.now()
            bdaylst[reg] = datetime.datetime(now.year, now.month, now.day, int(uptime), int((uptime * 60) % 60), int((uptime * 3600) % 3600)).strftime('%Y%m%d%H%M%S')
        else:
            bdaylst[reg] = datetime.datetime.strptime(args.t0, "%Y%m%d_%H%M%S").strftime('%Y%m%d%H%M%S')
            
    # mapping
    _, maphin = trigg.map2way(outdir, bdaylst, fcdir, hindir, vart=vart, vard=vard)
    
    # trigger
    trgl = []
    for reg in reglist:
        listf=glob.glob(os.path.join(fcdir, reg, 'timeseries', '*b%s*.nc' % bdaylst[reg]))
        if len(listf)>0:
            listf.sort()
            ncdat = xr.open_mfdataset(listf)
            # clip to desired length fcst
            tini = datetime.datetime.strptime(bdaylst[reg], "%Y%m%d%H%M%S")
            tend = tini + datetime.timedelta(days=fclim)
            ncdat_fc = ncdat.sel(time=slice(tini, tend))
            trgdat = trigg.trigger(outdir, ncdat_fc, maphin, maxdist=maxd)
            trgl.append(trgdat)
            
            if bool(args.plot):
                ncdat['stations']=[stname.decode("utf-8").lstrip() for stname in ncdat.isel(time=0)['stations'].values]
                for idx in trgdat.iloc[np.where(trgdat['flag'])[0]].index[::10]:
                    stn=trgdat.loc[idx]['map_id']
                    ncst=ncdat.sel(stations=stn)
                    outname=os.path.join(outdir,stn+ '_' +listf[0].split('_')[-3] + '.jpg')
                    trgi=trgdat.loc[idx]
                    trigg.plot_trigger(ncst,stn,trgi,outname)
    
                #sanity check
                bboxreg=[dsets.datasets_hydro[reg]['lon_min'],dsets.datasets_hydro[reg]['lon_max'],dsets.datasets_hydro[reg]['lat_min'],dsets.datasets_hydro[reg]['lat_max']]
                outnamept=os.path.join(outdir,reg+ '_' +listf[0].split('_')[-3] + '.jpg')
                trigg.plot_activated(trgdat,outnamept,bbox=bboxreg)
    trgall = pd.concat(trgl)
    fname = os.path.join(outdir, 'trigg_info.csv')
    trgall.to_csv(fname)  # m   

    
def main():
    #0. READ ARGS AND CONFIG ==========================================================================================================
    parser = argparse.ArgumentParser("op_trigger")
    parser.add_argument('-c', '--config', metavar='<config_file>', default='ecfas.cfg', required=True, help='Absolute path to config file')
    parser.add_argument('-t', '--t0', metavar='<YYmmdd_HHMMSS>', default=None, help='Start time t0 in the format YYmmdd_HHMMSS')
    parser.add_argument('-p', '--plot', default=0, help='Switch to plot triggered coastal points')
    parser.add_argument('--debug', action='store_true', help='Debug mode')

    execute_workflow(parser.parse_args())


if __name__ == "__main__":
    main()         
