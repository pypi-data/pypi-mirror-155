#Project module
from ticsummary.ui import uic as uicFile
from ticsummary import databaseMYSQL as dbMysql
#Third party module
from PyQt6 import QtCore, QtGui, QtWidgets, uic
import numpy as np
#Python module
from pkg_resources import resource_listdir,resource_filename
import logging
from enum import Enum

log = logging.getLogger()
nameList = ('id_Run','DateTime','TimeSliceB1','DelayB1','TimeSliceB2','DelayB2')

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        for i in range(len(nameList)):
            self.setHeaderData(i, QtCore.Qt.Orientation.Horizontal, QtCore.QObject.tr(nameList[i]))

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            #print(self._data[index.row()][self.nameList[index.column()]])
            return str(self._data[index.row()][nameList[index.column()]])
    def headerData(self, section, orientation,role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return nameList[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)
    def getCellIdRun(self,row):
        return self._data[row]['id_Run']
    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class ChooseRecordDialog(QtWidgets.QDialog):
    setIdRecordSignal = QtCore.pyqtSignal(int)
    def __init__(self,parent,model):
        super().__init__(parent)
        log.debug("Init choose record dialog")
        str = resource_filename(uicFile.__name__, "ChooseRecordDialog.ui")
        log.debug(str)
        uic.loadUi(str, self)
        self.model = model
        self.__initSignal__()
        self.__initView__()
    def __initSignal__(self):
        self.pushButtonFiltering.clicked.connect(self.pushButtonFilteringClicked) 
        self.tableViewData.doubleClicked.connect(self.selectRow)
        self.pushButtonOK.clicked.connect(self.pushButtonOKClicked)
        self.spinBoxTo.valueChanged.connect(self.spinBoxToValueChanged)
        self.spinBoxFrom.valueChanged.connect(self.spinBoxFromValueChanged)
        self.dateTimeEditTo.dateTimeChanged.connect(self.dateTimeEditToValueChanged)
        self.dateTimeEditFrom.dateTimeChanged.connect(self.dateTimeEditFromValueChanged)
    def __initView__(self):
        #self.tableViewData.setStretchLastSection(True)
        self.tableViewData.horizontalHeader().setStretchLastSection(True)
        self.tableViewData.horizontalHeader().setCascadingSectionResizes(True)
        self.tableViewData.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.firstLastRecordInfo = dbMysql.getInfoFirstAndLastRecord(self.model.sqlParameters.table,self.model.connector)
        self.dateTimeEditFrom.setMinimumDateTime(self.firstLastRecordInfo["firstDataTime"])
        self.dateTimeEditTo.setMaximumDateTime(self.firstLastRecordInfo["lastDataTime"])
        self.spinBoxTo.setMaximum(self.firstLastRecordInfo["count"])
        self.spinBoxFrom.setMinimum(0)
    def radioButtonNoFilterTriggered(self):
        pass
    def radioButtonFilterDateTimeTriggered(self):
        pass
    def radioButtonFilterIdTriggered(self):
        pass
    def pushButtonFilteringClicked(self):
        if self.radioButtonNoFilter.isChecked():
            data = dbMysql.getRecordsInfoByAll(self.model.sqlParameters.table,self.model.connector)
        if self.radioButtonFilterDateTime.isChecked():
            data = dbMysql.getRecordsInfoByDateTime(self.model.sqlParameters.table,self.model.connector,self.dateTimeEditFrom.dateTime().toPyDateTime(),self.dateTimeEditTo.dateTime().toPyDateTime())
        if self.radioButtonFilterId.isChecked():
            data = dbMysql.getRecordsInfoByFilterID(self.model.sqlParameters.table,self.model.connector,self.spinBoxFrom.value(),self.spinBoxTo.value())
        self.dataModel = TableModel(data)
        self.tableViewData.setModel(self.dataModel)
    def selectRow(self,index):
        self.setIdRecordSignal.emit(self.dataModel.getCellIdRun(index.row()))
    def pushButtonOKClicked(self):
        self.accept()
    def spinBoxFromValueChanged(self,value):
        self.spinBoxTo.setMinimum(value)
    def spinBoxToValueChanged(self,value):
        self.spinBoxFrom.setMaximum(value)
    def dateTimeEditFromValueChanged(self,value):
        self.dateTimeEditTo.setMinimumDateTime(value)
    def dateTimeEditToValueChanged(self,value):
        self.dateTimeEditFrom.setMaximumDateTime(value)
        
        