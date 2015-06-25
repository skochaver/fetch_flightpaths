# fetch_flightpaths
Downloads a KML of flight paths seen here: http://aviris.jpl.nasa.gov/alt_locator/ and compares paths to a site list.
Uses arcpy module.

To use this set of scripts simply download and make sure that they are all in the same directory during execution.
All of the functionality is wrapped up in fetch_runner.py using absolute paths to a list of points in an excel file (usually a site list). This script uses arcpy functions so ArcGIS needs to be on the machine with arcpy in your current Python environment.

All you need to do is change the "excel_file" variable in fetch_runner.py to point to the excel file that has your points (and change the "data_sheet" variable if it is not in Sheet1). The other variables can be changed to avoid name collisions or to keep track of multiple downloads.

Questions? Email: kochaver.python@gmail.com
