# coding=utf-8
# @Time    :4/12/2018 10:56 AM
# @Author  : Yanwen Wang

# This file aims to calculate the normalized elevation profiles of crater
# candidates in testing area(application area).

import os
import csv
import NormPrf_Functions

parent_path = os.path.abspath(os.path.dirname(__file__))
crcs_prfs_dem_path = parent_path + "\\crcs_prfs_dem\\"
crcs_normprfs_path = parent_path + "\\crcs_normprfs\\"

def calc_normprfs(crcs_prfs_dem_path, crcs_normprfs_path):
    #
    for start_ID in range(0, 84000, 1000):
        crcs_prfs_FileName =  crcs_prfs_dem_path + "Crcs_CrtCnds_" + str(start_ID+999) + "_prfs_dem.csv"
        crcs_prfs_csv = csv.reader(open(crcs_prfs_FileName))
        crcs_prfs_data = list(crcs_prfs_csv)[1:]
        ID_base = start_ID
        crcs_RF_prfs = []
        for i in range(len(crcs_prfs_data)):
            i_crc_prf = crcs_prfs_data[i]
            i_crc_RF_prf = NormPrf_Functions.crcs_RF_prfs(i_crc_prf, ID_base)
            crcs_RF_prfs.append(i_crc_RF_prf)
        csv_header = ['crc_ID', 'prf_ID', 'radius_km']
        with open (crcs_normprfs_path + "Crcs_CrtCnds_" + str(start_ID+999) + "_RF_prfs.csv", "w", newline = '') as csv_data:
            write_csv = csv.writer(csv_data)
            write_csv.writerow(csv_header)
            for i in range(len(crcs_RF_prfs)):
                writerow = crcs_RF_prfs[i]
                write_csv.writerow(writerow)
    #
    crcs_prfs_84560_FileName =  crcs_prfs_dem_path + "Crcs_CrtCnds_84560_prfs_dem.csv"
    crcs_prfs_84560_csv = csv.reader(open(crcs_prfs_84560_FileName))
    crcs_prfs_84560_data = list(crcs_prfs_84560_csv)[1:]
    ID_base = 84000
    crcs_84560_RF_prfs = []
    for i in range(len(crcs_prfs_84560_data)):
        i_crc_prf = crcs_prfs_84560_data[i]
        i_crc_RF_prf = NormPrf_Functions.crcs_RF_prfs(i_crc_prf, ID_base)
        crcs_84560_RF_prfs.append(i_crc_RF_prf)
    csv_header = ['crc_ID', 'prf_ID', 'radius_km']
    with open (crcs_normprfs_path + "Crcs_CrtCnds_84560_RF_prfs.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(crcs_84560_RF_prfs)):
            writerow = crcs_84560_RF_prfs[i]
            write_csv.writerow(writerow)
    #
    crcs_prfs_n_FileName =  crcs_prfs_dem_path + "Crcs_north_border_CrtCnds_prfs_dem.csv"
    crcs_prfs_n_csv = csv.reader(open(crcs_prfs_n_FileName))
    crcs_prfs_n_data = list(crcs_prfs_n_csv)[1:]
    ID_base = 84560
    crcs_n_RF_prfs = []
    for i in range(len(crcs_prfs_n_data)):
        i_crc_prf = crcs_prfs_n_data[i]
        i_crc_RF_prf = NormPrf_Functions.crcs_RF_prfs(i_crc_prf, ID_base)
        crcs_n_RF_prfs.append(i_crc_RF_prf)
    csv_header = ['crc_ID', 'prf_ID', 'radius_km']
    with open (crcs_normprfs_path + "Crcs_north_border_CrtCnds_RF_prfs.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(crcs_n_RF_prfs)):
            writerow = crcs_n_RF_prfs[i]
            write_csv.writerow(writerow)
    #
    crcs_prfs_s_FileName =  crcs_prfs_dem_path + "Crcs_south_border_CrtCnds_prfs_dem.csv"
    crcs_prfs_s_csv = csv.reader(open(crcs_prfs_s_FileName))
    crcs_prfs_s_data = list(crcs_prfs_s_csv)[1:]
    ID_base = 84660
    crcs_s_RF_prfs = []
    for i in range(len(crcs_prfs_s_data)):
        i_crc_prf = crcs_prfs_s_data[i]
        i_crc_RF_prf = NormPrf_Functions.crcs_RF_prfs(i_crc_prf, ID_base)
        crcs_s_RF_prfs.append(i_crc_RF_prf)
    csv_header = ['crc_ID', 'prf_ID', 'radius_km']
    with open (crcs_normprfs_path + "Crcs_south_border_CrtCnds_RF_prfs.csv", "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        for i in range(len(crcs_s_RF_prfs)):
            writerow = crcs_s_RF_prfs[i]
            write_csv.writerow(writerow)
        


