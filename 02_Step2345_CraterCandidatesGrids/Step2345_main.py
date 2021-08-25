# coding=utf-8

import numpy as np
from pygeoc.raster import RasterUtilClass
from sklearn.ensemble import RandomForestClassifier
import os
import csv
import Step2_CraterCandidatesGridsDetection
import Step3_OpeningMerge
import Step4_DBSCAN
import Step5_BorderProcessing

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
train_folder = parent_path + "\\train_data\\"
LE_folder = parentparent_path + "\\01_Step1_MultiLE\\LE_results\\"
blocksDEM_folder = parentparent_path + "\\00_PreStep_BlocksDivision\\output_blocks\\"
blocks_cratercandidatesgrids_folder = parent_path + "\\blocks_cratercandidatesgrids\\"
allLunar_cratercandidatesgrids_folder = parent_path + "\\allLunar_cratercandidatesgrids\\"
allLunar_cratercandidatesgrids_folder = parent_path + "\\allLunar_cratercandidatesgrids\\"
allLunar_DBSCANclusters_folder = parent_path + "\\allLunar_DBSCANclusters\\"
border_processing_folder = parent_path + "\\border_processing\\"



# Step 2 
Train_filename = train_folder + "Train_Craters.tif"
TrainLE_filename = train_folder + "TrainLE_1km_r60_500m.txt"
clf = Step2_CraterCandidatesGridsDetection.build_gridRF_classifier(Train_filename, TrainLE_filename)
Step2_CraterCandidatesGridsDetection.gird_classification(clf, 9, 13, blocksDEM_folder, blocks_cratercandidatesgrids_folder)



# Step 3
Step3_OpeningMerge.opening(blocks_cratercandidatesgrids_folder, 1, 1)
Step3_OpeningMerge.merge(blocks_cratercandidatesgrids_folder, allLunar_cratercandidatesgrids_folder, 9, 13)



# Step 4
AllCrtsCadsFileName = allLunar_cratercandidatesgrids_folder + "All_Lunar_CratersCandidates_afterOpenning_sc.tif"
Step4_DBSCAN.gridsDBSCAN(AllCrtsCadsFileName, allLunar_DBSCANclusters_folder, 5, 10)


# Step 5

DbscanFileName = allLunar_DBSCANclusters_folder + "All_Lunar_CratersCandidates_DBScan_sc.tif"
BorderFileName = Step5_BorderProcessing.produce_clusters_range(DbscanFileName, border_processing_folder)
BorderGridsFileName = Step5_BorderProcessing.border_original_clusters(BorderFileName, DbscanFileName, border_processing_folder)
Step5_BorderProcessing.border_DBSCAN(BorderGridsFileName, border_processing_folder, 5, 10)
borderDbscanFileName = border_processing_folder + "Border_CratersCandidates_DBScan_sc.tif"
Step5_BorderProcessing.produce_border_newclusters_range(borderDbscanFileName, border_processing_folder)
