from PySide2 import QtWidgets

from cionuke.widgets.steps import base

class MD5StepWidget(base.StepWidget):
    '''
    A StepWidget to show the progress of the MD5 calculation phase of the submission process.
    Shows a progress-bar for the overall process and a count of files completed / total files
    '''
    
    STEP_NAME = "Computing MD5"
    CACHED_SUFFIX = "--cached--"
    
    def __init__(self, *args, **kwargs):
        
        
        detailWidget = MD5StepDetailWidget        
        super(MD5StepWidget, self).__init__(stepName=self.STEP_NAME, detailWidget=detailWidget, *args, **kwargs)
        
    def setMD5Progress(self, uploadStats):

        try:
            processedMD5 = len([f['md5'] for f in uploadStats.file_progress.value.values()])
            
        except AttributeError:
            return 
        
        self.setStepLabel("{} {}/{}".format(self.STEP_NAME, processedMD5, uploadStats.files_to_analyze))

        self.setProgress(processedMD5/uploadStats.files_to_analyze*100.0)
        
        for filePath in uploadStats.file_progress.value.keys():
            
            if uploadStats.file_progress.value[filePath]['md5_was_cached']:
                filePath = "{} {}".format(filePath, self.CACHED_SUFFIX)
            
            self.detailWidget.addCompletedFile(filePath)
            
            
class MD5StepDetailWidget(QtWidgets.QWidget):
    '''
    The detail widget for the MD5 calculation step. Displays a list of all the files that have 
    already been processed and whether those files utilized the cache or not.
    '''
    
    HIDE_COMPLETED_FILES = True
     
    def __init__(self, *args, **kwargs):        
        
        super(MD5StepDetailWidget, self).__init__(*args, **kwargs)
        
        self.setLayout(QtWidgets.QVBoxLayout())        
        self.completedFileLayout = QtWidgets.QVBoxLayout()

        
        self.completedFilelabel = QtWidgets.QLabel("Completed files", parent=self)
        self.completedFileTextBox = QtWidgets.QTextEdit(parent=self)
        
        self.completedFileLayout.addWidget(self.completedFilelabel)
        self.completedFileLayout.addWidget(self.completedFileTextBox)
        
        self.layout().addLayout(self.completedFileLayout)
        
        self.completedfileNames = []    

    def addCompletedFile(self, fileName):
        
        if fileName not in self.completedfileNames:
            self.completedfileNames.append(fileName)
            self.completedfileNames.sort()
            self.completedFileTextBox.setPlainText("\n".join(self.completedfileNames))