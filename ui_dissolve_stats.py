# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dissolve_stats.ui'
#
# Created: Thu Aug 28 13:10:26 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DissolveWithStats(object):
    def setupUi(self, DissolveWithStats):
        DissolveWithStats.setObjectName(_fromUtf8("DissolveWithStats"))
        DissolveWithStats.resize(468, 548)
        self.labelLayerList = QtGui.QLabel(DissolveWithStats)
        self.labelLayerList.setGeometry(QtCore.QRect(30, 20, 211, 17))
        self.labelLayerList.setObjectName(_fromUtf8("labelLayerList"))
        self.labelFieldList = QtGui.QLabel(DissolveWithStats)
        self.labelFieldList.setGeometry(QtCore.QRect(30, 100, 211, 17))
        self.labelFieldList.setObjectName(_fromUtf8("labelFieldList"))
        self.comboLayerList = QtGui.QComboBox(DissolveWithStats)
        self.comboLayerList.setGeometry(QtCore.QRect(30, 50, 401, 27))
        self.comboLayerList.setObjectName(_fromUtf8("comboLayerList"))
        self.comboFieldList = QtGui.QComboBox(DissolveWithStats)
        self.comboFieldList.setGeometry(QtCore.QRect(30, 130, 401, 27))
        self.comboFieldList.setEditable(False)
        self.comboFieldList.setObjectName(_fromUtf8("comboFieldList"))
        self.buttonBox = QtGui.QDialogButtonBox(DissolveWithStats)
        self.buttonBox.setGeometry(QtCore.QRect(260, 500, 176, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.outButton = QtGui.QToolButton(DissolveWithStats)
        self.outButton.setGeometry(QtCore.QRect(340, 450, 91, 25))
        self.outButton.setObjectName(_fromUtf8("outButton"))
        self.outShape = QtGui.QLineEdit(DissolveWithStats)
        self.outShape.setEnabled(True)
        self.outShape.setGeometry(QtCore.QRect(30, 450, 291, 27))
        self.outShape.setObjectName(_fromUtf8("outShape"))
        self.labelOutput = QtGui.QLabel(DissolveWithStats)
        self.labelOutput.setGeometry(QtCore.QRect(30, 420, 211, 17))
        self.labelOutput.setObjectName(_fromUtf8("labelOutput"))
        self.labelFieldTable = QtGui.QLabel(DissolveWithStats)
        self.labelFieldTable.setGeometry(QtCore.QRect(30, 180, 261, 17))
        self.labelFieldTable.setObjectName(_fromUtf8("labelFieldTable"))
        self.tableFields = QtGui.QTableWidget(DissolveWithStats)
        self.tableFields.setGeometry(QtCore.QRect(30, 210, 401, 192))
        self.tableFields.setRowCount(0)
        self.tableFields.setColumnCount(4)
        self.tableFields.setObjectName(_fromUtf8("tableFields"))
        self.checkBoxAddFile = QtGui.QCheckBox(DissolveWithStats)
        self.checkBoxAddFile.setGeometry(QtCore.QRect(30, 500, 221, 22))
        self.checkBoxAddFile.setChecked(True)
        self.checkBoxAddFile.setObjectName(_fromUtf8("checkBoxAddFile"))

        self.retranslateUi(DissolveWithStats)
        self.comboFieldList.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(DissolveWithStats)

    def retranslateUi(self, DissolveWithStats):
        DissolveWithStats.setWindowTitle(QtGui.QApplication.translate("DissolveWithStats", "Dissolve with stats", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLayerList.setToolTip(QtGui.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Choose a layer to dissolve</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLayerList.setText(QtGui.QApplication.translate("DissolveWithStats", "Choose a layer to dissolve :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFieldList.setToolTip(QtGui.QApplication.translate("DissolveWithStats", "<html><head/><body><p>All the geometries with the same value for this field will be merged together</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFieldList.setText(QtGui.QApplication.translate("DissolveWithStats", "Choose a dissolve field :", None, QtGui.QApplication.UnicodeUTF8))
        self.outButton.setText(QtGui.QApplication.translate("DissolveWithStats", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutput.setToolTip(QtGui.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Click on Browse button to specify output layer</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutput.setText(QtGui.QApplication.translate("DissolveWithStats", "Create output layer :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFieldTable.setToolTip(QtGui.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Choose which fields will be present in the output layer, and which statistic to calculate</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFieldTable.setText(QtGui.QApplication.translate("DissolveWithStats", "Calculate statistics on other fields :", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAddFile.setToolTip(QtGui.QApplication.translate("DissolveWithStats", "<html><head/><body><p>Uncheck this if you do not want the output layer to be loaded in QGIS</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAddFile.setText(QtGui.QApplication.translate("DissolveWithStats", "Add output layer to the map", None, QtGui.QApplication.UnicodeUTF8))

