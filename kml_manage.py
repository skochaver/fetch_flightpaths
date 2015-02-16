import arcpy
import requests
import os


flight_kml_uri = "https://www.google.com/fusiontables/exporttable?query=select+col48+from+2214916+&o=kmllink&g=col48"
download_kml_name = 'flight_paths.kml'
output_gdb_name = 'path_output_gdb'
output_shapefile = 'flight_paths.shp'

keep_shapefile = False

def download_path_kml(download_kml_name, flight_kml_uri):
    '''
    Downloads response data from the given URI; program assumes response will be a KML and fills a file accordingly.
    Mimics data streaming and ends program if there is a bad response from the URI.
    Downloads in 1024 bit blocks and flushes in order to minimize catastrophic fallout if failure occurs.
    :params download_kml_name: The name of the file that will be filled with kml data
    :params flight_kml_uri: The internet location of the google fusion table KML data. Could be any KML data though.
    :return:
    '''

    with open(download_kml_name, 'wb') as handle:

        kml_response = requests.get(flight_kml_uri)
        if not kml_response.ok:
            # The internet has failed us. Truly, it is the end of times.
            exit()
            print "Something went wrong in calling the KML from the web. Check your connection or NASA's google fusion table download"
        for block in kml_response.iter_content(1024):
            if not block:
                break
            handle.write(block)
            handle.flush()
    return os.path.abspath(download_kml_name)

def db_conversion(output_shapefile, path_output_gdb):
    '''
    Converts KML to a database object (this is they way arcpy works). Converts the database object to a shapefile
    using the KML default creation Polygons feature class. Deletes the then-obsolete .gdb for cleanliness.
    :param output_shapefile:
    :return:
    '''

    # Arcpy converts the KML into a feature class called Polygons inside a GDB
    arcpy.KMLToLayer_conversion(download_kml_name, os.getcwd(), output_gdb_name)

    # For ease of use we take the gdb feature class and extract it out to a multipolygon shapefile.
    # The .gdb appears after the KML conversion. Polygons is always(?) the name given to the feature class.
    input_features = os.path.join(os.getcwd(), output_gdb_name + r'.gdb\Polygons')

    # Here is where the conversion takes place. The output is placed in the working directory and renamed.
    arcpy.FeatureClassToShapefile_conversion(input_features, os.getcwd())
    arcpy.Rename_management("Polygons.shp", output_shapefile)

    # Delete the .gdb to keep the environment clean
    arcpy.Delete_management(path_output_gdb+'.gdb')

    return os.path.abspath(output_shapefile)

