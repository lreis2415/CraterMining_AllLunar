# coding=utf-8

import numpy as np
import os
from osgeo import ogr, osr, gdal
from pygeoc.raster import RasterUtilClass
from sklearn.cluster import DBSCAN
import csv
from CoordsTrans import *

parent_path = os.path.abspath(os.path.dirname(__file__))
allLunar_DBSCANclusters_folder = parent_path + "\\allLunar_DBSCANclusters\\"
border_processing_folder = parent_path + "\\border_processing\\"

DbscanFileName = allLunar_DBSCANclusters_folder + "All_Lunar_CratersCandidates_DBScan_sc.tif"
def produce_clusters_range(DbscanFileName, border_processing_folder):  
    Dbscan = gdal.Open(DbscanFileName)
    Dbscan_band = Dbscan.GetRasterBand(1)
    Dbscan_data = Dbscan_band.ReadAsArray()
    Dbscan_nRows = Dbscan.RasterYSize
    Dbscan_nCols = Dbscan.RasterXSize
    max_ID = Dbscan_data.max()
    CrtCnds_xys = [[] for ID in range(max_ID+1)]
    for i in range(Dbscan_nRows):
        for j in range(Dbscan_nCols):
            if int(Dbscan_data[i,j]) != -1:
                ID = int(Dbscan_data[i,j])
                CrtCnds_xys[ID].append([i, j])
    #
    origin_clusters_range = []
    border_clusters_range = []
    for ID in range(len(CrtCnds_xys)):
        ID_xys = np.array(CrtCnds_xys[ID])
        [max_row, max_col] = np.amax(ID_xys, axis = 0)
        [min_row, min_col] = np.amin(ID_xys, axis = 0)
        cluster = [ID, max_row, min_row, max_col, min_col]
        origin_clusters_range.append(cluster)
        if max_col >= (Dbscan_nCols - 5) or min_col <= 4:
            border_clusters_range.append(cluster)
    #
    csv_header = ["ID","max row", "min row", "max col", "min col"]
    with open (border_processing_folder + "origin_CrtCnds_xy_ranges.csv", "w", newline = '') as origin_csvdata:
        write_csv = csv.writer(origin_csvdata)
        write_csv.writerow(csv_header)
        write_csv.writerows(origin_clusters_range)
    with open (border_processing_folder + "border_CrtCnds_xy_ranges.csv", "w", newline = '') as border_csvdata:
        write_csv = csv.writer(border_csvdata)
        write_csv.writerow(csv_header)
        write_csv.writerows(border_clusters_range)
    #
    BorderFileName = border_processing_folder + "border_CrtCnds_xy_ranges.csv"        
    return BorderFileName



BorderFileName = border_processing_folder + "border_CrtCnds_xy_ranges.csv"
def border_original_clusters(BorderFileName, DbscanFileName, border_processing_folder):
    Border_CrtCnds_csv = csv.reader(open(BorderFileName))
    Border_CrtCnds_data = np.array(list(Border_CrtCnds_csv))
    Border_CrtCnds = (Border_CrtCnds_data[1:,:]).astype(np.int)
    #
    DbscanData = RasterUtilClass.read_raster(DbscanFileName)         
    #
    bd_cnds = []
    left_bd_mincol = DbscanData.nRows
    right_bd_maxcol = 0
    for i in range(len(Border_CrtCnds)):
        i_bd_cnds = []
        i_bd_cnds_id = int(Border_CrtCnds[i,0])
        i_bd_cnds.append(i_bd_cnds_id)
        for row in range(int(Border_CrtCnds[i,2]), int(Border_CrtCnds[i,1])+1):
            for col in range(int(Border_CrtCnds[i,4]), int(Border_CrtCnds[i,3])+1):
                if DbscanData.data[row, col] == i_bd_cnds_id:
                    i_bd_cnds_coord = [row, col]
                    i_bd_cnds.append(i_bd_cnds_coord)
        bd_cnds.append(i_bd_cnds)
        if Border_CrtCnds[i,3] >= (DbscanData.nRows - 4):
            if Border_CrtCnds[i,4] < left_bd_mincol:
                left_bd_mincol = Border_CrtCnds[i,4]
        elif Border_CrtCnds[i,4] <= 4:
            if Border_CrtCnds[i,3] > right_bd_maxcol:
                right_bd_maxcol = Border_CrtCnds[i,3]            
    left_bd = int(DbscanData.nCols - left_bd_mincol)
    right_bd= int(right_bd_maxcol + 1)
    # left_bd = 13881
    # right_bd= 7065
    bd_cnds_id = np.ones([DbscanData.nRows, left_bd+right_bd]) * (-1)
    bd_cnds_is = np.zeros([DbscanData.nRows, left_bd+right_bd]) 
    for cnd in range(len(bd_cnds)):
        cnd_id = int(bd_cnds[cnd][0])
        if (Border_CrtCnds[cnd, 4] < 100):
            for cnd_point in range(1, len(bd_cnds[cnd])):
                new_rowcol = [bd_cnds[cnd][cnd_point][0], bd_cnds[cnd][cnd_point][1] + left_bd]
                bd_cnds_id[new_rowcol[0], new_rowcol[1]] = cnd_id
                bd_cnds_is[new_rowcol[0], new_rowcol[1]] = 1
        else:
            for cnd_point in range(1, len(bd_cnds[cnd])):
                new_rowcol = [bd_cnds[cnd][cnd_point][0], bd_cnds[cnd][cnd_point][1] - left_bd_mincol]
                bd_cnds_id[new_rowcol[0], new_rowcol[1]] = cnd_id
                bd_cnds_is[new_rowcol[0], new_rowcol[1]] = 1
    bd_cnds_id = np.array(bd_cnds_id)
    bd_cnds_is = np.array(bd_cnds_is)
    #
    new_geotrans = (DbscanData.geotrans[0]-left_bd*DbscanData.geotrans[1], DbscanData.geotrans[1], 
                    DbscanData.geotrans[2], DbscanData.geotrans[3], 
                    DbscanData.geotrans[4], DbscanData.geotrans[5])
    CndsIDFileName =  border_processing_folder + "border_CrtCnds_original_ID_sc.tif"
    CndsISFileName =  border_processing_folder + "border_fordbscan_sc.tif"
    RasterUtilClass.write_gtiff_file(CndsIDFileName, DbscanData.nRows,
                                     left_bd+right_bd, bd_cnds_id, new_geotrans,
                                     DbscanData.srs, -1, 5)
    RasterUtilClass.write_gtiff_file(CndsISFileName, DbscanData.nRows,
                                     left_bd+right_bd, bd_cnds_is, new_geotrans,
                                     DbscanData.srs, -1, 5)
    return CndsISFileName



BorderGridsFileName = border_processing_folder + "border_fordbscan_sc.tif"
def border_DBSCAN(BorderGridsFileName, border_processing_folder, eps, min_samples):
    BorderGrids = RasterUtilClass.read_raster(BorderGridsFileName)
    BorderGridsData = BorderGrids.data
    CrtCndsPxls = np.where(BorderGridsData == 1, 1, BorderGridsData)
    PxlsCoord = np.where(CrtCndsPxls == 1)
    PxlsCoord = np.array([PxlsCoord[0], PxlsCoord[1]]).swapaxes(0,1)
    # 
    DbScan = DBSCAN(eps=eps, min_samples=min_samples).fit(PxlsCoord)
    DbCrtCndsLbls = np.array(DbScan.labels_).reshape((DbScan.labels_.shape[0],1))
    DbCrtCndsPxls = np.concatenate((PxlsCoord, DbCrtCndsLbls), axis=1)
    # 
    DbCrtCndsData = np.ones((BorderGrids.nRows, BorderGrids.nCols)) * -1
    for i in range(DbCrtCndsPxls.shape[0]):
        DbCrtCndsData[DbCrtCndsPxls[i,0], DbCrtCndsPxls[i,1]] = DbCrtCndsPxls[i,2]
    DbBdCrtsFileName =  border_processing_folder + "Border_CratersCandidates_DBScan_sc.tif"
    RasterUtilClass.write_gtiff_file(DbBdCrtsFileName, BorderGrids.nRows,
                                     BorderGrids.nCols, DbCrtCndsData, BorderGrids.geotrans,
                                     BorderGrids.srs, -1, 5)
    return DbBdCrtsFileName

borderDbscanFileName = border_processing_folder + "Border_CratersCandidates_DBScan_sc.tif"
def produce_border_newclusters_range(borderDbscanFileName, border_processing_folder):  
    Dbscan = gdal.Open(borderDbscanFileName)
    Dbscan_band = Dbscan.GetRasterBand(1)
    Dbscan_data = Dbscan_band.ReadAsArray()
    Dbscan_nRows = Dbscan.RasterYSize
    Dbscan_nCols = Dbscan.RasterXSize
    max_ID = Dbscan_data.max()
    CrtCnds_xys = [[] for ID in range(max_ID+1)]
    for i in range(Dbscan_nRows):
        for j in range(Dbscan_nCols):
            if int(Dbscan_data[i,j]) != -1:
                ID = int(Dbscan_data[i,j])
                CrtCnds_xys[ID].append([i, j])
    #
    border_newclusters_range = []
    for ID in range(len(CrtCnds_xys)):
        ID_xys = np.array(CrtCnds_xys[ID])
        [max_row, max_col] = np.amax(ID_xys, axis = 0)
        [min_row, min_col] = np.amin(ID_xys, axis = 0)
        cluster = [ID, max_row, min_row, max_col, min_col]
        border_newclusters_range.append(cluster)
    #
    csv_header = ["ID","max row", "min row", "max col", "min col"]
    with open (border_processing_folder + "border_NewCrtCnds_xy_ranges.csv", "w", newline = '') as border_csvdata:
        write_csv = csv.writer(border_csvdata)
        write_csv.writerow(csv_header)
        write_csv.writerows(border_newclusters_range)