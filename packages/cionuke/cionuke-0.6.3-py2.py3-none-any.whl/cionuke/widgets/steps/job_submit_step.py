from cionuke.widgets.steps import base


class JobSubmitStepWidget(base.StepWidget):
    '''
    A StepWidget to show the progress of the job submission phase (when the payload is sent to the
    Conductor end-point)
    '''
    
    STEP_NAME = "Submitting Job"
    
    def __init__(self, *args, **kwargs):
        super(JobSubmitStepWidget, self).__init__(stepName=self.STEP_NAME, *args, **kwargs)
        
    def setJobSubmitProgress(self, uploadStats):
        if hasattr(uploadStats, "job_submission"):
            self.setProgress(uploadStats.job_submission)           
            