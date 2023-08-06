#Project module
from ticsummary.ui import connectionConfigurationDialog
from ticsummary.ui.openSqlDataDialog import OpenSQLData
from ticsummary.ui.viewGraphicsDialog import ViewGraphicsDialog
from ticsummary.ui.profileBeamDock import ProfileBeamDock
from ticsummary.ui.descriptionDataDock import DescriptionDataDock
from ticsummary.ui import uic as uicFile
#Third party module
from PyQt6 import QtCore, QtGui, QtWidgets,uic
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
#Python module
from pkg_resources import resource_listdir,resource_filename
from enum import Enum
import logging
import time

log = logging.getLogger()


class DockAreaWithUncloseableDocks(pg.dockarea.DockArea):
    def makeContainer(self, typ):
        new = super(DockAreaWithUncloseableDocks, self).makeContainer(typ)
        if hasattr(new, "setChildrenCollapsible"):
            new.setChildrenCollapsible(False)
        return new

class ModeInterface(Enum):
    DEFFAULT  = (False,False,False,False)
    MANUAL    = (True,True,True,False)
    MANUALSUM = (True,True,True,True)
    ONLINE    = (True,True,False,False)  
    def __init__(self,chartEnabled,comboBoxTypeEnabled,controlDataIdEnabled,controlSumDataIdEnabled):
        self.chartEnabled = chartEnabled
        self.comboBoxTypeEnabled = comboBoxTypeEnabled
        self.controlDataIdEnabled = controlDataIdEnabled
        self.controlSumDataIdEnabled = controlSumDataIdEnabled


class MainWindow(QtWidgets.QMainWindow, QtCore.QObject):
    sigIterationValueId = QtCore.pyqtSignal(int)
    sigSetNewId = QtCore.pyqtSignal(int)
    sigSetNewCountSum = QtCore.pyqtSignal(int)
    flagControlKeysOff = False
    #self.sigSetRealTimeMode = QtCore.pyqtSignal()
    #self.sigUnsetRealTimeMode = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super().__init__(parent)
        log.debug("Init main window")
        str = resource_filename(uicFile.__name__, "MainWindow.ui")
        log.debug(str)
        uic.loadUi(str, self)

        self.actionPlots.triggered.connect(self.__openViewGraphics__)
        self.actionReset_position.triggered.connect(lambda : self.dockAreaChart.restoreState(self.dockAreaState))
        self.pushButtonNext.clicked.connect(self.__nextId__)
        self.pushButtonPrev.clicked.connect(self.__prevId__)
        self.pushButtonNext.setFocus()

        self.progressBarTask.setHidden(True)

        self.dockAreaChart = DockAreaWithUncloseableDocks()

        self.profileDockX1 = ProfileBeamDock(self.keyPressEvent, name="MCP X B1", size=(5,1))
        self.profileDockX2 = ProfileBeamDock(self.keyPressEvent, name="MCP X B2", size=(5,1))
        self.profileDockY1 = ProfileBeamDock(self.keyPressEvent, name="MCP Y B1", size=(5,1))
        self.profileDockY2 = ProfileBeamDock(self.keyPressEvent, name="MCP Y B2", size=(5,1))
        self.descriptionData = DescriptionDataDock(self.keyPressEvent,name="DATA DESCRIPTION",size=(1,1))

        self.dockAreaChart.addDock(self.descriptionData)
        self.dockAreaChart.addDock(self.profileDockX1,'left',self.descriptionData)
        self.dockAreaChart.addDock(self.profileDockY1,"right",self.profileDockX1)
        self.dockAreaChart.addDock(self.profileDockX2,"bottom",self.profileDockX1)
        self.dockAreaChart.addDock(self.profileDockY2,"bottom",self.profileDockY1)
        self.horizontalLayoutGraphics.addWidget(self.dockAreaChart)
        
        self.dockAreaState = self.dockAreaChart.saveState()
        
        self.comboBoxType.addItem("Manual")
        self.comboBoxType.addItem("Online")
        self.comboBoxType.addItem("Manual sum")
        self.comboBoxType.setCurrentIndex(0)
    
        self.realTimeModeOn = False
        self.savedStateinterface = None

        self.setMode(ModeInterface.DEFFAULT)
    def setInfinityProgress(self, mode:bool):
        self.progressBarTask.setMaximum(0 if mode else 100)
        self.progressBarTask.setMinimum(0)
        self.progressBarTask.setValue(-1 if mode else 0)

    def autoRangeAllProfileDocks(self):
        self.profileDockX1.autoRangeAll()
        self.profileDockX2.autoRangeAll()
        self.profileDockY1.autoRangeAll()
        self.profileDockY2.autoRangeAll()

    def keyPressEvent(self,event):
        #if event.key() == Qt.Key.Key_Right:
        #    self.__nextId__()
        #if event.key() == Qt.Key.Key_Left:
        #    self.__prevId__()
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            if self.spinBoxId.hasFocus():
                self.__setId__()
            if self.spinBoxCountSum.hasFocus():
                self.__setCountSum()
        if event.key() == Qt.Key.Key_Right:
            self.__nextId__()
        if event.key() == Qt.Key.Key_Left:
            self.__prevId__()


    def __setId__(self):
        self.sigSetNewId.emit(self.spinBoxId.value())
        self.spinBoxId.clearFocus()
    def __setCountSum(self):
        self.sigSetNewCountSum.emit(self.spinBoxCountSum.value())
        self.spinBoxCountSum.clearFocus()

    def __nextId__(self):
        self.sigIterationValueId.emit(+1)

    def __prevId__(self):
        self.sigIterationValueId.emit(-1)
        
    def setMode(self, mode:ModeInterface):
        self.currentMode = mode
        self.dockAreaChart.setEnabled(mode.chartEnabled)
        self.comboBoxType.setEnabled(mode.comboBoxTypeEnabled)
        self.spinBoxId.setEnabled(mode.controlDataIdEnabled)
        self.pushButtonNext.setEnabled(mode.controlDataIdEnabled)
        self.pushButtonPrev.setEnabled(mode.controlDataIdEnabled)
        self.spinBoxCountSum.setEnabled(mode.controlSumDataIdEnabled)
        self.pushButtonChooseRecord.setEnabled(mode.controlDataIdEnabled)

    def setButtonNextEnabled(self,enabled):
        self.pushButtonNext.setEnabled(enabled)
    def setButtonPrevEnabled(self,enabled):
        self.pushButtonPrev.setEnabled(enabled)
        
    def setBusyMode(self,mode):
        if mode:
            self.savedStateinterface = (
                self.dockAreaChart.isEnabled(),
                self.comboBoxType.isEnabled(),
                self.spinBoxId.isEnabled(),
                self.pushButtonNext.isEnabled(),
                self.pushButtonPrev.isEnabled(),
                self.spinBoxCountSum.isEnabled(),
                self.pushButtonChooseRecord.isEnabled()
            )
            self.dockAreaChart.setEnabled(not mode)
            self.comboBoxType.setEnabled(not mode)
            self.spinBoxId.setEnabled(not mode)
            self.pushButtonNext.setEnabled(not mode)
            self.pushButtonPrev.setEnabled(not mode)
            self.spinBoxCountSum.setEnabled(not mode)
            self.pushButtonChooseRecord.setEnabled(not mode)
        else:
            if self.savedStateinterface == None:
                return
            self.dockAreaChart.setEnabled(self.savedStateinterface[0])
            self.comboBoxType.setEnabled(self.savedStateinterface[1])
            self.spinBoxId.setEnabled(self.savedStateinterface[2])
            self.pushButtonNext.setEnabled(self.savedStateinterface[3])
            self.pushButtonPrev.setEnabled(self.savedStateinterface[4])
            self.spinBoxCountSum.setEnabled(self.savedStateinterface[5])
            self.pushButtonChooseRecord.setEnabled(self.savedStateinterface[6])
    
    def setIdValue(self,id):
        self.spinBoxId.setValue(id)
    def setRangeId(self,min,max):
        self.spinBoxId.setMaximum(max)
        self.spinBoxId.setMinimum(min)

    #def connectSignalIteration

    def setIndexListData(self,data):
        self.comboBoxListData.addItems(data)
    
    def setData(self,dataX1,scaleTimeX1,delayX1,dataY1,scaleTimeY1,delayY1,dataX2,scaleTimeX2,delayX2,dataY2,scaleTimeY2,delayY2,scaleChannelToMM):
        self.profileDockX1.setData(dataX1, scaleTimeX1,scaleChannelToMM,delayX1)
        self.profileDockY1.setData(dataY1, scaleTimeY1,scaleChannelToMM,delayY1)
        self.profileDockX2.setData(dataX2, scaleTimeX2,scaleChannelToMM,delayX2)
        self.profileDockY2.setData(dataY2, scaleTimeY2,scaleChannelToMM,delayY2)
    def setDataInfo(self,text):
        self.descriptionData.setText(text)
    
    def __openViewGraphics__(self):
        self.viewGraphics = ViewGraphicsDialog(self.centralwidget , not self.profileDockX1.isHidden(), not self.profileDockX2.isHidden(), not self.profileDockY1.isHidden() ,not self.profileDockY2.isHidden(), not self.descriptionData.isHidden())
        self.viewGraphics.getUI().checkBoxMCPX1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX1))
        self.viewGraphics.getUI().checkBoxMCPX2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX2))
        self.viewGraphics.getUI().checkBoxMCPY1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY1))
        self.viewGraphics.getUI().checkBoxMCPY2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY2))
        self.viewGraphics.getUI().checkBoxDataDescription.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.descriptionData))
        self.viewGraphics.show()
    
    def __changeHiddenModeDock__(self,dock):
        if dock.isHidden():
            dock.show()
        else:
            dock.hide()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
    
    
    
