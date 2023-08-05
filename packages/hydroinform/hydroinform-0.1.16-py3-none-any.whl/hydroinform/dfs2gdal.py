# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:35:40 2020

@author: jacob
"""

from osgeo import gdal, osr
import numpy as np
from hydroinform import DFS

def save_dfs_as_tif(dfs, items, time_steps, tiffilename, layer=0):
    """
    Saves items and timesteps from .dfs2- or .dfs3-files as Tiff. Only save the items and time_steps in the lists. 
    Items and time_steps should be given as zero-based integer list or just integer numbers
    Multiple time steps or items are saved in bands
    """

    if isinstance(items, int):
        items = [items]
    if isinstance(time_steps, int):
        time_steps = [time_steps]

    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(tiffilename,dfs.number_of_columns, dfs.number_of_rows, len(items)*len(time_steps) ,gdal.GDT_Float32)
    spatial_reference = osr.SpatialReference()
    spatial_reference.ImportFromEPSG(25832)
    ds.SetProjection(spatial_reference.ExportToWkt())
    ds.SetGeoTransform((dfs.x_origin, dfs.dx, 0, dfs.y_origin, 0, dfs.dy))
    
    band_count=1
    for t in time_steps:
        for i in items:    
            rb = ds.GetRasterBand(band_count)
            if isinstance(dfs, DFS.DFS3):
                rb.WriteArray(dfs.get_data(t,i+1)[layer])
            else:
                rb.WriteArray(dfs.get_data(t,i+1))
            rb.SetNoDataValue(dfs.delete_value) 
            rb.SetDescription(dfs.items[i].name + '.Time: '+ str(dfs.time_steps[t]))
            band_count+=1
    ds=None
 
