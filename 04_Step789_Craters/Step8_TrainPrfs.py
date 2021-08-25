# coding=utf-8

import os
import shapefile
from pygeoc.raster import RasterUtilClass
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import random

skl_lines = [[0, 1], [1, 0], [0, -1], [-1, 0]]
line_theta = [math.pi/6, math.pi/3, 2*math.pi/3, 5*math.pi/6, 7*math.pi/6,
              4*math.pi/3, 5*math.pi/3, 11*math.pi/6]


def calc_attributes(line_j, center_elev, center, line_ID):
    points_num = len(line_j)
    long = float(points_num/10)
    attr_set = []
    for k in range(10):
        k_elev_sum = sum([k_elev for k_elev in line_j[int(k*long):int((k+1)*long)]])
        k_elev_num = len(line_j[int(k*long):int((k+1)*long)])
        k_attr = float(k_elev_sum/k_elev_num) - center_elev
        attr_set.append(k_attr)
    min_attr = min(attr_set)
    attr_range = max(attr_set) - min_attr
    std_attr_set = []
    std_attr_set.append(center[2])
    std_attr_set.append(line_ID)
    for k in range(len(attr_set)):
        std_attr = float((attr_set[k] - min_attr)/attr_range)
        std_attr_set.append(std_attr)
    return std_attr_set

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
traininput_path = parent_path + "\\train_input\\"
trainDEM_path = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\train_data\\"
trainoutput_path = parent_path + "\\train_output\\"

def calc_train_prfs(traininput_path, trainDEM_path, trainoutput_path):
    ###
    ##
    # Positive profiles samples.
    CentersFileName = (traininput_path + "TrainSamples_CratersCenters")
    Centers = shapefile.Reader(CentersFileName)
    CentersRcds = Centers.records()
    CentersInf = []
    for i in range(len(CentersRcds)):
        temp_centers = CentersRcds[i]
        CentersInf.append([temp_centers[6], temp_centers[7], temp_centers[2],
                             temp_centers[3]])
    DEMFileName = (trainDEM_path + "TrainDEM_500m_calc.tif")
    DEM = RasterUtilClass.read_raster(DEMFileName)
    DEMData = DEM.data
    #
    lines_attr_set = []
    for i in range(len(CentersInf)):
        center_i = CentersInf[i]
        center_i_elev = DEMData[center_i[0],center_i[1]]
        i_r = center_i[3]
        for j in range(4):
            line_j_endpoint = [center_i[0] + i_r * skl_lines[j][0], center_i[1] +
                               i_r * skl_lines[j][1]]
            line_j = []
            if (line_j_endpoint[0]>=0 and line_j_endpoint[0]<DEM.nRows and
                line_j_endpoint[1]>=0 and line_j_endpoint[1]<DEM.nCols) :
                for k in range(1,i_r+1):
                    line_j_temppoint =  [center_i[0] + k * skl_lines[j][0],
                                         center_i[1] + k * skl_lines[j][1]]
                    line_j_temppoint_elve = DEMData[line_j_temppoint[0],
                                                    line_j_temppoint[1]]
                    line_j.append(line_j_temppoint_elve)
                line_j_attr = calc_attributes(line_j, center_i_elev, center_i, j)
                lines_attr_set.append(line_j_attr)
        for j in range(len(line_theta)):
            theta = line_theta[j]
            line_j_endpoint = [center_i[0] + int(i_r * math.sin(theta)),
                               center_i[1] + int(i_r * math.cos(theta))]
            line_j = []
            if (line_j_endpoint[0]>=0 and line_j_endpoint[0]<DEM.nRows and
                line_j_endpoint[1]>=0 and line_j_endpoint[1]<DEM.nCols) :
                for k in range(1,i_r+1):
                    line_j_temppoint = [center_i[0] + int(k * math.sin(theta)),
                                        center_i[1] + int(k * math.cos(theta))]
                    line_j_temppoint_elve = DEMData[line_j_temppoint[0],
                                                    line_j_temppoint[1]]
                    line_j.append(line_j_temppoint_elve)
                line_j_attr = calc_attributes(line_j, center_i_elev, center_i, j+4)
                lines_attr_set.append(line_j_attr)
    x = range(10)
    for i in range(len(lines_attr_set)):
        plt.plot(x, lines_attr_set[i][2:12], color='b', alpha = 0.3)
    plt.show()
    #
    csv_header = ["crc_ID","prf_ID"]
    with open (trainoutput_path + "crcs_train_POS_prfs_RF.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(lines_attr_set)):
            writerow = lines_attr_set[i]
            write_csv.writerow(writerow)
    ###
    ##
    # Negative profiles samples.
    NoCratersFileName = traininput_path+ "Train_NoCraters.tif"
    NoCraters = RasterUtilClass.read_raster(NoCratersFileName)
    NoCratersCenters = []
    for i in range(len(CentersInf)):
        x, y = np.where(NoCraters.data == CentersInf[i][3])
        k = random.randint(0, len(x))
        NoCratersCenters.append([x[k], y[k], CentersInf[i][2], CentersInf[i][3]])
    lines_attr_set = []
    for i in range(len(NoCratersCenters)):
        center_i = NoCratersCenters[i]
        center_i_elev = DEMData[center_i[0],center_i[1]]
        i_r = center_i[3]
        # Skeleton lines.
        for j in range(4):
            line_j_endpoint = [center_i[0] + i_r * skl_lines[j][0], center_i[1] +
                               i_r * skl_lines[j][1]]
            line_j = []
            if (line_j_endpoint[0]>=0 and line_j_endpoint[0]<DEM.nRows and
                line_j_endpoint[1]>=0 and line_j_endpoint[1]<DEM.nCols) :
                # Extract the
                for k in range(1,i_r+1):
                    line_j_temppoint =  [center_i[0] + k * skl_lines[j][0],
                                         center_i[1] + k * skl_lines[j][1]]
                    line_j_temppoint_elve = DEMData[line_j_temppoint[0],
                                                    line_j_temppoint[1]]
                    line_j.append(line_j_temppoint_elve)
                line_j_attr = calc_attributes(line_j, center_i_elev, center_i, j)
                lines_attr_set.append(line_j_attr)
        for j in range(len(line_theta)):
            theta = line_theta[j]
            line_j_endpoint = [center_i[0] + int(i_r * math.sin(theta)),
                               center_i[1] + int(i_r * math.cos(theta))]
            line_j = []
            if (line_j_endpoint[0]>=0 and line_j_endpoint[0]<DEM.nRows and
                line_j_endpoint[1]>=0 and line_j_endpoint[1]<DEM.nCols) :
                for k in range(1,i_r+1):
                    line_j_temppoint = [center_i[0] + int(k * math.sin(theta)),
                                        center_i[1] + int(k * math.cos(theta))]
                    line_j_temppoint_elve = DEMData[line_j_temppoint[0],
                                                    line_j_temppoint[1]]
                    line_j.append(line_j_temppoint_elve)
                line_j_attr = calc_attributes(line_j, center_i_elev, center_i, j+4)
                lines_attr_set.append(line_j_attr)
    x = range(10)
    for i in range(len(lines_attr_set)):
        plt.plot(x, lines_attr_set[i][2:12], color='b', alpha = 0.3)
    plt.show()
    #
    csv_header = ["crc_ID","prf_ID"]
    with open (trainoutput_path + "crcs_train_NEG_prfs_RF.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(lines_attr_set)):
            writerow = lines_attr_set[i]
            write_csv.writerow(writerow)