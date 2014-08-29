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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
import dissolve_stats_dialog
import os.path



######################
# Variable declaration
######################




######################
# Class DissolveWithStats
######################

class DissolveWithStats:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/DissolveWithStats/dissolve_stats.png"), \
            "Dissolve with stats", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu("&Dissolve with stats", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginVectorMenu("&Dissolve with stats",self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):

        # create and show the dialog
        self.dlg = dissolve_stats_dialog.DissolveWithStatsDialog(self.iface)
     
        
 
        

