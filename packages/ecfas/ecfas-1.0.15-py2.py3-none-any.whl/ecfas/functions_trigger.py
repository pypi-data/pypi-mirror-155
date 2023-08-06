#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:57:15 2022

@author: mirazoki
"""
import glob
import os

from scipy.spatial import cKDTree as KDTree

import cartopy.crs as ccrs
import cartopy.feature as feat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr


def read_thresholds(hindir, vart):
    lfiles = glob.glob(os.path.join(hindir, '*%s.csv' % vart))
    pdlst = []
    for fid in lfiles:
        thrd = pd.read_csv(fid, header=0)
        pdlst.append(thrd)
    pdthr = pd.concat(pdlst)
    pdthr = pdthr.set_index(np.arange(len(pdthr)))
    return pdthr

    
def map2way(outdir, bdaylst, fcdir, hindir, vart='RL1', vard='p97', reglist=['NWS', 'IBI', 'MED', 'BAL', 'BS', 'ARC']):
    # remember to assign a threshold dummy (e.g. nan or -999?check with Sylvain) for those too far (e.g. buoys, TG)
    # keep an id count across regions not to repeat.we could keep the org name though
    
    # first do the mapping
    pdthr = read_thresholds(hindir, vart)
    corg = np.column_stack((pdthr['lon'].values, pdthr['lat'].values))  # either this, or I need to extrapolate the data first...
    kdorg = KDTree(corg)  
    
    pdlsttar = []
    for reg in reglist:
        # take one example file
        fex = glob.glob(os.path.join(fcdir, reg, 'timeseries', '*b%s*.nc' % bdaylst[reg]))[0]
        datatar = xr.open_dataset(fex)
        pdlsttar.append(datatar['stnames'].to_dataframe())
    pdtar = pd.concat(pdlsttar).drop(columns=['stnames'])
    iscoast = np.array(['station_coast' in str(stn) for stn in pdtar.index])
    
    kdist, indx = kdorg.query(np.column_stack((pdtar['lon'].values, pdtar['lat'].values)))
    
    pdtar['lon_map'] = pdthr.iloc[indx]['lon'].values
    pdtar['lat_map'] = pdthr.iloc[indx]['lat'].values
    pdtar['map_id'] = pdthr.index[indx]
    pdtar['thr1'] = pdthr.iloc[indx][vart].values
    
    pdfc = pdtar.iloc[iscoast]
    pdfc['stnames'] = [stname.decode("utf-8").lstrip() for stname in pdfc.index]
    pdfc = pdfc.set_index('stnames')
    pdfc['dist'] = kdist[iscoast]
    fname1 = os.path.join(outdir, 'hind2fc.csv')
    pdfc.to_csv(fname1)  # mapping file limited to coastal points
    
    # inverse mapping
    cfc = np.column_stack((pdfc['lon'].values, pdfc['lat'].values))  # either this, or I need to extrapolate the data first...
    kdfc = KDTree(cfc)  
    kdist, indx = kdfc.query(np.column_stack((pdthr['lon'].values, pdthr['lat'].values)))  # by hindcast index
    pdhin = pdthr.copy()
    pdhin['lon_map'] = pdfc['lon'].values[indx]
    pdhin['lat_map'] = pdfc['lat'].values[indx]
    pdhin['map_id'] = pdfc.index[indx]
    pdhin['dist'] = kdist
    pdhin['thr1'] = pdhin[vart].copy()
    try:
        pdhin['thr2'] = pdhin[vard].copy()
        pdhin = pdhin.drop(columns=[vart, vard])
    except KeyError:
        pdhin = pdhin.drop(columns=[vart])
    fname2 = os.path.join(outdir, 'fc2hind.csv')
    pdhin.to_csv(fname2)  # mapping file limited to coastal points
    return pdfc, pdhin


def trigger(outdir, ncdata, mapd, maxdist=0):
    wl = ncdata['zos'] + ncdata['Vsetup'].fillna(0)
    wl['stations'] = [stname.decode("utf-8").lstrip() for stname in wl.isel(time=0)['stations'].values]
    
    # reduce mapd to this region
    comst = mapd.set_index('map_id').index.intersection(wl['stations'])
    mapdreg = mapd[mapd['map_id'].isin(comst)]
    
    # initialize
    ffirst = np.full(mapdreg.index.shape, -9999)
    flag = np.full(mapdreg.index.shape, 0, dtype=bool)
    fhours = np.full(mapdreg.index.shape, -9999)
    
    wlhin = wl.sel(stations=mapdreg['map_id'].values)
    if 'thr1' in mapdreg.columns:
        wlhin['thr1'] = xr.DataArray(data=np.tile(mapdreg['thr1'].values, (wlhin.shape[1], 1)).T,
                                           coords=wlhin.coords,
                                           dims=wlhin.dims,
                                           attrs={'units':'m'})
        flag = np.any(wlhin.values > wlhin['thr1'].values, axis=1)
        for idx in np.where(flag)[0]:
            ffirst[idx] = wlhin.isel(stations=idx).values[np.where((wlhin.values > wlhin['thr1'].values)[idx,:])[0][0]]
    if 'thr2' in mapdreg.columns:
        wlhin['thr2'] = xr.DataArray(data=np.tile(mapdreg['thr2'].values, (wlhin.shape[1], 1)).T,
                                           coords=wlhin.coords,
                                           dims=wlhin.dims,
                                           attrs={'units':'m'})
        fhours = np.sum(wlhin.values > wlhin['thr2'].values, axis=1)  # THIS SHOULD BE CALCULATED WITH SECOND THRS
    maxwl = np.nanmax(wlhin.values, axis=1)
    maxwlt = wlhin['time'].isel(time=np.nanargmax(wlhin.values, axis=1)).values

    trgdat = mapdreg.copy()
    trgdat['flag'] = flag
    trgdat['fhours'] = fhours
    trgdat['maxwl'] = maxwl
    trgdat['maxwlt'] = maxwlt
    trgdat['ffirst'] = ffirst
    
    # turn flag off for those too far
    toofar = trgdat.index[trgdat['dist'] > maxdist]
    trgdat.loc[toofar, 'flag'] = False

    fname = os.path.join(outdir, 'trigg_info.csv')
    trgdat.to_csv(fname)  # m    
    
    return trgdat


def plot_trigger(ncst, stn, trd, outname):
    fig = plt.figure()
    plt.plot(ncst['time'], ncst['zos'] + ncst['Vsetup'])
    plt.axhline(y=trd['thr1'], color='cyan', linestyle='--', label='thr1')
    plt.title('%s lon:%.2f lat:%.2f ' % (stn, trd['lon'], trd['lat']))
    fig.savefig(outname, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plot_activated(trgdat, outnamept, bbox=None):
    # org thresholds
    thorg = read_thresholds(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thresholds'), 'RL1')
    trac = trgdat.iloc[np.where(trgdat['flag'])[0]]
    trac = trac.replace(-9999, np.nan)
    fig = plt.figure()
    ax = plt.gca(projection=ccrs.PlateCarree())
    ax.add_feature(feat.LAND.with_scale('10m'), facecolor='gray', zorder=0, alpha=1)
    if bbox is not None:
        ax.set_extent(bbox, ccrs.PlateCarree()) 
    im = ax.scatter(thorg['lon'], thorg['lat'], s=20, c=thorg['RL1'], marker='o', transform=ccrs.PlateCarree(), vmin=1, vmax=5, cmap='jet')
    plt.colorbar(im)
    ax.scatter(trac['lon'], trac['lat'], s=20, marker='^', c=trac['thr1'], edgecolors='black', transform=ccrs.PlateCarree(), vmin=1, vmax=5, cmap='jet')
    fig.savefig(outnamept, dpi=300, bbox_inches='tight')
    plt.close(fig)   
    
    for item in ['fhours', 'maxwl', 'maxwlt', 'ffirst']:
        fig = plt.figure()
        ax = plt.gca(projection=ccrs.PlateCarree())
        ax.add_feature(feat.LAND.with_scale('10m'), facecolor='gray', zorder=0, alpha=1)
        if bbox is not None:
            ax.set_extent(bbox, ccrs.PlateCarree()) 
        im = ax.scatter(trac['lon'], trac['lat'], s=20, marker='^', c=trac[item], edgecolors='black', transform=ccrs.PlateCarree(), cmap='jet')
        plt.colorbar(im)
        fig.savefig(outnamept.replace('.jpg', '_%s.jpg' % item), dpi=300, bbox_inches='tight')
        plt.close(fig)  
