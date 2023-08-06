from PySide2 import QtWidgets, QtCore

from . import notice_grp
from . import icons


class ValidationItem(QtWidgets.QFrame):
    '''
    A ValidationItem is intended to be used within the ValidationStepWidget
    '''
    
    STEP_NAME = "validator"
    
    STATUS_NOTRUN = "notrun"
    STATUS_SUCCESS = "success"
    STATUS_ERRORED = "error"
    STATUS_WARNING = "warning"
    
    def __init__(self, validator, *args, **kwargs):
        super(ValidationItem, self).__init__(*args, **kwargs)
        
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setLineWidth(2)        
        
        self.validator = validator
        self.stepName = self.validator.title()
        self.headerText = self.validator.title()
        self.status = self.STATUS_NOTRUN
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        self.addHeader()
        
    def addHeader(self):
                
        self.header = ValidationItemHeader(self.headerText, 
                                           self.validator.DESCRIPTION, 
                                           parent=self)
        
        self.layout().addWidget(self.header)
        
    def setStatus(self, status=None):
        
        # If no status is given, determine it
        if status is None:
            if self.validator.errors:
                status = self.STATUS_ERRORED
                
            elif self.validator.warnings:
                status = self.STATUS_WARNING
                
            else:
                status = self.STATUS_SUCCESS 
                    
        self.status = status
        
        if self.status == self.STATUS_NOTRUN:
            self.header.label.setText(self.headerText)
            
        else:
            self.header.setStatus(self.status)
        
    def isErrored(self):
        return self.status == self.STATUS_ERRORED
    
    def run(self):        
        
        try:
            self.validator.run(None)
        
        except BaseException as ex:
            warning = "[{}]:\nValidator failed to run. Don't panic, it's probably due to an unsupported feature and can be ignored.\n{}".format(
                    self.validator.title(), str(ex)
            )
            notice_grp.NoticeGrp(warning, severity="warning")
            raise
            
        for msg in self.validator.errors:            
            self.addMessage(msg, 'error')
            
        for msg in self.validator.warnings:
            self.addMessage(msg, 'warnings')
            
        for msg in self.validator.notices:
            self.addMessage(msg, 'info')
            
        self.setStatus()

    def addMessage(self, message, severity):
        
        new_notice_group = notice_grp.NoticeGrp(message, severity=severity)
        self.layout().addWidget(new_notice_group)
        
        return new_notice_group
    
class ValidationItemHeader(QtWidgets.QWidget):    
    
    def __init__(self, name, description, *args, **kwargs):
        
        super(ValidationItemHeader, self).__init__(*args, **kwargs)
        
        self.name = name
        self.description = description
        
        mainLayout = QtWidgets.QVBoxLayout()
        topLayout = QtWidgets.QHBoxLayout()
        descriptionLayout = QtWidgets.QHBoxLayout()
        
        self.nameLabel = QtWidgets.QLabel(text=self.name, parent=self)
        
        self.statusIcon = QtWidgets.QLabel(parent=self)
        self.statusIcon.setPixmap(icons.SubmitStatusIcon())
        self.statusIcon.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
        self.descriptionLabel = QtWidgets.QLabel(text=self.description, parent=self)
        
        topLayout.addWidget(self.nameLabel)
        topLayout.addWidget(self.statusIcon)
        descriptionLayout.addWidget(self.descriptionLabel)
                
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(descriptionLayout)
        self.setLayout(mainLayout)
        
    def setStatus(self, status):
        
        icon = icons.StatusIcon.getIconForSeverity(status)
        self.statusIcon.setPixmap(icon)
