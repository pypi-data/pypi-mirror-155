from PySide2 import QtWidgets

class FileProgressBar(QtWidgets.QWidget):
    '''
    A progress bar with an added file label to the left
    '''
    
    def __init__(self, fileName, *args, **kwargs):        
        
        super(FileProgressBar, self).__init__(*args, **kwargs)
        self.setLayout(QtWidgets.QHBoxLayout())
        
        self.fileLabel = QtWidgets.QLabel(fileName)
        self.progressBar = QtWidgets.QProgressBar(parent=self)
        
        self.layout().addWidget(self.fileLabel)
        self.layout().addWidget(self.progressBar)
        
    def setProgressValue(self, value):
        self.progressBar.setValue(value)
        
    def getProgressValue(self):
        return self.progressBar.value()