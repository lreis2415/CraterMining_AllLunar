# coding=utf-8

import numpy as np
from pygeoc.raster import RasterUtilClass
from sklearn.ensemble import RandomForestClassifier
import os
import csv

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
train_folder = parent_path + "\\train_data\\"
LE_folder = parentparent_path + "\\01_Step1_MultiLE\\LE_results\\"
blocksDEM_folder = parentparent_path + "\\00_PreStep_BlocksDivision\\output_blocks\\"
blocks_cratercandidatesgrids_folder = parent_path + "\\blocks_cratercandidatesgrids\\"


Train_filename = train_folder + "Train_Craters.tif"
TrainLE_filename = train_folder + "TrainLE_1km_r60_500m.txt"
def build_gridRF_classifier(Train_filename, TrainLE_filename): 
    TrnSplsLbls = RasterUtilClass.read_raster(Train_filename)
    r = 60
    TrnSplsLbls1D = TrnSplsLbls.data.reshape(TrnSplsLbls.nRows*TrnSplsLbls.nCols, 1)
    TrnSplsLE = np.zeros((TrnSplsLbls.nRows * TrnSplsLbls.nCols, r))
    fTrnSplsLE = open(TrainLE_filename)
    for line in fTrnSplsLE:
        dataline = line.split(',')[:-1]
        dataline = [int(i) for i in dataline]
        index = (dataline[0])*(TrnSplsLbls.nCols) + (dataline[1])
        TrnSplsLE[index] = dataline
    TrnSplsLE = TrnSplsLE[:, 2:r]
    TrnSpls = np.hstack((TrnSplsLE, TrnSplsLbls1D))
    #
    clf = RandomForestClassifier(n_estimators=200, max_features=10,
                                 bootstrap=True, n_jobs=1)
    #
    TrnLabels = TrnSpls[:, -1:]
    TrnInputfeatures = TrnSpls[:, :-1]
    clf.fit(TrnInputfeatures, TrnLabels)
    return clf

def gird_classification(clf, block_rowmax, block_colmax, blocksDEM_folder, blocks_cratercandidatesgrids_folder):
    for blocki in range(0, block_rowmax):
        for blockj in range(0, block_colmax):
            TstBlockName = "blockR" + str(blocki) + "C" + str(blockj)
            TstDEMFileName = blocksDEM_folder + TstBlockName +".tif"
            TstDEM = RasterUtilClass.read_raster(TstDEMFileName)
            TstSplsLE_csv = csv.reader(open(LE_folder + TstBlockName + "LE_csv.csv"))
            TstSplsLE_data = np.array(list(TstSplsLE_csv))
            TstSplsLE = (TstSplsLE_data[:,2:]).astype(np.float).astype(np.int)
            #
            TstRst = clf.predict(TstSplsLE)
            TstCrtCddts = np.zeros((TstDEM.nRows, TstDEM.nCols))
            k = 0
            for i in range(120, TstDEM.nRows-120):
                for j in range(120, TstDEM.nCols-120):
                    TstCrtCddts[i, j] = TstRst[k]
                    k = k+1
            ClcTstRstName = (blocks_cratercandidatesgrids_folder + TstBlockName + "_candidate.tif")
            RasterUtilClass.write_gtiff_file(ClcTstRstName, TstDEM.nRows, TstDEM.nCols,
                                             TstCrtCddts, TstDEM.geotrans, TstDEM.srs,
                                             999, TstDEM.dataType)
    print("OK")