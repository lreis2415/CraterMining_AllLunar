# coding=utf-8

import shapefile
import numpy as np
import os
from osgeo import ogr, osr, gdal
import math
from pygeoc.raster import RasterUtilClass
import csv
import CoordsTrans



def getscrowcol(NSsrs_pnt, NSsrs2sc_ct, sc_trans):
    sc_pnt = CoordsTrans.proj2proj(NSsrs2sc_ct, NSsrs_pnt[0], NSsrs_pnt[1])
    sc_pxl = CoordsTrans.geo2imagexy(sc_trans, sc_pnt[0], sc_pnt[1])
    return sc_pxl

def getpxllength(sc_pxl, sc2NSsrs_ct, sc_trans, rownum, colnum):
    sc_pxl_coord = CoordsTrans.imagexy2geo(sc_trans, sc_pxl[0], sc_pxl[1])
    NSsrs_pxl_coord = CoordsTrans.proj2proj(sc2NSsrs_ct, sc_pxl_coord[0], sc_pxl_coord[1])
    if sc_pxl[0] == rownum - 1:
        sc_pxlnxt_row = sc_pxl[0] - 1
    else:
        sc_pxlnxt_row = sc_pxl[0] + 1
    if sc_pxl[1] == colnum - 1:
        sc_pxlnxt_col = sc_pxl[1] - 1
    else:
        sc_pxlnxt_col = sc_pxl[1] + 1
    sc_pxlnxt_coord = CoordsTrans.imagexy2geo(sc_trans, sc_pxlnxt_row, sc_pxlnxt_col)
    NSsrs_pxlnxt_coord = CoordsTrans.proj2proj(sc2NSsrs_ct, sc_pxlnxt_coord[0], sc_pxlnxt_coord[1])
    x_length = NSsrs_pxl_coord[1] - NSsrs_pxlnxt_coord[1]
    y_length = NSsrs_pxl_coord[0] - NSsrs_pxlnxt_coord[0]
    NSsrs_pxl_length = math.sqrt(x_length*x_length + y_length*y_length)
    return NSsrs_pxl_length

def get_starts_ends(crcs_amount, crcs_points):
    crcs_starts = []
    crcs_ends = []
    for i in range(crcs_amount):
        i_crcs_pnts_amount = len(crcs_points[i])
        i_crcs_pnts_gap = float(i_crcs_pnts_amount/12.0)
        i_crcs_ends = []
        for j in range(12): 
            j_end_order = int(j*i_crcs_pnts_gap)
            i_crcs_j_end = crcs_points[i][j_end_order]
            i_crcs_ends.append(i_crcs_j_end)
        x_sum = 0
        y_sum = 0
        for j in range(12):
            x_sum = x_sum + i_crcs_ends[j][0]
            y_sum = y_sum + i_crcs_ends[j][1]
        i_crcs_start = (float(x_sum/12.0), float(y_sum/12.0))
        crcs_ends.append(i_crcs_ends)
        crcs_starts.append(i_crcs_start)
    return crcs_starts, crcs_ends

def get_starts_ends_lengths(crcs_amount, crcs_starts, crcs_ends, NSsrs2sc_ct, sc2NSsrs_ct, sc_trans, Rst_nRows, Rst_nCols):
    crcs_starts_length = []
    crcs_ends_length = []
    for i in range(crcs_amount):
        Nsrs_start_pnt_coord = crcs_starts[i]
        sc_start_pxl = getscrowcol(Nsrs_start_pnt_coord, NSsrs2sc_ct, sc_trans)
        sc_start_pxl_length = getpxllength(sc_start_pxl, sc2NSsrs_ct, sc_trans, Rst_nRows, Rst_nCols)
        crcs_starts_length.append(sc_start_pxl_length)
        ends_length = []
        for j in range(12):
            Nsrs_end_pnt_coord = crcs_ends[i][j]
            sc_end_pxl = getscrowcol(Nsrs_end_pnt_coord, NSsrs2sc_ct, sc_trans)
            sc_end_pxl_length = getpxllength(sc_end_pxl, sc2NSsrs_ct, sc_trans, Rst_nRows, Rst_nCols)
            ends_length.append(sc_end_pxl_length)
        crcs_ends_length.append(ends_length)
    return crcs_starts_length, crcs_ends_length

def get_profiles_pxls_dem(crcs_amount, crcs_starts, crcs_starts_length, crcs_ends, crcs_ends_length, NSsrs2sc_ct, sc_trans, DEM_data):
    crcs_profiles_pxls_dem = [] 
    for i in range(crcs_amount):
        i_crc_start_pnt = crcs_starts[i]
        i_crc_start_length = crcs_starts_length[i]
        i_crc_profiles_pxls_dem = [] 
        for j in range(12):
            i_crc_j_profile_pxls = [] 
            i_crc_j_profile_pxls_dem = [] 
            i_crc_j_profile_pxls_dem.append(i)
            i_crc_j_profile_pxls_dem.append(j)
            i_crc_j_end_pnt = crcs_ends[i][j]
            i_crc_j_end_length = crcs_ends_length[i][j]
            if i_crc_start_length <= i_crc_j_end_length:
                pxl_length = i_crc_start_length
            else:
                pxl_length = i_crc_j_end_length
            i_crc_j_pfl_length = math.sqrt((i_crc_j_end_pnt[0]-i_crc_start_pnt[0])**2
                                           +(i_crc_j_end_pnt[1]-i_crc_start_pnt[1])**2)
            pxls_num = int(i_crc_j_pfl_length/pxl_length)+1
            if j in [0, 6]:
                if j == 0:
                    pxl_length = pxl_length
                else:
                    pxl_length = -pxl_length
                for n in range(pxls_num):
                    nxt_pxl_pnt = [i_crc_start_pnt[0], i_crc_start_pnt[1]+n*pxl_length]
                    nxt_pxl = getscrowcol(nxt_pxl_pnt, NSsrs2sc_ct, sc_trans)
                    if nxt_pxl not in i_crc_j_profile_pxls:
                        i_crc_j_profile_pxls.append(nxt_pxl)
                        nxt_pxl_dem = DEM_data[nxt_pxl[0]][nxt_pxl[1]]
                        i_crc_j_profile_pxls_dem.append(nxt_pxl_dem)
                i_crc_profiles_pxls_dem.append(i_crc_j_profile_pxls_dem)
            elif j in [3, 9]:
                if j == 3:
                    pxl_length = pxl_length
                else:
                    pxl_length = -pxl_length
                for n in range(pxls_num):
                    nxt_pxl_pnt = [i_crc_start_pnt[0]+n*pxl_length, i_crc_start_pnt[1]]
                    nxt_pxl = getscrowcol(nxt_pxl_pnt, NSsrs2sc_ct, sc_trans)
                    if nxt_pxl not in i_crc_j_profile_pxls:
                        i_crc_j_profile_pxls.append(nxt_pxl)
                        nxt_pxl_dem = DEM_data[nxt_pxl[0]][nxt_pxl[1]]
                        i_crc_j_profile_pxls_dem.append(nxt_pxl_dem)
                i_crc_profiles_pxls_dem.append(i_crc_j_profile_pxls_dem)
            else:
                # Calculate passing pixels.
                a = np.array([[i_crc_start_pnt[0], 1], [i_crc_j_end_pnt[0], 1]])
                b = np.array([i_crc_start_pnt[1], i_crc_j_end_pnt[1]])
                [k, h] = np.linalg.solve(a,b)
                # Split length into x add and y add.
                x_para = math.sqrt(1/(1+k**2))
                if j < 6:
                    pxl_length = pxl_length
                else:
                    pxl_length = -pxl_length
                x_add = x_para*pxl_length
                y_add = k*x_add
                for n in range(pxls_num):
                    nxt_pxl_pnt = [i_crc_start_pnt[0]+n*x_add, i_crc_start_pnt[1]+n*y_add]
                    nxt_pxl = getscrowcol(nxt_pxl_pnt, NSsrs2sc_ct, sc_trans)
                    if nxt_pxl not in i_crc_j_profile_pxls:
                        i_crc_j_profile_pxls.append(nxt_pxl)
                        nxt_pxl_dem = DEM_data[nxt_pxl[0]][nxt_pxl[1]]
                        i_crc_j_profile_pxls_dem.append(nxt_pxl_dem)
                i_crc_profiles_pxls_dem.append(i_crc_j_profile_pxls_dem)
        crcs_profiles_pxls_dem.append(i_crc_profiles_pxls_dem)
    return crcs_profiles_pxls_dem

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
crcs_shp_path =  parentparent_path + "\\03_Step6_Clusters2Objects\\crcs_shp\\"
crcs_prfs_dem_path = parent_path + "\\crcs_prfs_dem\\"
DEM_path = parentparent_path + "\\00_PreStep_BlocksDivision\\original_DEM\\"
Rst_path = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\allLunar_DBSCANclusters\\"

DEMFileName = DEM_path + "globalDEM.tif"
RstFileName = Rst_path + "All_Lunar_CratersCandidates_DBScan_sc.tif"

def norm_profile_csv(RstFileName, DEMFileName, crcs_shp_path, crcs_prfs_dem_path):
    Rst = gdal.Open(RstFileName)
    Rst_nRows = Rst.RasterYSize
    Rst_nCols = Rst.RasterXSize
    DEM = gdal.Open(DEMFileName)
    DEM_band = DEM.GetRasterBand(1)
    DEM_data = DEM_band.ReadAsArray()
    sc_prosrs, sc_geosrs = CoordsTrans.getSRSPair(Rst)
    sc_trans = Rst.GetGeoTransform()
    N_srs = osr.SpatialReference()
    N_srs.ImportFromWkt('PROJCS["Moon_North_Pole_Stereographic",GEOGCS["Moon 2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Stereographic"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",90],UNIT["Meter",1]]')
    Nsrs2sc_ct = osr.CoordinateTransformation(N_srs, sc_prosrs)
    sc2Nsrs_ct = osr.CoordinateTransformation(sc_prosrs, N_srs)
    S_srs = osr.SpatialReference()
    S_srs.ImportFromWkt('PROJCS["Moon_South_Pole_Stereographic",GEOGCS["Moon 2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Stereographic"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-90],UNIT["Meter",1]]')
    Ssrs2sc_ct = osr.CoordinateTransformation(S_srs, sc_prosrs)
    sc2Ssrs_ct = osr.CoordinateTransformation(sc_prosrs, S_srs)
    #
    for start_ID in range(0, 60000, 1000):
        CrcFileName =  crcs_shp_path + "Crcs_CrtCnds_" + str(start_ID+999) + ".shp"
        crcs = shapefile.Reader(CrcFileName)
        crcs_shapes = crcs.shapes()
        crcs_amount = len(crcs_shapes)
        crcs_points = []
        for i in range(crcs_amount):
            i_crc_points = crcs_shapes[i].points
            crcs_points.append(i_crc_points)
        crcs_starts, crcs_ends = get_starts_ends(crcs_amount, crcs_points)
        crcs_starts_length, crcs_ends_length = get_starts_ends_lengths(crcs_amount, crcs_starts, crcs_ends, Nsrs2sc_ct, sc2Nsrs_ct, sc_trans, Rst_nRows, Rst_nCols)
        crcs_profiles_pxls_dem = get_profiles_pxls_dem(crcs_amount, crcs_starts, crcs_starts_length, crcs_ends, crcs_ends_length, Nsrs2sc_ct, sc_trans, DEM_data)
        csv_header = ["crc_ID","prf_ID"]
        with open (crcs_prfs_dem_path + "Crcs_CrtCnds_" + str(start_ID+999) + "_prfs_dem.csv", "w", newline = '') as csv_data:
            write_csv = csv.writer(csv_data)
            write_csv.writerow(csv_header)
            for i in range(len(crcs_profiles_pxls_dem)):
                for j in range(len(crcs_profiles_pxls_dem[i])):
                    writerow = crcs_profiles_pxls_dem[i][j]
                    write_csv.writerow(writerow)
    #
    for start_ID in range(60000, 84000, 1000):
        CrcFileName =  crcs_shp_path + "Crcs_CrtCnds_" + str(start_ID+999) + ".shp"
        crcs = shapefile.Reader(CrcFileName)
        crcs_shapes = crcs.shapes()
        crcs_amount = len(crcs_shapes)
        crcs_points = []
        for i in range(crcs_amount):
            i_crc_points = crcs_shapes[i].points
            crcs_points.append(i_crc_points)
        crcs_starts, crcs_ends = get_starts_ends(crcs_amount, crcs_points)
        crcs_starts_length, crcs_ends_length = get_starts_ends_lengths(crcs_amount, crcs_starts, crcs_ends, Ssrs2sc_ct, sc2Ssrs_ct, sc_trans, Rst_nRows, Rst_nCols)
        crcs_profiles_pxls_dem = get_profiles_pxls_dem(crcs_amount, crcs_starts, crcs_starts_length, crcs_ends, crcs_ends_length, Ssrs2sc_ct, sc_trans, DEM_data)
        csv_header = ["crc_ID","prf_ID"]
        with open (crcs_prfs_dem_path + "Crcs_CrtCnds_" + str(start_ID+999) + "_prfs_dem.csv", "w", newline = '') as csv_data:
            write_csv = csv.writer(csv_data)
            write_csv.writerow(csv_header)
            for i in range(len(crcs_profiles_pxls_dem)):
                for j in range(len(crcs_profiles_pxls_dem[i])):
                    writerow = crcs_profiles_pxls_dem[i][j]
                    write_csv.writerow(writerow)
    #
    for start_ID in range(84000, 84001):
        CrcFileName =  crcs_shp_path + "Crcs_CrtCnds_84560.shp"
        crcs = shapefile.Reader(CrcFileName)
        crcs_shapes = crcs.shapes()
        crcs_amount = len(crcs_shapes)
        crcs_points = []
        for i in range(crcs_amount):
            i_crc_points = crcs_shapes[i].points
            crcs_points.append(i_crc_points)
        crcs_starts, crcs_ends = get_starts_ends(crcs_amount, crcs_points)
        crcs_starts_length, crcs_ends_length = get_starts_ends_lengths(crcs_amount, crcs_starts, crcs_ends, Ssrs2sc_ct, sc2Ssrs_ct, sc_trans, Rst_nRows, Rst_nCols)
        crcs_profiles_pxls_dem = get_profiles_pxls_dem(crcs_amount, crcs_starts, crcs_starts_length, crcs_ends, crcs_ends_length, Ssrs2sc_ct, sc_trans, DEM_data)
        csv_header = ["crc_ID","prf_ID"]
        with open (crcs_prfs_dem_path + "Crcs_CrtCnds_84560_prfs_dem.csv", "w", newline = '') as csv_data:
            write_csv = csv.writer(csv_data)
            write_csv.writerow(csv_header)
            for i in range(len(crcs_profiles_pxls_dem)):
                for j in range(len(crcs_profiles_pxls_dem[i])):
                    writerow = crcs_profiles_pxls_dem[i][j]
                    write_csv.writerow(writerow)
    
    # 
    NCrcFileName = crcs_shp_path + "Crcs_north_border_CrtCnds.shp"
    SCrcFileName = crcs_shp_path + "Crcs_south_border_CrtCnds.shp"
    Ncrcs = shapefile.Reader(NCrcFileName)
    Ncrcs_shapes = Ncrcs.shapes()
    Ncrcs_amount = len(Ncrcs_shapes)
    Ncrcs_points = []
    for i in range(Ncrcs_amount):
        i_Ncrc_points = Ncrcs_shapes[i].points
        Ncrcs_points.append(i_Ncrc_points)
    Scrcs = shapefile.Reader(SCrcFileName)
    Scrcs_shapes = Scrcs.shapes()
    Scrcs_amount = len(Scrcs_shapes)
    Scrcs_points = []
    for i in range(Scrcs_amount):
        i_Scrc_points = Scrcs_shapes[i].points
        Scrcs_points.append(i_Scrc_points)
    Ncrcs_starts, Ncrcs_ends = get_starts_ends(Ncrcs_amount, Ncrcs_points)
    Scrcs_starts, Scrcs_ends = get_starts_ends(Scrcs_amount, Scrcs_points)
    Ncrcs_starts_length, Ncrcs_ends_length = get_starts_ends_lengths(Ncrcs_amount, Ncrcs_starts, Ncrcs_ends, Nsrs2sc_ct, sc2Nsrs_ct, sc_trans, Rst_nRows, Rst_nCols)
    Scrcs_starts_length, Scrcs_ends_length = get_starts_ends_lengths(Scrcs_amount, Scrcs_starts, Scrcs_ends, Ssrs2sc_ct, sc2Ssrs_ct, sc_trans, Rst_nRows, Rst_nCols)
    Ncrcs_profiles_pxls_dem = get_profiles_pxls_dem(Ncrcs_amount, Ncrcs_starts, Ncrcs_starts_length, Ncrcs_ends, Ncrcs_ends_length, Nsrs2sc_ct, sc_trans, DEM_data)
    Scrcs_profiles_pxls_dem = get_profiles_pxls_dem(Scrcs_amount, Scrcs_starts, Scrcs_starts_length, Scrcs_ends, Scrcs_ends_length, Ssrs2sc_ct, sc_trans, DEM_data)
    #
    csv_header = ["crc_ID","prf_ID"]
    with open (crcs_prfs_dem_path+"Crcs_north_border_CrtCnds_prfs_dem.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(Ncrcs_profiles_pxls_dem)):
            for j in range(len(Ncrcs_profiles_pxls_dem[i])):
                writerow = Ncrcs_profiles_pxls_dem[i][j]
                write_csv.writerow(writerow)
    with open (crcs_prfs_dem_path+"Crcs_south_border_CrtCnds_prfs_dem.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(Scrcs_profiles_pxls_dem)):
            for j in range(len(Scrcs_profiles_pxls_dem[i])):
                writerow = Scrcs_profiles_pxls_dem[i][j]
                write_csv.writerow(writerow)
           
