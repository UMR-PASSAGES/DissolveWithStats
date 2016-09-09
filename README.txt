"""
/***************************************************************************
 DissolveWithStats
                                 A QGIS plugin
Group geometries using one field, calculate stats on the other fields (mean, sum...)
                              -------------------
        begin                : 2014-22-08
        copyright            : (C) 2016 by J. Pierson, UMR 5319 PASSAGES
        email                : julie.pierson@cnrs.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 
 ------------------
 DESCRIPTION
 ------------------
 
This plugin group geometries, using qgis:dissolve algorithm by Victor Olaya, and in the process calculates statistics on other fields.

Once activated, it is located in the extension toolbar or in the vector menu -> dissolve with stats
 
 
------------------
PARAMETERS
------------------
 
 - Input layer
 A droplit lists all vector layers loaded in QGIS.
 The user must select one layer.
 
 - Dissolve field
 A droplist lists all fields for the selected input layer.
 The user must select one field.
 All the geometries with the same value for this field will be merged together.
 
 - Statistics
A table lists all fields in the input layer, with their name and type.
The user can choose via a checkbox wether to keep a field or not; if not, this field won't be present in the output layer.
At least one field must be kept.
The user can choose for each field, except the dissolve field, which statistic to calculate via a droplist.
For numeric fields, availabe statistics are count, first, last, max, mean, median, min, sum and standard deviation.
For non numeric fields, available statistics are first, last and count.
NULL values will not be taken into account. If there are only NULL values to calculate a statistic from, NULL will be returned as a result.

- Output layer

- Add output layer to map
If this checkbox is checked, the output layer will be loaded in QGIS.


------------------
SOMETHING WRONG ?
------------------

Please send an email to julie.pierson@cnrs.fr !



