from PySide2 import QtWidgets

class StepWidget(QtWidgets.QWidget):
    '''
    The StepWidget an item in the MultiStep widget. It's intended to represent a running process.
    It has a progress-bar and an optional nested detail widget that can be show/hidden.
    
    These classes should run the actual process. They should be updated by a seperate thread using
    Qt's slots & signals.
    '''
    
    def __init__(self, stepName, detailWidget=None, stepLabel=None, *args, **kwargs):
        super(StepWidget, self).__init__(*args, **kwargs)
        
        self.stepName = stepName
        self.stepLabel = stepLabel or self.stepName 
        
        self.setLayout(QtWidgets.QVBoxLayout())
        self.mainRow = QtWidgets.QGridLayout()
                    
        self.toggleDetailWidgetButton = QtWidgets.QPushButton("+")
        self.toggleDetailWidgetButton.setMinimumSize(10, 10)
        self.toggleDetailWidgetButton.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred) 
        
        self.stepLabelWidget = QtWidgets.QLabel()
        self.setStepLabel(self.stepLabel)
        self.progressBar = QtWidgets.QProgressBar(parent=self)

        self.mainRow.addWidget(self.stepLabelWidget, 0, 0)
        self.mainRow.addWidget(self.progressBar, 0, 1)
        self.mainRow.addWidget(self.toggleDetailWidgetButton, 0, 2)
        
        self.layout().addLayout(self.mainRow)
        
        if detailWidget:
            self.detailWidget = detailWidget(parent=self)
            self.layout().addWidget(self.detailWidget)
            self.detailWidget.hide()
            
        else:
            self.toggleDetailWidgetButton.hide()
            
        # Signals
        self.toggleDetailWidgetButton.clicked.connect(self.onToggleDetailWidget)
        
    def onToggleDetailWidget(self):
        
        if self.detailWidget.isVisible():
            self.toggleDetailWidgetButton.setText("+")
            self.detailWidget.hide()
        
        else:
            self.toggleDetailWidgetButton.setText("-")
            self.detailWidget.show()
            
    def setStepLabel(self, name):
        self.stepLabelWidget.setText(name)
        
    def setProgress(self, value):
        self.progressBar.setValue(value)  