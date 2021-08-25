# coding=utf-8

import numpy as np
import os
from osgeo import ogr, osr, gdal
import csv
import CoordsTrans
import arcpy
from arcpy import env

parent_path = os.path.abspath(os.path.dirname(__file__))
def CrtCnds_pnts2objs(parent_path):
    parent_path = os.path.abspath(os.path.dirname(__file__))
    env.workspace = parent_path + "\\crcs_shp"
    for i in range(84):
        CrtCnds = "CrtCnds_" + str(i*1000+999)
        inFeatures = CrtCnds + "_pnts.shp"
        outFeatures = "Crcs_" + CrtCnds + ".shp"
        arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatures, "CIRCLE", "LIST", "ID", "MBG_FIELDS")
    #
    Southest_CrtCnds = "CrtCnds_84560"
    inFeatures = Southest_CrtCnds + "_pnts.shp"
    outFeatures = "Crcs_" + Southest_CrtCnds + ".shp"
    arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatures, "CIRCLE", "LIST", "ID", "MBG_FIELDS")
    #
    NorthBorder_CrtCnds = "north_border_CrtCnds"
    inFeatures = NorthBorder_CrtCnds + "_pnts.shp"
    outFeatures = "Crcs_" + NorthBorder_CrtCnds + ".shp"
    arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatures, "CIRCLE", "LIST", "ID", "MBG_FIELDS")
    #
    SouthBorder_CrtCnds = "south_border_CrtCnds"
    inFeatures = SouthBorder_CrtCnds + "_pnts.shp"
    outFeatures = "Crcs_" + SouthBorder_CrtCnds + ".shp"
    arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatures, "CIRCLE", "LIST", "ID", "MBG_FIELDS")