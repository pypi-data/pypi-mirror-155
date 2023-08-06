from PySide2 import QtWidgets

from cionuke.widgets.steps import base

from .. import notice_grp
from .. import validation_item
from cionuke.widgets import multi_step


class ValidationStepWidget(base.StepWidget):
    '''
    A StepWidget representing a particular Validation item
    '''
    
    STEP_NAME = "Validation"
    
    def __init__(self, validators, *args, **kwargs):
                
        detailWidget = ValidationDetailWidget        
        super(ValidationStepWidget, self).__init__(stepName=self.STEP_NAME, detailWidget=detailWidget, *args, **kwargs)
        
        self.addValidators(validators) 
        
    def addValidators(self, validators):
        self.validators = validators
        self.detailWidget.addValidators(self.validators)
        
    def validate(self):
        self.detailWidget.validate()
        successPercentage = self.detailWidget.getSuccessPercentage()
        self.setProgress(successPercentage)
        
        return successPercentage == 100.0


class ValidationDetailWidget(multi_step.MultiStep):
    
    HEADER_ERROR = [
        "There are issues that would cause your submission to fail.",
        "To save you unwanted costs, the submission is blocked. ",
        "Please attend to the errors listed below and try again.",
    ]
    
    HEADER_WARNING = [
        "There are issues that could cause unexpected results in your render.",
        "Please read the messages carefully.",
        "If everything looks okay, you can continue with the submission.",
    ]
    
    HEADER_INFO = [
        "There are some informational notices below.",
        "Please read the messages.",
        "If everything looks okay, continue with the submission.",
    ]
    
    def addValidators(self, validators):
        
        for validator in validators:            
            validatorWidget = validation_item.ValidationItem(validator)
            self.addStepWidget(validatorWidget)
            
    def validate(self):
        
        failed_items = 0
        
        for validator_widget in self.stepWidgets.values():
            validator_widget.run()
            
            if validator_widget.isErrored():
                failed_items += 1
                
        self.successPercentage = (float(len(self.stepWidgets) - failed_items) / float(len(self.stepWidgets))) * 100.0
        
    def getSuccessPercentage(self):
        return self.successPercentage
    
    def populateValidationMessages(self, messages):

        widgets = []
        
        for severity in ["error", "warning", "info"]:
            for entry in messages[severity]:
                self.addStepWidget(notice_grp.NoticeGrp(entry, severity=severity, stepName=entry))
        
        headerMsg = None
        
        if messages["error"]:
            if self.submitting:
                headerMsg = "\n".join(self.HEADER_ERROR)
            else:
                headerMsg = self.HEADER_ERROR[0]
        
        elif messages["warning"]:
            if self.submitting:
                headerMsg = "\n".join(self.HEADER_WARNING)
            else:
                headerMsg = self.HEADER_WARNING[0]
        
        elif messages["info"]:
            if self.submitting:
                headerMsg = "\n".join(self.HEADER_INFO)
            else:
                headerMsg = self.HEADER_INFO[0]
        
        else:
            msg = "We found no issues with this submission."
            self.addStepWidget(notice_grp.NoticeGrp(msg, severity="success", stepName="validationSuccess"))

        if headerMsg:
            header_widget = QtWidgets.QLabel()
            header_widget.setWordWrap(True)
            header_widget.setText(headerMsg)
            widgets = [header_widget] + widgets