# coding=utf-8
# @Time    :4/12/2018 10:56 AM
# @Author  : Yanwen Wang

# This file aims to calculate the normalized elevation profiles of crater
# candidates in testing area(application area).

import os
import csv
from sklearn.ensemble import RandomForestClassifier
import numpy as np


parent_path = os.path.abspath(os.path.dirname(__file__))
test_prfs_RF_path =  parent_path + "\\crcs_normprfs\\"
train_prfs_RF_path = parent_path + "\\train_output\\"
test_prfs_RFresult_path = parent_path + "\\crcs_normprfs_RFresults\\"

def profile_classification(test_prfs_RF_path, train_prfs_RF_path, test_prfs_RFresult_path):
    test_prfs_RF_files = os.listdir(test_prfs_RF_path)
    NEG_train_prfs_RF_file = train_prfs_RF_path + "crcs_train_NEG_prfs_RF.csv"
    POS_train_prfs_RF_file = train_prfs_RF_path + "crcs_train_POS_prfs_RF.csv"
    # Negative
    train_NEG_prfs_csv = csv.reader(open(NEG_train_prfs_RF_file))
    train_NEG_prfs_data = np.array(list(train_NEG_prfs_csv)[1:]).astype(np.float)
    train_NEG_prfs_fts = train_NEG_prfs_data[:,2:]
    train_NEG_prfs_lbs = np.zeros((len(train_NEG_prfs_fts)))
    # Positive
    train_POS_prfs_csv = csv.reader(open(POS_train_prfs_RF_file))
    train_POS_prfs_data = np.array(list(train_POS_prfs_csv)[1:]).astype(np.float)
    train_POS_prfs_fts = train_POS_prfs_data[:,2:]
    train_POS_prfs_lbs = np.ones((len(train_POS_prfs_fts)))
    #
    TrainData = np.vstack((train_POS_prfs_fts, train_NEG_prfs_fts))
    TrainLabel = np.hstack((train_POS_prfs_lbs, train_NEG_prfs_lbs))
    #
    clf = RandomForestClassifier(n_estimators=200, max_features=10,
                                 bootstrap=True, n_jobs=1)
    clf.fit(TrainData, TrainLabel)
    #
    csv_header = ['crc_ID', 'prf_ID', 'radius_km', "profile_result"]
    for test_prfs_RF_file in test_prfs_RF_files:
        test_prfs_csv = csv.reader(open(test_prfs_RF_path + test_prfs_RF_file))
        test_prfs_data = np.array(list(test_prfs_csv)[1:]).astype(np.float)
        test_prfs_fts = test_prfs_data[:,3:]
        test_prfs_lbs = clf.predict(test_prfs_fts)
        test_prfs_RFressult_filename = str(test_prfs_RF_file.split('.')[:-1][0]) + "_result.csv"
        with open (test_prfs_RFresult_path + test_prfs_RFressult_filename, "w", newline = '') as csv_data:
            write_csv = csv.writer(csv_data)
            write_csv.writerow(csv_header)
            for i in range(len(test_prfs_lbs)):
                writerow = [test_prfs_data[i,0], test_prfs_data[i,1], test_prfs_data[i,2], test_prfs_lbs[i]]
                write_csv.writerow(writerow)

