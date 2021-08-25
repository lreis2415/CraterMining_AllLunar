# coding=utf-8

import numpy as np
import os
from osgeo import ogr, osr, gdal
import csv
import CoordsTrans
import Step6_Clusters2Objects

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
allLunar_DBSCANclusters_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\allLunar_DBSCANclusters\\"
border_processing_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\border_processing\\"
crcsshp_folder = parent_path + "\\crcs_shp\\"


origin_DbscanFileName = allLunar_DBSCANclusters_folder + "All_Lunar_CratersCandidates_DBScan_sc.tif"
border_DbscanFileName = border_processing_folder + "Border_CratersCandidates_DBScan_sc.tif"
origin_CrtCnds_xys_file = border_processing_folder + "origin_CrtCnds_xy_ranges.csv"
border_CrtCnds_xys_file = border_processing_folder + "border_NewCrtCnds_xy_ranges.csv"


Step6_Clusters2Objects.clusters_grds2pnts(origin_DbscanFileName, border_DbscanFileName, origin_CrtCnds_xys_file, border_CrtCnds_xys_file, crcsshp_folder)
Step6_Clusters2Objects.CrtCnds_pnts2objs(parent_path)
