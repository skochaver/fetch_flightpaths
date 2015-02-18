__author__ = 'skochaver'

import os
import kml_manage
import join_manage
import csv_manage

########################################
'''
This program is designed to organize and execute functions in the associated python files for grabbing AVIRIS flight paths.
This initial block is for the definition of the global variables among and between the functions.
'''

flight_kml_uri = "https://www.google.com/fusiontables/exporttable?query=select+col48+from+2214916+&o=kmllink&g=col48"  # Location of the google fusion table of flight path KMLs.
download_kml_name = 'flight_paths.kml'  # The file name of the kml after it's downloaded
output_gdb_name = 'path_output_gdb'  # The temporary file geodatabase for processing the KML
output_path_shp = 'flight_paths.shp'  # The multipolygon output of flight paths.

excel_file = "Site_Data_Update.xlsx"  # Name of the excel file containing the point data
data_sheet = "Sheet1"  # Name of the sheet within the excel file with the data
output_site_shp = 'site_points.shp'  # Ouput name of the converted point data

out_join = os.path.join(os.getcwd(), "join_point.shp")  # The full path name of the spatially joined data.
#########################################


'''
kml_manage.download_path_kml(download_kml_name, flight_kml_uri)
kml_manage.db_conversion(download_kml_name, output_path_shp, output_gdb_name)

output_csv = csv_manage.xlsx_to_csv(excel_file, data_sheet)
csv_manage.parse_whole_csv(output_csv)
csv_manage.csv_to_shp(output_csv, output_site_shp, "TowerSite")

'''

join_manage.spatial_join(output_site_shp, output_path_shp , out_join)
