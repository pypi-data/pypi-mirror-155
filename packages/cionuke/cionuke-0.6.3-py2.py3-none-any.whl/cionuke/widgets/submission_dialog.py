import json
import requests
import traceback

try:
    import urlparse as parse
except ImportError:
    from urllib import parse
    
from PySide2 import QtWidgets, QtCore

import ciocore.exceptions
import ciocore.config

from cionuke.widgets import submit_mult_step
from . import utils

from cionuke import const as k


class SubmissionDialog(QtWidgets.QDialog):
    '''
    Threaded dialog to submit jobs to Conductor
    '''
    
    def __init__(self, submitter, validators=None, autoValidate=False, parent=None ):
        '''
        If autoValidate is True, the validators will be run when the dialog is shown.
        '''
        
        super(SubmissionDialog, self).__init__(parent=parent)
        
        self.submitter = submitter
        self.validators = validators or []
        self.autoValidate = autoValidate
        self.successfulValidation = False
        
        title = "Submission"

        self.setWindowTitle(title)

        self.buildUI()
        self.connectSlots()
            
    def show(self, *args, **kwargs):

        if self.autoValidate:
            self.onValidate()
            
        super(SubmissionDialog, self).show(*args, **kwargs)
        
    def buildUI(self):

        maxHeight = utils.getScaledScreenValue(900)
        maxWidth = utils.getScaledScreenValue(600)

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.validateButton = QtWidgets.QPushButton(self.tr("&Validate"))
        self.submitButton = QtWidgets.QPushButton(self.tr("&Submit"))
        
        self.buttonBox = QtWidgets.QDialogButtonBox(buttons, parent=self)
        self.buttonBox.addButton(self.validateButton, QtWidgets.QDialogButtonBox.ApplyRole)
        self.buttonBox.addButton(self.submitButton, QtWidgets.QDialogButtonBox.ApplyRole)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(True)
        
        self.multiStepWidget = submit_mult_step.SubmitMultiStep(submitter=self.submitter,
                                                                 validators=self.validators,
                                                                 parent=self
                                                                 )

        self.setLayout( QtWidgets.QVBoxLayout() )
        self.layout().addWidget(self.multiStepWidget)
        self.layout().addStretch(stretch=0)
        self.layout().addWidget(self.buttonBox)
        
        self.multiStepWidget.setMinimumSize(maxWidth, -1)
        self.multiStepWidget.setMaximumSize(maxWidth, maxHeight)
        
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        
        self.jobCompletedMessageBox = QtWidgets.QMessageBox(parent=self)
        self.jobCompletedMessageBox.setTextFormat(QtCore.Qt.RichText)
        
    def connectSlots(self):
        
        self.buttonBox.accepted.connect(self.accept)                        
        self.buttonBox.rejected.connect(self.reject)
        
        self.submitButton.clicked.connect(self.onSubmit)
        self.validateButton.clicked.connect(self.onValidate)
        self.multiStepWidget.completed.connect(self.workCompleted)
        self.multiStepWidget.errored.connect(self.onError)
        
        self.jobCompletedMessageBox.setTextFormat(QtCore.Qt.RichText)   

    def onSubmit(self):

        try:
            if not self.successfulValidation or self.multiStepWidget.validate():
                self.doSubmission()
        
        except BaseException as ex:
            raise
        
    def onValidate(self):
        self.validationSuccesful = self.submitButton.setEnabled(self.multiStepWidget.validate())
        return self.validationSuccesful

    def doSubmission(self):

        self.multiStepWidget.submit()        

        self.submitButton.setEnabled(False)
        self.validateButton.setEnabled(False)
        
    def onError(self, exceptionClass, exception, tb):
        
        # If the user cancelled the submission, don't show the dialog
        if exceptionClass == ciocore.exceptions.UserCanceledError:
            return
                
        informativeText = None        
        
        if exceptionClass == requests.exceptions.HTTPError:
            informativeText = json.loads(exception.response.text)['message']        
        
        # Close the progress dialog
        self.jobCompletedMessageBox.finished.connect(self.reject)
        
        self.jobCompletedMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
        self.jobCompletedMessageBox.setWindowTitle("Error!")
        
        # Force the dialog to be wider
        self.jobCompletedMessageBox.setText(str(exception) + " "*20)

        if informativeText:
            self.jobCompletedMessageBox.setInformativeText(informativeText)
        
        self.jobCompletedMessageBox.setDetailedText("".join(traceback.format_tb(tb)))
        
        self.jobCompletedMessageBox.open()

    def workCompleted(self, response, responseCode):
        
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)        
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setEnabled(False)
        
        errorDetails = None
        
        self.submitButton.setEnabled(False)
 
        if response.get("status") == "success":
            try:
                success_msg = self.get_success_message(response)
                info_msg = self.get_downloader_info_message(response)
                daemon_msg = self.get_daemon_message()
                informativeText = "\n\n".join((info_msg, daemon_msg))

                self.jobCompletedMessageBox.setIcon(QtWidgets.QMessageBox.Information)
                self.jobCompletedMessageBox.setWindowTitle("Job submitted")
                self.jobCompletedMessageBox.setText(success_msg)
                self.jobCompletedMessageBox.finished.connect(self.accept)
                             
            except BaseException as ex:
                errorDetails = traceback.format_exc()
                self.jobCompletedMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
                self.jobCompletedMessageBox.setWindowTitle("Error!")
                self.jobCompletedMessageBox.setText(str(ex))
        else:

            errorDetails = response["body"]    
            self.jobCompletedMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.jobCompletedMessageBox.setWindowTitle("Error!")
            self.jobCompletedMessageBox.setText("Error when submitting to Conductor")                  
        
        if informativeText:
            self.jobCompletedMessageBox.setInformativeText(informativeText)
            
        if errorDetails:
            self.jobCompletedMessageBox.setDetailedText(str(errorDetails))
        
        self.jobCompletedMessageBox.open()

    def get_success_message(self, response):
        
        cfg = ciocore.config.config().config
        success_uri = response["uri"].replace("jobs", "job")
        url = parse.urljoin(cfg["url"], success_uri)
        message = 'Success!<br><br><a href="{url}">{url}</a>'.format(url=url)
        
        return message

    def get_downloader_info_message(self, response):
        
        # The use of format() appears to be incompatible with rich text tokens, hence the strings
        # are concatenated
        job_id = response["uri"].split("/")[-1]
        
        msg = "To download finished frames, either use the Companion app, or enter the following command in a terminal or command prompt:<br><br><code>"
        msg += k.CONDUCTOR_COMMAND_PATH
        msg += " downloader --job_id "
        msg += job_id
        msg += "</code>"
                
        return msg

    def get_daemon_message(self):
        
        # The use of format() appears to be incompatible with rich text tokens, hence the strings
        # are concatenated        
        use_daemon = not self.submitter['local_upload']
        
        if not use_daemon:
            return ""
        
        location = self.submitter['location']
        
        if location:
            msg = "This submission expects an uploader daemon to be running and set to a specific location tag.<br>"
            msg += "If you haven't already done so, open a shell and type:<br><code>"
            msg += k.CONDUCTOR_COMMAND_PATH
            msg += " uploader --location "
            msg += location
            msg += "</code><br><br>"
        
        else:
            msg = "This submission expects an uploader daemon to be running.<br>"
            msg += "If you haven't already done so, open a shell and type:<br><code>"
            msg += k.CONDUCTOR_COMMAND_PATH
            msg += " uploader</code><br><br>"

        msg += "You'll also find this information in the script editor.\n"

        return msg
    
    def reject(self):
        self.multiStepWidget.stop()
        super(SubmissionDialog, self).reject()
        
    def accept(self):
        
        self.multiStepWidget.cleanUpThreads()    
        super(SubmissionDialog, self).accept()
