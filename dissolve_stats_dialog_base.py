# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dissolve_stats_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DissolveWithStatsDialogBase(object):
    def setupUi(self, DissolveWithStatsDialogBase):
        DissolveWithStatsDialogBase.setObjectName(_fromUtf8("DissolveWithStatsDialogBase"))
        DissolveWithStatsDialogBase.resize(471, 450)
        self.gridLayout = QtGui.QGridLayout(DissolveWithStatsDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelFieldStatistics = QtGui.QLabel(DissolveWithStatsDialogBase)
        self.labelFieldStatistics.setObjectName(_fromUtf8("labelFieldStatistics"))
        self.gridLayout.addWidget(self.labelFieldStatistics, 4, 0, 1, 1)
        self.outLayerName = QtGui.QLineEdit(DissolveWithStatsDialogBase)
        self.outLayerName.setEnabled(True)
        self.outLayerName.setReadOnly(True)
        self.outLayerName.setClearButtonEnabled(False)
        self.outLayerName.setObjectName(_fromUtf8("outLayerName"))
        self.gridLayout.addWidget(self.outLayerName, 8, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(DissolveWithStatsDialogBase)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(DissolveWithStatsDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 2)
        self.labelInputLayer = QtGui.QLabel(DissolveWithStatsDialogBase)
        self.labelInputLayer.setObjectName(_fromUtf8("labelInputLayer"))
        self.gridLayout.addWidget(self.labelInputLayer, 0, 0, 1, 1)
        self.labelOutputLayer = QtGui.QLabel(DissolveWithStatsDialogBase)
        self.labelOutputLayer.setObjectName(_fromUtf8("labelOutputLayer"))
        self.gridLayout.addWidget(self.labelOutputLayer, 6, 0, 1, 1)
        self.labelDissolveField = QtGui.QLabel(DissolveWithStatsDialogBase)
        self.labelDissolveField.setObjectName(_fromUtf8("labelDissolveField"))
        self.gridLayout.addWidget(self.labelDissolveField, 2, 0, 1, 1)
        self.mFieldComboBox = QgsFieldComboBox(DissolveWithStatsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mFieldComboBox.sizePolicy().hasHeightForWidth())
        self.mFieldComboBox.setSizePolicy(sizePolicy)
        self.mFieldComboBox.setObjectName(_fromUtf8("mFieldComboBox"))
        self.gridLayout.addWidget(self.mFieldComboBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 9, 1, 1, 1)
        self.outButton = QtGui.QToolButton(DissolveWithStatsDialogBase)
        self.outButton.setObjectName(_fromUtf8("outButton"))
        self.gridLayout.addWidget(self.outButton, 8, 1, 1, 1)
        self.mMapLayerComboBox = QgsMapLayerComboBox(DissolveWithStatsDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mMapLayerComboBox.sizePolicy().hasHeightForWidth())
        self.mMapLayerComboBox.setSizePolicy(sizePolicy)
        self.mMapLayerComboBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.mMapLayerComboBox.setObjectName(_fromUtf8("mMapLayerComboBox"))
        self.gridLayout.addWidget(self.mMapLayerComboBox, 1, 0, 1, 2)

        self.retranslateUi(DissolveWithStatsDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DissolveWithStatsDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DissolveWithStatsDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(DissolveWithStatsDialogBase)

    def retranslateUi(self, DissolveWithStatsDialogBase):
        DissolveWithStatsDialogBase.setWindowTitle(_translate("DissolveWithStatsDialogBase", "Dissolve with stats", None))
        self.labelFieldStatistics.setText(_translate("DissolveWithStatsDialogBase", "Field statistics", None))
        self.labelInputLayer.setText(_translate("DissolveWithStatsDialogBase", "Input layer", None))
        self.labelOutputLayer.setText(_translate("DissolveWithStatsDialogBase", "Output layer", None))
        self.labelDissolveField.setText(_translate("DissolveWithStatsDialogBase", "Dissolve field", None))
        self.outButton.setText(_translate("DissolveWithStatsDialogBase", "...", None))

from qgsfieldcombobox import QgsFieldComboBox
from qgsmaplayercombobox import QgsMapLayerComboBox
