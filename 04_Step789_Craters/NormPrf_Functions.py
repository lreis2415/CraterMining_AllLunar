# coding=utf-8

def more10kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num):
    crc_ID = int(crc_ID)
    prf_ID = int(prf_ID)
    prf_dem_pxls = [int(x) for x in prf_dem_pxls]
    long = float(pxls_num/10)
    RF_prf_dem_pxls = []
    for k in range(10):
        k_dem_sum = sum([k_dem for k_dem in prf_dem_pxls[int(k*long):int((k+1)*long)]])
        k_dem_num = len(prf_dem_pxls[int(k*long):int((k+1)*long)])
        k_rele_dem = float(k_dem_sum/k_dem_num) - prf_dem_pxls[0]
        RF_prf_dem_pxls.append(k_rele_dem)
    min_rele_dem = min(RF_prf_dem_pxls)
    rele_dem_range = max(RF_prf_dem_pxls) - min_rele_dem
    std_RF_prf_dem_pxls = []
    std_RF_prf_dem_pxls.append(crc_ID)
    std_RF_prf_dem_pxls.append(prf_ID)
    std_RF_prf_dem_pxls.append(10) 
    for k in range(len(RF_prf_dem_pxls)):
        std_rele_dem = float((RF_prf_dem_pxls[k] - min_rele_dem)/rele_dem_range)
        std_RF_prf_dem_pxls.append(std_rele_dem)
    return std_RF_prf_dem_pxls


def more5kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num):
    crc_ID = int(crc_ID)
    prf_ID = int(prf_ID)
    prf_dem_pxls = [int(x) for x in prf_dem_pxls]
    long = float(pxls_num/10)
    RF_prf_dem_pxls = []
    for k in range(10):
        k_dem_sum = sum([k_dem for k_dem in prf_dem_pxls[int(k*long):int((k+1)*long)]])
        k_dem_num = len(prf_dem_pxls[int(k*long):int((k+1)*long)])
        k_rele_dem = float(k_dem_sum/k_dem_num) - prf_dem_pxls[0]
        RF_prf_dem_pxls.append(k_rele_dem)
    min_rele_dem = min(RF_prf_dem_pxls)
    rele_dem_range = max(RF_prf_dem_pxls) - min_rele_dem
    std_RF_prf_dem_pxls = []
    std_RF_prf_dem_pxls.append(crc_ID)
    std_RF_prf_dem_pxls.append(prf_ID)
    std_RF_prf_dem_pxls.append(5) 
    for k in range(len(RF_prf_dem_pxls)):
        std_rele_dem = float((RF_prf_dem_pxls[k] - min_rele_dem)/rele_dem_range)
        std_RF_prf_dem_pxls.append(std_rele_dem)
    return std_RF_prf_dem_pxls


def more1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num):
    crc_ID = int(crc_ID)
    prf_ID = int(prf_ID)
    prf_dem_pxls = [int(x) for x in prf_dem_pxls]
    pixels_length = float(0+9)/float(pxls_num - 1)
    rest_num = 10
    RF_prf_dem_pxls = []
    for i in range(pxls_num - 2):
        start_dem = prf_dem_pxls[i]
        end_dem = prf_dem_pxls[i+1]
        temp_int_length = int(pixels_length * (i + 1))-int(pixels_length * i)
        inter_dem = float(end_dem - start_dem)/temp_int_length
        for j in range(temp_int_length):
            RF_prf_dem_pxls.append(start_dem + j * inter_dem)
            rest_num = rest_num - 1
    start_dem = prf_dem_pxls[-2]
    end_dem = prf_dem_pxls[-1]
    inter_dem = float(end_dem - start_dem)/(rest_num - 1)
    for j in range(rest_num):
        RF_prf_dem_pxls.append(start_dem + j * inter_dem)
    min_dem = min(RF_prf_dem_pxls)
    rele_dem_range = max(RF_prf_dem_pxls) - min_dem
    if rele_dem_range == 0:
        rele_dem_range = 0.0000000001 
    std_RF_prf_dem_pxls = []
    std_RF_prf_dem_pxls.append(crc_ID)
    std_RF_prf_dem_pxls.append(prf_ID)
    std_RF_prf_dem_pxls.append(1) 
    for k in range(len(RF_prf_dem_pxls)):
        std_rele_dem = float((RF_prf_dem_pxls[k] - min_dem)/rele_dem_range)
        std_RF_prf_dem_pxls.append(std_rele_dem)
    return std_RF_prf_dem_pxls


def equal1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num):
    crc_ID = int(crc_ID)
    prf_ID = int(prf_ID)
    std_RF_prf_dem_pxls = []
    std_RF_prf_dem_pxls.append(crc_ID)
    std_RF_prf_dem_pxls.append(prf_ID)
    std_RF_prf_dem_pxls.append(0.1) 
    if(prf_dem_pxls[0] > prf_dem_pxls[1]):
        std_RF_prf_dem_pxls.append(1)
        for i in range(1,10):
            i_dem = 1-float(1)/float(9)*i
            std_RF_prf_dem_pxls.append(i_dem)
    else:
        std_RF_prf_dem_pxls.append(0)
        for i in range(1,10):
            i_dem = float(1)/float(9)*i
            std_RF_prf_dem_pxls.append(i_dem)
    return std_RF_prf_dem_pxls


def less1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num):
    crc_ID = int(crc_ID)
    prf_ID = int(prf_ID)
    std_RF_prf_dem_pxls = []
    std_RF_prf_dem_pxls.append(crc_ID)
    std_RF_prf_dem_pxls.append(prf_ID)
    std_RF_prf_dem_pxls.append(0) 
    for i in range(10):
        std_RF_prf_dem_pxls.append(0)
    return std_RF_prf_dem_pxls


def crcs_RF_prfs(prf_dem_record, ID_base):
    crc_ID = int(prf_dem_record[0]) + ID_base
    prf_ID = int(prf_dem_record[1])
    prf_dem_pxls = prf_dem_record[2:]
    pxls_num = len(prf_dem_pxls)
    if pxls_num >= 20:
        std_RF_prf = more10kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num)
    elif pxls_num >= 10:
        std_RF_prf = more5kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num)
    elif pxls_num > 2:
        std_RF_prf = more1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num)
    elif pxls_num == 2:
        std_RF_prf = equal1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num)
    else:
        std_RF_prf = less1kmcrcs_RF_prfs(crc_ID, prf_ID, prf_dem_pxls, pxls_num)
    return std_RF_prf

