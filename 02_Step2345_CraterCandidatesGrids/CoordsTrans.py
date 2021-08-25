# coding=utf-8

from osgeo import ogr, osr, gdal
import numpy as np

def getCT(prosrs, geosrs):
    '''
    得到投影坐标转换大地经纬度坐标信息
    :param prosrs: 栅格数据投影坐标系信息
    :param geosrs: 栅格数据大地坐标系信息
    :return ct: 栅格数据投影坐标转换经纬度信息
    '''
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    return ct

def imagexy2geo(trans, row, col):
    '''
    根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
    :param trans: 栅格数据geotrans信息
    :param row: 像素的行号
    :param col: 像素的列号
    :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
    '''
    px = trans[0] + col * trans[1] + row * trans[2]
    py = trans[3] + col * trans[4] + row * trans[5]
    return px, py

def geo2imagexy(trans, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 投影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    [col, row] = np.linalg.solve(a, b) # 使用numpy的linalg.solve进行二元一次方程的求解
    [row, col] = [int(row), int(col)]
    return row, col

def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs
    
def geo2lonlat(ct, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
    :param ct: 栅格数据投影坐标转换大地经纬度坐标信息
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
    '''
    coords = ct.TransformPoint(x, y)
    return coords[:2]

def lonlat2geo(ct, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]

def proj2proj(ct, x, y):
    '''
    将投影1中的坐标转为投影2中的坐标（具体的投影坐标系由给定数据确定）
    :param ct: 投影1坐标转换投影2坐标信息
    :param x: 投影1坐标x
    :param y: 投影1坐标y
    :return: 投影1坐标(x, y)对应的投影2坐标(x2, y2)
    '''
    coords = ct.TransformPoint(x, y)
    return coords[:2]