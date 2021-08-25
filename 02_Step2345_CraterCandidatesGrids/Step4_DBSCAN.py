# coding=utf-8

import numpy as np
from pygeoc.raster import RasterUtilClass
from sklearn.cluster import DBSCAN
import os

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
allLunar_cratercandidatesgrids_folder = parent_path + "\\allLunar_cratercandidatesgrids\\"
allLunar_DBSCANclusters_folder = parent_path + "\\allLunar_DBSCANclusters\\"


AllCrtsCadsFileName = allLunar_cratercandidatesgrids_folder + "All_Lunar_CratersCandidates_afterOpenning_sc.tif"
eps = 5
min_samples = 10

def gridsDBSCAN(AllCrtsCadsFileName, allLunar_DBSCANclusters_folder, eps, min_samples):
    AllCrtsCads = RasterUtilClass.read_raster(AllCrtsCadsFileName)
    AllCrtsCadsData = AllCrtsCads.data
    OpnCrtsPxls = np.where(AllCrtsCadsData == 1, 1, AllCrtsCadsData)
    PxlsCoord = np.where(OpnCrtsPxls == 1)
    PxlsCoord = np.array([PxlsCoord[0], PxlsCoord[1]]).swapaxes(0,1)
    DbScan = DBSCAN(eps=eps, min_samples=min_samples).fit(PxlsCoord)
    DbCrtsLbls = np.array(DbScan.labels_).reshape((DbScan.labels_.shape[0],1))
    DbCrtsPxls = np.concatenate((PxlsCoord, DbCrtsLbls), axis=1)
    DbCrtsData = np.ones((AllCrtsCads.nRows, AllCrtsCads.nCols)) * -1
    for i in range(DbCrtsPxls.shape[0]):
        DbCrtsData[DbCrtsPxls[i,0], DbCrtsPxls[i,1]] = DbCrtsPxls[i,2]
    OpnCrtsFileName =  allLunar_DBSCANclusters_folder + "All_Lunar_CratersCandidates_DBScan_sc.tif"
    RasterUtilClass.write_gtiff_file(OpnCrtsFileName, AllCrtsCads.nRows,
                                 AllCrtsCads.nCols, DbCrtsData, AllCrtsCads.geotrans,
                                 AllCrtsCads.srs, -1, 5)          
    print("OK")
