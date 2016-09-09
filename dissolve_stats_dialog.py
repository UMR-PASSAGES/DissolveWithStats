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

from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
from ui_dissolve_stats import Ui_DissolveWithStats
import os.path
import processing
import sys
import time
import math


# the stats which can be calculated for numeric fields
statNum = ["Count", "First", "Last", "Max", "Mean", "Median", "Min", "Standard deviation", "Sum"]
# the stats which can be calculated for non numeric fields
statElse = ["Count", "Concatenation", "First", "Last", "Uniquification"]


# create the dialog
class DissolveWithStatsDialog(QtGui.QDialog, Ui_DissolveWithStats):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        self.iface = iface
        # Set up the user interface from Designer.
        self.ui = Ui_DissolveWithStats()
        self.ui.setupUi(self)
        
        # connect changed index signal in comboLayerList
        self.ui.comboLayerList.currentIndexChanged[int].connect(self.onChangedValueLayer)
        # connect changed index signal in comboFieldList
        self.ui.comboFieldList.currentIndexChanged[int].connect(self.onChangedValueField)
        # connect click on browse button, to display file dialog for output shapefile
        self.ui.outButton.clicked.connect(self.outFile)
        # connect OK button to validation function
        self.ui.buttonBox.accepted.connect(self.validation)
        # connect Cancel button to reject function
        self.ui.buttonBox.rejected.connect(self.reject)

        # to get all the vector layers names to populate combo box comboLayerList
        legendInterface = self.iface.legendInterface()
        listLayerName = [i.name() for i in legendInterface.layers() if i.type() == QgsMapLayer.VectorLayer]
        # add all these layer names to combo box comboLayerList
        self.ui.comboLayerList.addItems(listLayerName)
        
        # populate the field table header
        listHeaders = ["name", "type", "keep", "stat"]
        self.ui.tableFields.setHorizontalHeaderLabels(listHeaders)
        # set column widths for field table
        self.ui.tableFields.setColumnWidth(0,120)
        self.ui.tableFields.setColumnWidth(1,80)
        self.ui.tableFields.setColumnWidth(2,80)
        self.ui.tableFields.setColumnWidth(3,100)
        
        # Run the dialog event loop
        result = self.exec_()
        # if Cancel was pressed
        if result == QtGui.QFileDialog.Rejected:
            return
        # If OK was pressed
        if result == QtGui.QFileDialog.Accepted:
#            try:
            # get selected layer in combo box comboLayerList
            selectedLayerName = self.ui.comboLayerList.currentText()
            # get selected field in combo box comboFieldList
            selectedFieldName = self.ui.comboFieldList.currentText()
            # get fields to keep and stats to calculate
            listKeep = []
            listStats = []
            for row in range(self.ui.tableFields.rowCount()):
                listKeep.append(self.ui.tableFields.cellWidget(row, 2).checkState())
                listStats.append(self.ui.tableFields.cellWidget(row,3).currentText())
            # get output shape
            output = self.ui.outShape.text()
            # run qgis:dissolve algorithm from processing module
            processing.runalg("qgis:dissolve", selectedLayerName, "false", selectedFieldName, output)
            # calculate new field values
            listRes = self.calculateFields(listKeep, listStats, output)
            # integrates these new values in the output attribute table, and remove fields if necessary
            self.setAttributes(listRes, listKeep, output)
            # add layer to map if checkBoxAddFile is checked
            if self.ui.checkBoxAddFile.checkState() == 2:
                self.addFile(output)
#            except:
#                QtGui.QMessageBox.warning(self, 'Oops', 'Sorry, something went wrong', QtGui.QMessageBox.Ok)


    # check if all the dialog parameters are valid
    def validation(self):
        message = ''
        # get list of kept fields
        if self.ui.comboLayerList.currentText() != '':
            listKeep = []
            for row in range(self.ui.tableFields.rowCount()):
                listKeep.append(self.ui.tableFields.cellWidget(row, 2).checkState())
        # get selected layer, to test self.ui.outShape.text()
        if self.ui.comboLayerList.currentText() != '':
            index = self.ui.comboLayerList.currentIndex()
            legendInterface = self.iface.legendInterface()
            listLayers = [layer for layer in legendInterface.layers() if layer.type() == QgsMapLayer.VectorLayer]
            selectedLayer = listLayers[index]
            outfile = QgsVectorFileWriter(self.ui.outShape.text(), "utf-8", selectedLayer.dataProvider().fields(), selectedLayer.dataProvider().geometryType(), selectedLayer.crs())
        # if no layer is selected :
        if self.ui.comboLayerList.currentText() == '':
            message = 'No layer selected\nQGIS must have at least one vector layer loaded'
        # if a layer is selected but doesn't have any field
        elif self.ui.comboFieldList.currentText() == '':
            message = 'No Field selected\nThe selected layer must have at least one field'
        # if layer and dissolve field ok, but no fields are checked to be kept
        elif 2 not in listKeep:
            message = 'Please select at least one field to be kept'
        # if no output is selected:
        elif self.ui.outShape.text() == '':
            message = 'No output layer\nPlease click on Browse button to specify output layer'
        # if error in output shapefile path (permission problem for example)
        elif (outfile.hasError() != QgsVectorFileWriter.NoError):
            message = "Sorry, could not create output shapefile"
        # if output does not end in .shp (can happen if user wrote it directly in the QLineEdit box)
        elif self.ui.outShape.text()[-4:] not in ['.shp', '.SHP']:
            self.ui.outShape.setText(self.ui.outShape.text() + '.shp')
        # if something is wrong : show warning message
        if message != '':
            QtGui.QMessageBox.warning(self, 'Information missing or invalid', message, QtGui.QMessageBox.Ok)
        # if everything is ok : proceed
        else:
            self.accept()

        
    # if selected value in comboLayerList changes :
    # actualize the values in comboFieldList and in tableFields
    def onChangedValueLayer(self, index):
        # get list of all vector layers in QGIS
        legendInterface = self.iface.legendInterface()
        listLayers = [layer for layer in legendInterface.layers() if layer.type() == QgsMapLayer.VectorLayer]
        # get name of selected layer
        provider = listLayers[index].dataProvider()
        fields = provider.fields()
        listFieldNames = [field.name() for field in fields]
        # clear the combo box comboFieldList
        self.ui.comboFieldList.clear()
        # add all these field names to combo box comboFieldList
        self.ui.comboFieldList.addItems(listFieldNames)
        # add as many rows in the field table as fields in the shape, minus one
        self.ui.tableFields.setRowCount(len(fields))
        # populate columns in field table
        for i in range (self.ui.tableFields.rowCount()):
            # first column : field names
            nameitem = QtGui.QTableWidgetItem(fields[i].name())
            # the names are not editable
            nameitem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.ui.tableFields.setItem(i, 0, nameitem)
            # second column : field types
            typeitem = QtGui.QTableWidgetItem(fields[i].typeName())
            # the types are not editable
            typeitem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.ui.tableFields.setItem(i, 1, typeitem)
            # third column : check box
            keepcheckbox = QtGui.QCheckBox()
            keepcheckbox.setCheckState(QtCore.Qt.Checked)
            keepitem = self.ui.tableFields.setCellWidget(i, 2, keepcheckbox)
            # fourth column : stat
            listStat = QtGui.QComboBox()
            # if field is numeric (works also for PostGIS data, fix by DelazJ, and for int64 and double, fix by A. Ferraton)
            if fields[i].type() in [QtCore.QVariant.Int, QtCore.QVariant.Double, 2, 4, 6]:
                listStat.addItems(statNum)
            # if field is not numeric
            else:
                listStat.addItems(statElse)
            statitem = self.ui.tableFields.setCellWidget(i, 3, listStat)
            # enable all field lists
            self.ui.tableFields.cellWidget(i, 3).setEnabled(True)
        # disable list for first field (since it is selected by default when a new layer is selected)
        self.ui.tableFields.cellWidget(0, 3).setEnabled(False)
            
        
    # if selected value in comboFieldList changes :
    # re-enable the stats list for ex-selected value, disable it for selected value
    def onChangedValueField(self, index):
        if self.ui.tableFields.cellWidget(index, 3):
            # enable all field lists
            for i in range (self.ui.tableFields.rowCount()):
                self.ui.tableFields.cellWidget(i, 3).setEnabled(True)
            # disable current field list
            self.ui.tableFields.cellWidget(index, 3).setEnabled(False)
            
            
    # creation of the output shapefile
    def outFile(self): # by Carson Farmer 2008
        # display file dialog for output shapefile
        self.ui.outShape.clear()
        fileDialog = QtGui.QFileDialog()
        fileDialog.setConfirmOverwrite(False)
        outName = fileDialog.getSaveFileName(self, "Output Shapefile",".", "Shapefiles (*.shp)")
        outPath = QtCore.QFileInfo(outName).absoluteFilePath()
        if not outPath.upper().endswith(".SHP"):
            outPath = outPath + ".shp"
        if outName:
            self.ui.outShape.clear()
            self.ui.outShape.insert(outPath)
            
    # gets the median from a list of numbers
    def median(self, l):
        # sorts list, get list length
        l.sort()
        z = len(l)
        # if the list has an uneven number of elements
        if z%2:
            return l[z/2]
        # if the list has an even number of elements
        else:
            return (l[(z/2)-1] + l[z/2]) / 2.0
            
    # gets standard deviation from a list of numbers
    def standard_dev(self, l):
        mean = sum(l) / len(l)
        dev = [(x - mean)*(x - mean) for x in l]
        return math.sqrt(sum(dev) / len(l))
     
            
    # once the dissolve output layer is created, calculates its new attributes values
    def calculateFields(self, listKeep, listStats, output):
        # get selected layer
        index = self.ui.comboLayerList.currentIndex()
        legendInterface = self.iface.legendInterface()
        listLayers = [layer for layer in legendInterface.layers() if layer.type() == QgsMapLayer.VectorLayer]
        selectedLayer = listLayers[index]
        # iterates over layer features to get attributes as a list of lists
        # uses the processing method so as to get only selected features if this option is set in the processing options
        iter = processing.features(selectedLayer)
        attrs = [feature.attributes() for feature in iter]
        # get all values of the dissolve field (before processing : with duplicate values)
        indexDissolveField = self.ui.comboFieldList.currentIndex()
        valuesDissolveField = [feature[indexDissolveField] for feature in attrs]
        # get unique values for dissolve field, from output (seems more secure than to get it from valuesDissolveField ?)
        outputLayer = QgsVectorLayer(output, "name", "ogr")
        provider = outputLayer.dataProvider()
        fields = provider.fields()
        listFieldNames = [field.name() for field in fields]
        iter = outputLayer.getFeatures()
        uniqueValuesDissolveField = [feature.attributes()[indexDissolveField] for feature in iter]
        # initializes list of lists which will contain results (it will have one element per kept field)
        listRes = []
        # trick for dissolve field, if kept
        if listKeep[indexDissolveField] == 2:
            listStats [indexDissolveField] = 'First'
        # for each kept field
        for i in range(len(listFieldNames)):
            if listKeep[i]  == 2:
                # creates list which will contain attribute values for current field, one empty element per unique dissolve field value
                listAttrs = [[] for val in range(len(uniqueValuesDissolveField))]
                # fill this list with all the current field values corresponding to each dissolve field value
                valuesField = [feature[i] for feature in attrs]
                for (x,y) in zip(valuesDissolveField, valuesField):
                    listAttrs[uniqueValuesDissolveField.index(x)].append(y)
                # removes any NULL values
                listAttrs = [[x for x in l if x] for l in listAttrs]
                # for each list in listAttrs, calculates one value according to the chosen stat
                # if list is empty (can happen if it contained originally only NULL values), return NULL as a result
                if listStats[i] == "Mean":
                    listAttrs = [sum(y) / len(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Sum":
                    listAttrs = [sum(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Min":
                    listAttrs = [min(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Max":
                    listAttrs = [max(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Count":
                    listAttrs = [len(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "First":
                    listAttrs = [y[0] if y else NULL for y in listAttrs]
                elif listStats[i] == "Last":
                    listAttrs = [y[-1] if y else NULL for y in listAttrs]
                elif listStats[i] == "Median":
                    listAttrs = [self.median(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Standard deviation":
                    listAttrs = [self.standard_dev(y) if y else NULL for y in listAttrs]
<<<<<<< HEAD
		elif listStats[i] == "Concatenation":
		    listAttrs = [", ".join(y) if y else NULL for y in listAttrs]
		elif listStats[i] == "Uniquification":
		    listAttrs = [", ".join(set(y)) if y else NULL for y in listAttrs]
=======
                elif listStats[i] == "Concatenation":
                    listAttrs = [", ".join(y) if y else NULL for y in listAttrs]
                elif listStats[i] == "Uniquification":
                    listAttrs = [", ".join(set(y)) if y else NULL for y in listAttrs]
>>>>>>> origin/master
                # append each field result to listRes
                listRes.append(listAttrs)
        return listRes


    # removes fields from the output which mustn't be kept, and set the other field values            
    def setAttributes(self, listRes, listKeep, output):
        # get indexes of fields to be deleted
        listIndexesDel = [i for i in range(len(listKeep)) if listKeep[i] == 0]
        # get layer, provider and provider capabilities
        outputLayer = QgsVectorLayer(output, "name", "ogr")
        provider = outputLayer.dataProvider()
        caps = provider.capabilities()
        # delete fields to be deleted
        if caps & QgsVectorDataProvider.DeleteAttributes:
            res = provider.deleteAttributes(listIndexesDel)
            outputLayer.updateFields()
        # changes other fields attribute values
        fields = provider.fields()
        nb_fields = len(fields)
        outputLayer.startEditing()
        for fieldIndex in  range(nb_fields):
            for fid in range(len(listRes[0])):
                outputLayer.changeAttributeValue(fid, fieldIndex, listRes[fieldIndex][fid])
        outputLayer.commitChanges()
        
    
    # add output layer to the map
    def addFile(self, output):
        layerNameSHP = output.split('/')[-1]
        layerName = layerNameSHP.split('.')[0]
        layer = QgsVectorLayer(output, layerName, "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer)



