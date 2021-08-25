# coding=utf-8

import numpy as np
from pygeoc.raster import RasterUtilClass
import os

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
train_folder = parent_path + "\\train_data\\"
LE_folder = parentparent_path + "\\01_Step1_MultiLE\\LE_results\\"
blocksDEM_folder = parentparent_path + "\\00_PreStep_BlocksDivision\\output_blocks\\"
blocks_cratercandidatesgrids_folder = parent_path + "\\blocks_cratercandidatesgrids\\"
allLunar_cratercandidatesgrids_folder = parent_path + "\\allLunar_cratercandidatesgrids\\"


def opening(blocks_cratercandidatesgrids_folder, block_rowmax, block_colmax):    
    for blocki in range(0, block_rowmax):
        for blockj in range(0, block_colmax):
            current_block = "blockR" + str(blocki) + "C" + str(blockj)
            InitCrtsFileName = blocks_cratercandidatesgrids_folder + current_block + "_candidate.tif"
            InitCrts = RasterUtilClass.read_raster(InitCrtsFileName)
            OpnCrtsData = RasterUtilClass.openning(InitCrtsFileName,1)
            FinalOpnCrtsData = OpnCrtsData[120:InitCrts.nRows-120, 120:InitCrts.nCols-120]
            OpnCrtsFileName = blocks_cratercandidatesgrids_folder + current_block + "_openning&cut.tif"
            FinalGeotrans = [InitCrts.geotrans[0] + InitCrts.geotrans[1]*120, InitCrts.geotrans[1],
                             InitCrts.geotrans[2], InitCrts.geotrans[3] + InitCrts.geotrans[5]*120,
                             InitCrts.geotrans[4], InitCrts.geotrans[5]]
            RasterUtilClass.write_gtiff_file(OpnCrtsFileName, InitCrts.nRows-240,
                                     InitCrts.nCols-240, FinalOpnCrtsData, FinalGeotrans,
                                     InitCrts.srs, 999, InitCrts.dataType)      
    print("OK")


def merge(blocks_cratercandidatesgrids_folder, allLunar_cratercandidatesgrids_folder, block_rowmax, block_colmax):
    start_block = "blockR0C0"
    CrtsFileName = blocks_cratercandidatesgrids_folder + start_block + "_openning&cut.tif"
    start_Crts = RasterUtilClass.read_raster(CrtsFileName)
    MscnRows = start_Crts.nRows * block_rowmax
    MscnCols = start_Crts.nCols * block_colmax
    MscCrtsData = np.zeros((MscnRows, MscnCols))
    for blocki in range(0, block_rowmax):
        for blockj in range(0, block_colmax):
            current_block = "blockR" + str(blocki) + "C" + str(blockj)
            SglCrtsFileName = blocks_cratercandidatesgrids_folder + current_block + "_openning&cut.tif"
            SglCrts = RasterUtilClass.read_raster(SglCrtsFileName)
            Left_x_pixel = blockj * SglCrts.nCols
            Right_x_pixel = (blockj+1) * SglCrts.nCols
            Top_y_pixel = blocki * SglCrts.nRows
            Bottom_y_pixel = (blocki+1) * SglCrts.nRows
            MscCrtsData[Top_y_pixel:Bottom_y_pixel, Left_x_pixel:Right_x_pixel] = SglCrts.data[:,:]
    MscCrtsFileName = allLunar_cratercandidatesgrids_folder + "All_Lunar_CratersCandidates_afterOpenning.tif"
    RasterUtilClass.write_gtiff_file(MscCrtsFileName, MscnRows, MscnCols, MscCrtsData, 
                                     start_Crts.geotrans, start_Crts.srs, 999, start_Crts.dataType)
