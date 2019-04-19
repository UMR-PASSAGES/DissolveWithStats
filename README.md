# Dissolve with stats

## What is it ?
A QGIS 3 plugin that group geometries using one field, and calculate statistics (mean, sum...) on the other fields. This script was created by [Julie Pierson](https://github.com/juliepierson), with help from [DelazJ](https://github.com/DelazJ), [Ferraton](https://github.com/FERRATON) and [Manuel A. Ureña-Cámara](https://github.com/maurena).

## What is it for ?
This plugin is useful if you want to group geometries which have the same attribute value for one field as well as calculate statistics on the other fields.
It is therefore an ameliorated version of the vector geoprocessing tool "Dissolve" upon which it is based.

For each field other than the one used to group geometries, you can choose a statistic to calculate.

For example, if you have a polygon layer corresponding to small administrative units, with 2 fields :
* one for the bigger administrative units code
* one for the population
You can create another polygon layer corresponding to the bigger administrative units, with the sum of the population for each of these units.

Statistics available for numeric fields :
* count
* first
* last
* min
* max
* sum
* mean
* median
* standard deviation

Statistics available for text fields :
* count
* first
* last
* concatenation
* uniquification (same as concatenation but only concatenates unique values, no duplicates)


## How to use it ?

Install this plugin in QGIS : Plugin menu, Install/manage plugins (you will need an internet connection for this).
Dissolve with stats will then be available in the plugin toolbar or menu.

This extension takes 4 parameters :

**Input layer**

A vector layer, point, line or polygon. Tested formats : shapefile, GeoPackage, PostGIS layer.
Layer must be loaded in QGIS.

**Dissolve field**

Choose a field from the input layer. All entities with the same value for this field will be merged together.

**Field statistics**

For each field other than the dissolve field, you can choose wether to keep it or not. If you keep it, you can chose a statistic to be calculated on this field (see above for available statistics).
Note that if the input layer is a geopackage, choosing a statistic for the fid field will have no effect as this is a field automatically populated by QGIS.

**Output layer**

Choose where to the output layer path and name by clicking on the ... button on the right.
2 formats available : GeoPackage and shapefile.



