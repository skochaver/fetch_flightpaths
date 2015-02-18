__author__ = 'skochaver'
import os
import arcpy


def spatial_join(input_points, path_poly, out_name):
    field_mapping = "label \"label\" true true false 254 Text 0 0 ,First,#,site_points,label,-1,-1;Name \"Name\" true true false 254 Text 0 0 ,First,#,flight_paths,Name,-1,-1"
    arcpy.SpatialJoin_analysis(input_points, path_poly, out_name, "JOIN_ONE_TO_MANY", "KEEP_ALL", "", "WITHIN", "", "")
    return os.path.abspath(out_name)


