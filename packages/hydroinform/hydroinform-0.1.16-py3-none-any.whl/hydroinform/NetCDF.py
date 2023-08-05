# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 09:33:03 2020

@author: jacob
"""
from netCDF4 import Dataset, date2num
import time
import os
from datetime import datetime
from hydroinform.DFS import DFSBase, DFS0, DFS2, DFS3
from hydroinform import Mike_river


def save_as_NetCDF(dfsfilename, NetCDFfilename=''):
    """
    Saves the DFS-file in NetCDF-format. Works for .dfs0, .dfs2, .dfs3, .res1d and res11.
    If no NetCDFfilename is given it will use the dfs-filename and change the extension
    """
    t0 = time.time()    

    if NetCDFfilename=='':
        pre, ext = os.path.splitext(dfsfilename)
        NetCDFfilename =pre + '.nc'

    #Try to create a river
    river=Mike_river.River_setup.from_file(dfsfilename)
    if river is not None:
        print('Read finished: ', time.time() - t0)
        save_river_as_NetCDF(river, NetCDFfilename)
    else:
        morg = DFSBase.open_file(dfsfilename)
        save_dfs_as_NetCDF(morg, range(0,len(morg.items)),range(0,len(morg.time_steps)), NetCDFfilename)


def save_river_as_NetCDF(river, NetCDFfilename):
    """
    Saves a River_setup as NetCDF. 
    """
    t0 = time.time()    
    
    rootgrp = Dataset(NetCDFfilename, "w", format="NETCDF4")
    rootgrp.createDimension("time", river.res.number_of_time_steps)
    times = rootgrp.createVariable("time","f8",("time",))
    times.units = "hours since 0001-01-01 00:00:00.0"
    times.calendar = "gregorian"
    items=[]
    for r in river.reaches:
        for p in r.grid_points_q:
            items.append(rootgrp.createVariable(p.name, 'f4', ('time'),chunksizes=([river.res.number_of_time_steps]), fill_value=river.res.delete_value, zlib=True, complevel=9))
            items[-1].units="m3/s"
            items[-1].x =p.x
            items[-1].y =p.y
            items[-1].Chainage =p.chainage
            items[-1].BranchName =r.name
            items[-1].TopoID =r.topo_id
    i = 0
    for r in river.reaches:
        for p in r.grid_points_q:
            items[i][:]=river.get_values_Q(p)
            i+=1
    times[:] = date2num(river.res.time_steps,units=times.units,calendar=times.calendar)

    print('write finished: ', time.time() - t0)
    
    rootgrp.close()


def save_dfs_as_NetCDF(dfs, items, time_steps, NetCDFfilename):
    """
    Saves a .dfs-file as NetCDF. Only save the items and time_steps in the lists. 
    Items and time_steps should be given as zero-based integer list 
    """
    t0 = time.time()
    if isinstance(dfs,DFS0):
        dfs.get_values(1)
        print('Read finished: ', time.time() - t0)

    rootgrp = Dataset(NetCDFfilename, "w", format="NETCDF4")
    rootgrp.createDimension("time", len(time_steps))
    times = rootgrp.createVariable("time","f8",("time",))
    times.units = "hours since 0001-01-01 00:00:00.0"
    times.calendar = "gregorian"
    
    if isinstance(dfs,DFS3) or isinstance(dfs,DFS2):
        rootgrp.createDimension("X", dfs.number_of_columns)
        rootgrp.createDimension("Y", dfs.number_of_rows)
        xs = rootgrp.createVariable("X","f4",("X",))
        xs.units='m'
        xs[:]=[dfs.get_x_center(i) for i in range(0,dfs.number_of_columns)]
        ys = rootgrp.createVariable("Y","f4",("Y",))
        ys.units='m'
        ys[:]=[dfs.get_y_center(i) for i in range(0,dfs.number_of_rows)]

        if isinstance(dfs, DFS3):
            rootgrp.createDimension("layer", dfs.number_of_layers)    
            layers = rootgrp.createVariable("layer","i4",("layer",))
            layers[:]=range(0, dfs.number_of_layers)
    
    netcdf_items=[]
    
    for i in items:
        if isinstance(dfs,DFS2):
            netcdf_items.append(rootgrp.createVariable(dfs.items[i].name, 'f4', ('time','Y','X'), chunksizes=(1,dfs.number_of_rows,dfs.number_of_columns),fill_value=dfs.delete_value, zlib=True, complevel=1))
        elif isinstance(dfs,DFS3):
            netcdf_items.append(rootgrp.createVariable(dfs.items[i].name, 'f4', ('time', 'layer','Y','X'), chunksizes=(1,1,dfs.number_of_rows,dfs.number_of_columns),fill_value=dfs.delete_value, zlib=True, complevel=1))
        elif isinstance(dfs,DFS0):
            netcdf_items.append(rootgrp.createVariable(dfs.items[i].name, 'f4', ('time'),chunksizes=([dfs.number_of_time_steps]), fill_value=dfs.delete_value, zlib=True, complevel=9))
        netcdf_items[-1].units=str(dfs.items[i].eum_unit)
    
    netcdf_i=0
    if isinstance(dfs,DFS0):
        for i in items:
            netcdf_items[netcdf_i][:]=dfs.get_values(i+1)
            netcdf_i+=1
    else:
        netcdf_t=0
        for t in time_steps:
            netcdf_i=0
            for i in items:
                data =dfs.get_data(t,i+1)
                if isinstance(dfs,DFS2):
                    netcdf_items[netcdf_i][netcdf_t,:,:]=data
                elif isinstance(dfs,DFS3):
                    netcdf_items[netcdf_i][netcdf_t,:,:,:]=data
                netcdf_i+=1
            netcdf_t+=1
    
    times[:] = date2num([dfs.get_time_of_timestep(i) for i in time_steps],units=times.units,calendar=times.calendar)

    print('write finished: ', time.time() - t0)
    
    rootgrp.close()





