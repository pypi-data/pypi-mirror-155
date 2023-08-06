from PySide2 import QtCore, QtWidgets

from cionuke.widgets.steps import base
from cionuke.widgets import file_progress_bar

class UploadStepWidget(base.StepWidget):
    '''
    A StepWidget to show progress on the upload process of job submission. The main progress bar
    shows overall progress of the upload. 
    '''
    
    def __init__(self, *args, **kwargs):
        
        detailWidget = UploadStepDetailWidget
        super(UploadStepWidget, self).__init__(stepName="File Upload", detailWidget=detailWidget, *args, **kwargs)
        
    def setUploadProgress(self, uploadStats):

        try:
            percent_complete = uploadStats.percent_complete.value or 0
            
            if len(uploadStats.file_progress.value.items()) and (
                len(self.detailWidget.completedfileNames) == len(uploadStats.file_progress.value.items())):
                percent_complete = 1.0               
            
            self.setProgress(percent_complete*100.0)
            self.detailWidget.setUploadProgress(uploadStats)
            
        except AttributeError:
            pass


class UploadStepDetailWidget(QtWidgets.QWidget):
    '''
    The detail widget shows the progress of each file that is actively being transferred and a list
    of all files that have already been uploaded. Files that have already been uploaded are marked
    with a '--cached--' suffix.
    '''
    
    HIDE_COMPLETED_FILES = True
    CACHED_SUFFIX = "--cached--"
     
    def __init__(self, *args, **kwargs):        
        
        super(UploadStepDetailWidget, self).__init__(*args, **kwargs)
        
        self.setLayout(QtWidgets.QVBoxLayout())        
        self.completedFileLayout = QtWidgets.QVBoxLayout()

        self.fileProgressWidget = QtWidgets.QWidget()
        self.fileProgressScrollArea = QtWidgets.QScrollArea()
        self.fileProgressScrollArea.setWidget(self.fileProgressWidget)
        self.fileProgressScrollArea.setWidgetResizable(True)
        self.fileProgressScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fileProgressScrollArea.hide()
        
        self.fileProgressLayout = QtWidgets.QVBoxLayout(self.fileProgressWidget)
        
        self.completedFilelabel = QtWidgets.QLabel("Completed files", parent=self)
        self.completedFileTextBox = QtWidgets.QTextEdit(parent=self)
        
        self.completedFileLayout.addWidget(self.completedFilelabel)
        self.completedFileLayout.addWidget(self.completedFileTextBox)
        
        self.layout().addWidget(self.fileProgressScrollArea, 2)
        self.layout().addLayout(self.completedFileLayout, 1)
        
        self.fileProgressBars = {}
        self.completedfileNames = []
        
    def addUploadProgressBar(self, fileName):
        
        if self.fileProgressScrollArea.isHidden():
            self.fileProgressScrollArea.show()
            
        newUploadWidget = file_progress_bar.FileProgressBar(parent=self, fileName=fileName)
        self.fileProgressLayout.addWidget(newUploadWidget)
        self.fileProgressBars[fileName] = newUploadWidget
        
    def hideCompletedProgressBar(self, fileName, already_uploaded=False):
        
        if fileName not in self.completedfileNames:
            
            if not already_uploaded:
                self.fileProgressBars[fileName].hide()
            
            self.completedfileNames.append(fileName)
            self.completedfileNames.sort()
            self.completedFileTextBox.setPlainText("\n".join(self.completedfileNames))
        
    def setUploadProgress(self, uploadStats):
        
        for fileName, progress_fields in uploadStats.file_progress.value.items():
            
            # Only add the progress bar if the upload has started
            if progress_fields['bytes_uploaded'] > 0:            
                if fileName not in self.fileProgressBars:
                    self.addUploadProgressBar(fileName)                
                    
                if self.HIDE_COMPLETED_FILES and self.fileProgressBars[fileName].getProgressValue() == 100:
                    self.hideCompletedProgressBar(fileName)

                else:                
                    progress = (float(progress_fields['bytes_uploaded']) / float(progress_fields['bytes_to_upload']))*100.0
                    self.fileProgressBars[fileName].setProgressValue(progress)
                    
            if 'already_uploaded' in progress_fields and progress_fields['already_uploaded']:
                fileName = "{} {}".format(fileName, self.CACHED_SUFFIX)
                self.hideCompletedProgressBar(fileName, already_uploaded=True)