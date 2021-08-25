# coding=utf-8

import numpy as np
import os
from osgeo import ogr, osr, gdal
import csv
import CoordsTrans 

parentparent_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
parent_path = os.path.abspath(os.path.dirname(__file__))
allLunar_DBSCANclusters_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\allLunar_DBSCANclusters\\"
border_processing_folder = parentparent_path + "\\02_Step2345_CraterCandidatesGrids\\border_processing\\"
crcsshp_folder = parent_path + "\\crcs_shp\\"

origin_DbscanFileName = allLunar_DBSCANclusters_folder + "All_Lunar_CratersCandidates_DBScan_sc.tif"
border_DbscanFileName = border_processing_folder + "Border_CratersCandidates_DBScan_sc.tif"
origin_CrtCnds_xys_file = border_processing_folder + "origin_CrtCnds_xy_ranges.csv"
border_CrtCnds_xys_file = border_processing_folder + "border_CrtCnds_xy_ranges.csv"

def clusters_grds2pnts(origin_DbscanFileName, border_DbscanFileName, origin_CrtCnds_xys_file, border_CrtCnds_xys_file, crcsshp_folder):
    ##
    origin_Dbscan = gdal.Open(origin_DbscanFileName)
    origin_Dbscan_band = origin_Dbscan.GetRasterBand(1)
    origin_Dbscan_data = origin_Dbscan_band.ReadAsArray()
    origin_Dbscan_nRows = origin_Dbscan.RasterYSize
    origin_Dbscan_nCols = origin_Dbscan.RasterXSize
    #
    border_Dbscan = gdal.Open(border_DbscanFileName)
    border_Dbscan_band = border_Dbscan.GetRasterBand(1)
    border_Dbscan_data = border_Dbscan_band.ReadAsArray()
    border_Dbscan_nRows = border_Dbscan.RasterYSize
    border_Dbscan_nCols = border_Dbscan.RasterXSize
    #
    origin_CrtCnds_xys_csv = csv.reader(open(origin_CrtCnds_xys_file))
    origin_CrtCnds_xys_range = np.array(list(origin_CrtCnds_xys_csv))
    origin_CrtCnds_xys_range = (origin_CrtCnds_xys_range[1:,:]).astype(np.int)
    #
    border_CrtCnds_xys_csv = csv.reader(open(border_CrtCnds_xys_file))
    border_CrtCnds_xys_range = np.array(list(border_CrtCnds_xys_csv))
    border_CrtCnds_xys_range = (border_CrtCnds_xys_range[1:,:]).astype(np.int)
    ##
    Dbscan_prosrs, Dbscan_geosrs = CoordsTrans.getSRSPair(origin_Dbscan)
    Dbscan_ct = osr.CoordinateTransformation(Dbscan_prosrs, Dbscan_geosrs)
    Dbscan_trans = origin_Dbscan.GetGeoTransform()
    #
    N_srs = osr.SpatialReference()
    N_srs.ImportFromWkt('PROJCS["Moon_North_Pole_Stereographic",GEOGCS["Moon 2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Stereographic"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",90],UNIT["Meter",1]]')
    print(N_srs)
    Nsrs_ct = osr.CoordinateTransformation(Dbscan_geosrs, N_srs)
    #
    S_srs = osr.SpatialReference()
    S_srs.ImportFromWkt('PROJCS["Moon_South_Pole_Stereographic",GEOGCS["Moon 2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Stereographic"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-90],UNIT["Meter",1]]')
    print(S_srs)
    Ssrs_ct = osr.CoordinateTransformation(Dbscan_geosrs, S_srs)
    ###
    ##
    # no border North, 1000 clusters one shp file, 60 shp files.
    for start_ID in range(0, 60000, 1000):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        shp_file =  crcsshp_folder + "CrtCnds_" + str(start_ID+999) + "_pnts.shp"
        shp_layer_name = "CrtCnds_" + str(start_ID+999) + "_pnts"
        data_source = driver.CreateDataSource(shp_file)
        layer = data_source.CreateLayer(shp_layer_name,N_srs,ogr.wkbPoint)
        layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger64))
        layer.CreateField(ogr.FieldDefn("longitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("latitude", ogr.OFTReal))
        for i in range(start_ID, start_ID+1000):
            ID = int(origin_CrtCnds_xys_range[i, 0])
            temp_coords = [] 
            N_pnts_coords = [] 
            min_row = origin_CrtCnds_xys_range[i, 2]
            max_row = origin_CrtCnds_xys_range[i, 1]
            min_col = origin_CrtCnds_xys_range[i, 4]
            max_col = origin_CrtCnds_xys_range[i, 3]
            for i in range(min_row, max_row+1):
                for j in range(min_col, max_col+1):
                    if int(origin_Dbscan_data[i,j]) == ID:
                        Dbscan_projcoords = CoordsTrans.imagexy2geo(Dbscan_trans, i, j) 
                        geocoords = CoordsTrans.geo2lonlat(Dbscan_ct, Dbscan_projcoords[0], Dbscan_projcoords[1]) 
                        N_projcoords = CoordsTrans.lonlat2geo(Nsrs_ct, geocoords[0], geocoords[1]) 
                        N_pnts_coords.append([N_projcoords[0], N_projcoords[1]])
                        temp_coords.append([geocoords[0], geocoords[1]])
            for point in range(len(N_pnts_coords)):
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField("longitude", temp_coords[point][0])
                feature.SetField("latitude", temp_coords[point][1])
                feature.SetField("ID", ID)
                wkt = "POINT(%f %f)" % (float(N_pnts_coords[point][0]), float(N_pnts_coords[point][1]))
                shp_point = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(shp_point)
                layer.CreateFeature(feature)
                feature = None
        data_source = None
    ###
    ##
    # no border South, 1000 clusters one shp file, 24 files
    for start_ID in range(60000, 84000, 1000):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        shp_file =  crcsshp_folder + "CrtCnds_" + str(start_ID+999) + "_pnts.shp"
        shp_layer_name = "CrtCnds_" + str(start_ID+999) + "_pnts"
        data_source = driver.CreateDataSource(shp_file)
        layer = data_source.CreateLayer(shp_layer_name,S_srs,ogr.wkbPoint)
        layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger64))
        layer.CreateField(ogr.FieldDefn("longitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("latitude", ogr.OFTReal))
        for i in range(start_ID, start_ID+1000):
            ID = int(origin_CrtCnds_xys_range[i, 0])
            temp_coords = [] 
            S_pnts_coords = [] 
            min_row = origin_CrtCnds_xys_range[i, 2]
            max_row = origin_CrtCnds_xys_range[i, 1]
            min_col = origin_CrtCnds_xys_range[i, 4]
            max_col = origin_CrtCnds_xys_range[i, 3]
            for i in range(min_row, max_row+1):
                for j in range(min_col, max_col+1):
                    if int(origin_Dbscan_data[i,j]) == ID:
                        Dbscan_projcoords = CoordsTrans.imagexy2geo(Dbscan_trans, i, j) 
                        geocoords = CoordsTrans.geo2lonlat(Dbscan_ct, Dbscan_projcoords[0], Dbscan_projcoords[1]) 
                        S_projcoords = CoordsTrans.lonlat2geo(Ssrs_ct, geocoords[0], geocoords[1]) 
                        S_pnts_coords.append([S_projcoords[0], S_projcoords[1]])
                        temp_coords.append([geocoords[0], geocoords[1]])
            for point in range(len(S_pnts_coords)):
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField("longitude", temp_coords[point][0])
                feature.SetField("latitude", temp_coords[point][1])
                feature.SetField("ID", ID)
                wkt = "POINT(%f %f)" % (float(S_pnts_coords[point][0]), float(S_pnts_coords[point][1]))
                shp_point = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(shp_point)
                layer.CreateFeature(feature)
                feature = None
        data_source = None
    ###
    ##
    # no border Southest, one shp file
    max_ID = origin_Dbscan_data.max()
    start_ID = 84000
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp_file =  crcsshp_folder + "CrtCnds_" + str(max_ID) + "_pnts.shp"
    shp_layer_name = "CrtCnds_" + str(max_ID) + "_pnts"
    data_source = driver.CreateDataSource(shp_file)
    layer = data_source.CreateLayer(shp_layer_name, S_srs, ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn("longitude", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("latitude", ogr.OFTReal))
    for i in range(start_ID, len(origin_CrtCnds_xys_range)):
        ID = int(origin_CrtCnds_xys_range[i, 0])
        temp_coords = [] 
        S_pnts_coords = [] 
        min_row = origin_CrtCnds_xys_range[i, 2]
        max_row = origin_CrtCnds_xys_range[i, 1]
        min_col = origin_CrtCnds_xys_range[i, 4]
        max_col = origin_CrtCnds_xys_range[i, 3]
        for i in range(min_row, max_row+1):
            for j in range(min_col, max_col+1):
                if int(origin_Dbscan_data[i,j]) == ID:
                    Dbscan_projcoords = CoordsTrans.imagexy2geo(Dbscan_trans, i, j) 
                    geocoords = CoordsTrans.geo2lonlat(Dbscan_ct, Dbscan_projcoords[0], Dbscan_projcoords[1]) 
                    S_projcoords = CoordsTrans.lonlat2geo(Ssrs_ct, geocoords[0], geocoords[1]) 
                    S_pnts_coords.append([S_projcoords[0], S_projcoords[1]])
                    temp_coords.append([geocoords[0], geocoords[1]])
        for point in range(len(S_pnts_coords)):
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("longitude", temp_coords[point][0])
            feature.SetField("latitude", temp_coords[point][1])
            feature.SetField("ID", ID)
            wkt = "POINT(%f %f)" % (float(S_pnts_coords[point][0]), float(S_pnts_coords[point][1]))
            shp_point = ogr.CreateGeometryFromWkt(wkt)
            feature.SetGeometry(shp_point)
            layer.CreateFeature(feature)
            feature = None
    data_source = None
    ###
    ##
    # border North, one shp file
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp_file =  crcsshp_folder + "north_border_CrtCnds_pnts.shp"
    shp_layer_name = "north_CrtCnds_pnts"
    data_source = driver.CreateDataSource(shp_file)
    layer = data_source.CreateLayer(shp_layer_name,N_srs,ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn("longitude", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("latitude", ogr.OFTReal))
    for ID in range(100):
        all_ID = ID + 84561 
        temp_coords = [] 
        N_pnts_coords = [] 
        min_row = border_CrtCnds_xys_range[ID, 2]
        max_row = border_CrtCnds_xys_range[ID, 1]
        min_col = border_CrtCnds_xys_range[ID, 4]
        max_col = border_CrtCnds_xys_range[ID, 3]
        for i in range(min_row, max_row+1):
            for j in range(min_col, max_col+1):
                if int(border_Dbscan_data[i,j]) == ID:
                    Dbscan_projcoords = CoordsTrans.imagexy2geo(Dbscan_trans, i, j) 
                    geocoords = CoordsTrans.geo2lonlat(Dbscan_ct, Dbscan_projcoords[0], Dbscan_projcoords[1]) 
                    N_projcoords = CoordsTrans.lonlat2geo(Nsrs_ct, geocoords[0], geocoords[1]) 
                    N_pnts_coords.append([N_projcoords[0], N_projcoords[1]])
                    temp_coords.append([geocoords[0], geocoords[1]])
        for point in range(len(N_pnts_coords)):
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("longitude", temp_coords[point][0])
            feature.SetField("latitude", temp_coords[point][1])
            feature.SetField("ID", all_ID)
            wkt = "POINT(%f %f)" % (float(N_pnts_coords[point][0]), float(N_pnts_coords[point][1]))
            shp_point = ogr.CreateGeometryFromWkt(wkt)
            feature.SetGeometry(shp_point)
            layer.CreateFeature(feature)
            feature = None
    data_source = None
    ###
    ##
    # border South, one shp file
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp_file =  crcsshp_folder + "south_border_CrtCnds_pnts.shp"
    shp_layer_name = "south_CrtCnds_pnts"
    data_source = driver.CreateDataSource(shp_file)
    layer = data_source.CreateLayer(shp_layer_name,S_srs,ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn("longitude", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("latitude", ogr.OFTReal))
    for ID in range(100, len(border_CrtCnds_xys_range)):
        all_ID = ID + 84561 
        temp_coords = [] 
        S_pnts_coords = [] 
        min_row = border_CrtCnds_xys_range[ID, 2]
        max_row = border_CrtCnds_xys_range[ID, 1]
        min_col = border_CrtCnds_xys_range[ID, 4]
        max_col = border_CrtCnds_xys_range[ID, 3]
        for i in range(min_row, max_row+1):
            for j in range(min_col, max_col+1):
                if int(border_Dbscan_data[i,j]) == ID:
                    Dbscan_projcoords = CoordsTrans.imagexy2geo(Dbscan_trans, i, j) 
                    geocoords = CoordsTrans.geo2lonlat(Dbscan_ct, Dbscan_projcoords[0], Dbscan_projcoords[1]) 
                    S_projcoords = CoordsTrans.lonlat2geo(Ssrs_ct, geocoords[0], geocoords[1]) 
                    S_pnts_coords.append([S_projcoords[0], S_projcoords[1]])
                    temp_coords.append([geocoords[0], geocoords[1]])
        for point in range(len(S_pnts_coords)):
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("longitude", temp_coords[point][0])
            feature.SetField("latitude", temp_coords[point][1])
            feature.SetField("ID", all_ID)
            wkt = "POINT(%f %f)" % (float(S_pnts_coords[point][0]), float(S_pnts_coords[point][1]))
            shp_point = ogr.CreateGeometryFromWkt(wkt)
            feature.SetGeometry(shp_point)
            layer.CreateFeature(feature)
            feature = None
    data_source = None
        