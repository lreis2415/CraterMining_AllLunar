# -*- coding: utf-8 -*-

from pygeoc.raster import RasterUtilClass
import numpy as np
import os

parent_path = os.path.abspath(os.path.dirname(__file__))
original_DEM_folder = parent_path + "\\original_DEM\\"
output_blocks = parent_path + "\\output_blocks\\"

input_tif = original_DEM_folder + "globalDEM.tif"
rst = RasterUtilClass.read_raster(input_tif)
# 120 is because the calculate radius is 120 pixel.
rst_divide_data = np.zeros((rst.nRows + 120 * 2, rst.nCols + 120 *2))

center_col = int(rst.nCols/2)

# 20 is because I find there is around 20 pixels overlap between left and right border from original DEM.
left_top_corner = np.flip(rst.data[:120, center_col-140:center_col-20], 0)
left_bottom_corner = np.flip(rst.data[-120:, center_col-140:center_col-20], 0)
left_border = np.concatenate((left_top_corner, rst.data[:, -140:-20], left_bottom_corner), axis = 0)

right_top_corner = np.flip(rst.data[:120, center_col+20:center_col+140], 0)
right_bottom_corner = np.flip(rst.data[-120:, center_col+20:center_col+140], 0)
right_border = np.concatenate((right_top_corner, rst.data[:, 20:140], right_bottom_corner), axis = 0)

top_border = np.concatenate((np.flip(rst.data[:120, -center_col-1:], 0), np.flip(rst.data[:120, :center_col], 0)), axis = 1)
bottom_border = np.concatenate((np.flip(rst.data[-120:, -center_col-1:], 0), np.flip(rst.data[-120:, :center_col], 0)), axis = 1)

rst_divide_data[:, :120] = left_border
rst_divide_data[:, -120:] = right_border
rst_divide_data[:120, 120:-120] = top_border
rst_divide_data[-120:, 120:-120] = bottom_border
rst_divide_data[120:-120, 120:-120] = rst.data


new_geotrans = (rst.geotrans[0]-120*rst.geotrans[1], rst.geotrans[1], rst.geotrans[2], rst.geotrans[3]-120*rst.geotrans[5], rst.geotrans[4], rst.geotrans[5])

# Original data is 10917(row) * 21853(col)
# 10917 = 3 * 3 *1213
# 21853 = 13 * 41 * 41
# Therefore every block is 120*2 + 1213(row) * (120 *2 + 41 * 41)(col), totally 9(row num) * 13(col num) = 117 blocks

for i in range(9):
    for j in range(13):
        block_data = rst_divide_data[(i*1213):((i+1)*1213+240), (j*1681):((j+1)*1681+240)]
        new_block_geotrans = (new_geotrans[0]+j*1681*new_geotrans[1], new_geotrans[1], new_geotrans[2],
                                new_geotrans[3]+i*1213*new_geotrans[5], new_geotrans[4], new_geotrans[5])
        new_block_tif = output_blocks + "blockR" + str(i) + "C" + str(j) + ".tif"
        RasterUtilClass.write_gtiff_file(new_block_tif, 1213+240, 1681+240, block_data, new_block_geotrans,
                                     rst.srs, rst.noDataValue, rst.dataType)