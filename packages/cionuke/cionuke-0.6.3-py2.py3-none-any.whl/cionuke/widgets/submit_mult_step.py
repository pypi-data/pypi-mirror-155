import logging
import sys
import time
import types

from PySide2 import QtCore

import ciocore.conductor_submit

from cionuke.widgets import multi_step
from cionuke.widgets.steps import validation_step
from cionuke.widgets.steps import md5_step
from cionuke.widgets.steps import upload_step
from cionuke.widgets.steps import job_submit_step

logging = logging.getLogger("conductor")

class SubmitMultiStep(multi_step.MultiStep):
    '''
    Implements a MultiStep widget for the various steps of submitting a job
    '''
    
    completed = QtCore.Signal(dict, int)
    errored = QtCore.Signal(type, BaseException, types.TracebackType)
    started = QtCore.Signal()
    
    def __init__(self, validators=None, submitter=None, *args, **kwargs):
        super(SubmitMultiStep, self).__init__(*args, **kwargs)
        
        self.submitter = submitter
        self.validators = validators
        
        self.worker = SubmitWorker()
        self.thread = QtCore.QThread(self)
        self.thread.started.connect(self.worker.run)
    
        self.worker.completed.connect(self.onCompleted)
        self.worker.errored.connect(self.onError)     
        
        self.addStepWidgets()
        
    def validate(self):
         
        return self.stepWidgets[validation_step.ValidationStepWidget.STEP_NAME].validate()
    
    def submit(self):
        
        if not self.submitter:
            raise ValueError("The submitter (SubmitMultiStep.submitter) must be set prior to calling submit()")
        
        self.worker.submission = self.submitter        

        self.worker.moveToThread(self.thread)
        
        self.thread.start()
        self.started.emit()
        
    def stop(self):
        '''
        Force the worker to stop and then ensure the thread is completed
        '''
        
        if self.worker:        
            self.worker.stop()
            
        if self.thread:
            self.thread.quit()
            
        self.cleanUpThreads()
        
    def onError(self, exceptionClass, exception, tb):
        
        self.cleanUpThreads()
        self.errored.emit(exceptionClass, exception, tb)
        
    def onCompleted(self, response, responseCode):
        
        self.cleanUpThreads()
        self.completed.emit(response, responseCode)
        
    def cleanUpThreads(self):
        '''
        The threads are notorious for not completing on their own. This method tries to clean 
        them up as gracefully as possible, utlimately killing them if necessary.
        
        Some applications are very sensitive to forcefully killing threads (ex: Nuke) so it's only
        a last resort
        '''
        
        if self.thread:
            logging.debug("Quitting thread {}".format(self.thread))
            self.thread.exit()
            time.sleep(0.5)
            
            if not self.thread.isFinished():
                logging.warning("Thread did not quit. Waiting for 1s")
                if not self.thread.wait(1.0):
                    logging.warning("Thread did not quit after waiting. Terminating")
                    self.thread.terminate()
                    self.thread.wait(1.0)
            
            logging.debug("Is thread finished? {}".format(self.thread.isFinished()))        
        
    def setWorker(self, worker):
        self.worker = worker
        self.addStepWidgets()
        
    def addStepWidgets(self):
        
        if self.validators:        
            newWidget = validation_step.ValidationStepWidget(parent=self, validators=self.validators)
            self.addStepWidget(newWidget)

        newWidget = md5_step.MD5StepWidget(parent=self)
        self.worker.updatedProgress.connect(newWidget.setMD5Progress)
        self.addStepWidget(newWidget)   
        
        newWidget = upload_step.UploadStepWidget(parent=self)
        self.worker.updatedProgress.connect(newWidget.setUploadProgress)
        self.addStepWidget(newWidget)
        
        newWidget = job_submit_step.JobSubmitStepWidget(parent=self)
        self.worker.updatedProgress.connect(newWidget.setJobSubmitProgress)
        self.addStepWidget(newWidget)
        

class SubmitWorker(QtCore.QObject):
    '''
    Main worker thread for submitting a job.
    
    Note: Any exceptions that are raised within this worker thread (and its children) will not bubble
    up unless caught by the try/except in run(). If submitting a job and nothing seems to happen,
    it's most likely the result of a an exception being raised.
    '''
    
    updatedProgress = QtCore.Signal(object)
    completed = QtCore.Signal(dict, int)
    errored = QtCore.Signal(type, BaseException, types.TracebackType)
    
    def __init__(self, submission=None, *args, **kwargs):
        
        self.submission = submission
        self.jobSubmit = None
        super(SubmitWorker, self).__init__(*args, **kwargs)
        
    def stop(self):
        '''
        Force the submission process to stop
        '''

        if self.jobSubmit:
            self.jobSubmit.stop_work()
    
    def run(self):

        try:
            self.jobSubmit = ciocore.conductor_submit.Submit(self.submission)
            self.jobSubmit.progress_handler = self.emitProgress
            response, responseCode = self.jobSubmit.main()
        
        except Exception:
            self.errored.emit(*sys.exc_info())
            return False
        
        # Mock class for UploadStats
        class DummyObject(object):
            pass
        
        uploadStats = DummyObject()
        
        # Give the impression that the submission is happening - even though it already happened
        for x in range(1, 21):        
            uploadStats.job_submission = x*5
            self.emitProgress(uploadStats)
            time.sleep(0.05)

        self.completed.emit(response, responseCode)
            
    def emitProgress(self, data):
        self.updatedProgress.emit(data)