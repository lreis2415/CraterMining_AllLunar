# coding=utf-8

import shapefile
import numpy as np
import os
from osgeo import ogr, osr, gdal
import math
from pygeoc.raster import RasterUtilClass
import csv
import CoordsTrans
import Step7_CrtCndsPrfs
import Step7_NormPrfs
import Step8_TrainPrfs
import Step8_ClassifyPrfs
import Step9_Prfs2Crts


parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
crcs_shp_path =  parentparent_path + "\\03_Step6_Clusters2Objects\\crcs_shp\\"
crcs_prfs_dem_path = parent_path + "\\crcs_prfs_dem\\"
DEM_path = parentparent_path + "\\00_PreStep_BlocksDivision\\original_DEM\\"
Rst_path = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\allLunar_DBSCANclusters\\"
crcs_normprfs_path = parent_path + "\\crcs_normprfs\\"
traininput_path = parent_path + "\\train_input\\"
trainDEM_path = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\train_data\\"
trainoutput_path = parent_path + "\\train_output\\"
test_prfs_RFresult_path = parent_path + "\\crcs_normprfs_RFresults\\"
crcs_RFresult_path = parent_path + "\\crcs_RFresult\\"
border_processing_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\border_processing\\"


DEMFileName = DEM_path + "globalDEM.tif"
RstFileName = Rst_path + "All_Lunar_CratersCandidates_DBScan_sc.tif"


# Step 7
Step7_CrtCndsPrfs.norm_profile_csv(RstFileName, DEMFileName, crcs_shp_path, crcs_prfs_dem_path)
Step7_NormPrfs.calc_normprfs(crcs_prfs_dem_path, crcs_normprfs_path)


# Step 8
Step8_TrainPrfs.calc_train_prfs(traininput_path, trainDEM_path, trainoutput_path)
Step8_ClassifyPrfs.profile_classification(crcs_normprfs_path, trainoutput_path, test_prfs_RFresult_path)


# Step 9
Step9_Prfs2Crts.prfs2crts_result(test_prfs_RFresult_path, crcs_RFresult_path, border_processing_folder)