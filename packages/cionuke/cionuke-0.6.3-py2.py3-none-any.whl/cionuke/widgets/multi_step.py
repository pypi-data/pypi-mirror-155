from PySide2 import QtWidgets

class MultiStep(QtWidgets.QWidget):
    '''
    A widget that vertically lists StepWidgets. Intended to show a set of discreet steps in a 
    process.
    '''
    
    def __init__(self, *args, **kwargs):
        super(MultiStep, self).__init__(*args, **kwargs)
        
        self.setLayout( QtWidgets.QVBoxLayout() )

        self.setAutoFillBackground(True)
        
        self.stepWidgets = {}        
        
    def addStepWidget(self, stepWidget):
        
        self.stepWidgets[stepWidget.stepName] = stepWidget        
        self.layout().addWidget(stepWidget, 0)