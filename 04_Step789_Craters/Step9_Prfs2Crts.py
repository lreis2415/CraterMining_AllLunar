# coding=utf-8


import os
import csv
import numpy as np

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
test_prfs_RFresult_path = parent_path + "\\crcs_normprfs_RFresults\\"
crcs_RFresult_path = parent_path + "\\crcs_RFresult\\"
border_processing_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\border_processing\\"

def prfs2crts_result(test_prfs_RFresult_path, crcs_RFresult_path, border_processing_folder):
    test_prfs_RFresult_files = os.listdir(test_prfs_RFresult_path)
    csv_header = ['crc_ID', 'radius_km_type', "crc_result", "delete_border"]
    all_crcs_result = []
    for test_prfs_RFresult_file in test_prfs_RFresult_files:
        test_prfs_RFresult_csv = csv.reader(open(test_prfs_RFresult_path + test_prfs_RFresult_file))
        test_prfs_RFresult_data = np.array(list(test_prfs_RFresult_csv)[1:]).astype(np.float)
        temp_crcs_num = len(test_prfs_RFresult_data)/12
        for i in range(int(temp_crcs_num)):
            start_record_i = i*12
            crc_ID = test_prfs_RFresult_data[start_record_i, 0]
            radius = test_prfs_RFresult_data[start_record_i, 2]
            pos_num = 0
            for j in range(12):
                prf_j = start_record_i + j
                if test_prfs_RFresult_data[prf_j, 3] == 1:
                    pos_num = pos_num + 1
            pos_pct = pos_num/float(12)
            if pos_pct >= 0.5:
                crc_cls_result = 1
            else:
                crc_cls_result = 0
            crc_result = [crc_ID, radius, crc_cls_result, 0]
            all_crcs_result.append(crc_result)
    border_crc_file = border_processing_folder + "border_CrtCnds_xy_ranges.csv"
    border_crc_csv = csv.reader(open(border_crc_file))
    border_crc_data = np.array(list(border_crc_csv)[1:]).astype(np.int)
    for i in range(len(border_crc_data)):
        border_crc_ID = border_crc_data[i,0]
        all_crcs_result[border_crc_ID][3] = 1
    crcs_RFressult_filename = crcs_RFresult_path + "crcs_RFresult.csv"
    with open (crcs_RFressult_filename, "w", newline = '') as csv_data:
        write_csv = csv.writer(csv_data)
        write_csv.writerow(csv_header)
        write_csv.writerows(all_crcs_result)


