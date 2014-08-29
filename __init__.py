"""
/***************************************************************************
 DissolveWithStats
                                 A QGIS plugin
Group geometries using one field, calculate stats on the other fields (mean, sum...)
                              -------------------
        begin                : 2014-22-08
        copyright            : (C) 2014 by J. Pierson, UMR 5185 ADESS
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load DissolveWithStats class from file dissolve_stats
    from dissolve_stats import DissolveWithStats
    return DissolveWithStats(iface)
