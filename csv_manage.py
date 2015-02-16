__author__ = 'skochaver'

import re
import xlrd
import os
import csv
import arcpy
from tempfile import mkstemp
from shutil import move

def xlsx_to_csv(xlsx_file, sheet_name, csv_name=''):
    '''
    Takes a sheet from an xlsx (or xls) excel file and transforms it into a csv format.
    Retention in formatting will result in strange csv output so it is recommended to sterilize your xlsx file
    prior to running this function.
    :param xlsx_file: The file name and file path if not in working directory
    :param sheet_name: The string sheet name from the xlsx. (See xlrd docs for exposing these name)
    :param csv_name: Name and path of target csv. Defaults to empty string to fill with xlsx base name.
    :return: return the name of the resulting csv file
    '''

    # If not defined csv_name default is given xlsx param basename + .csv
    if not csv_name:
        csv_name = os.path.basename(xlsx_file).split('.')[0]+'.csv'

    # Block to open target page using xldr package
    workbook = xlrd.open_workbook(xlsx_file)
    worksheet = workbook.sheet_by_name(sheet_name)
    # Prepare csv writing
    new_csv = open(csv_name, 'wb')
    writer = csv.writer(new_csv, quoting=csv.QUOTE_ALL)

    # Iterate fill target with source xlsx data.
    for row in xrange(worksheet.nrows):
        writer.writerow(worksheet.row_values(row))

    new_csv.close()

    return csv_name


def alpha_string_parse(raw_string):
    '''
    Takes a string and transforms it into an Arc friendly format. No spaces and only alphanum chars.
    :param raw_string: Any string
    :return: String parsed to Arc-friendly criteria
    '''
    # Optimized remove spaces.
    raw_string = "".join(raw_string.split())
    # Optimized remove non-alphanum
    raw_string = re.compile('[\W_]+').sub('', raw_string)

    return raw_string


def parse_whole_csv(csv_file):
    '''
    Creates a temporary file of the csv in question, does all the parsing to the first row and first column of the
    file (field and record names) through alpha_string_parse, and replaces the target file with the temporary one.
    It's like nothing ever happened. Spooky.
    :param csv_file: The csv file to parse. Makes an abspath call in case the full path isn't included.
    :return:
    '''

    # Sets up the temp file and opens both old and new for reading.
    csv_file = os.path.abspath(csv_file)
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'wb')
    old_file = open(csv_file, 'rb')

    # Creates csv pointers for going through the files.
    reader = csv.reader(old_file)
    writer = csv.writer(new_file)

    # Replaces all the field names with their parsed version in the temp file.
    old_headers = reader.next()
    new_headers = [alpha_string_parse(str(header)) for header in old_headers]
    writer.writerow(new_headers)

    # Goes through the remaining rows and parses the first item (record labels).
    for row in reader:
        row[0] = alpha_string_parse(row[0])
        writer.writerow(row)

    # Close all the files. Delete the old csv and move the new temporary csv to take it's place.
    new_file.close()
    os.close(fh)
    old_file.close()
    os.remove(csv_file)
    move(abs_path, csv_file)

    return


def csv_to_shp(csv_path, out_name, label, x_label='lon', y_label='lat'):
    '''
    Changes a csv file to a shape file if given a valid x and y parameter and an identifying label.
    :param csv_path: The path to the source csv file
    :param out_name: The name of the target .shp file. It will be put in the current working directory
    :param label: CSV column name, as a string, that has the label for the point.
    :param x_label: The column name that contains the X data (defaults to 'lon')
    :param y_label: The column name that contains the Y data (defaults to 'lat')
    :return: Returns the absolute path of the output shapefile. Just in case you care about that.
    '''
    # Default spatial reference in the new shapefile.
    sr = arcpy.SpatialReference().factoryCode = 4326
    # Try Except block to check if the out shapefile already exists by name. Will terminate if it does.
    try:
        arcpy.CreateFeatureclass_management(os.getcwd(), out_name, 'Point', None, None, None, sr)
    except:
       print 'Shape file already exists'
       exit()

    # Adds label field to empty feature table. Creates cursor to populate table.
    arcpy.AddField_management(out_name, 'label', 'TEXT')
    cursor = arcpy.InsertCursor(out_name)

    # Open the csv file to read data and plug into our new feature table.
    with open(csv_path, 'rb') as data:
        reader = csv.DictReader(data)
        for row in reader:

            feature = cursor.newRow()
            # Populate the point data with from our csv. Create point then add label.
            point = arcpy.CreateObject('Point')
            point.X = row[x_label]
            point.Y = row[y_label]
            feature.shape = point
            feature.label = row[label]
            cursor.insertRow(feature)
    # Clean up cursor.
    del cursor

    return os.path.abspath(out_name)