import nuke

from PySide2 import QtWidgets

from cionuke.widgets import submission_dialog
from .. import utils
from .. import validation


class NukeSubmissionDialog(submission_dialog.SubmissionDialog):
    
    def __init__(self, autosave_filename, autosave=True, *args, **kwargs):
        
        super(NukeSubmissionDialog, self).__init__(*args, **kwargs)
        
        self.autosave = autosave
        self.autosave_filename = autosave_filename
        
    def doSubmission(self): 
        """
        Save or autosave, then submit

        Returns:
            tuple: submission response and code.
        """
                
        if self.autosave:
            with utils.transient_save(self.autosave_filename):
                with utils.create_directories_on():
                    submission_dialog.SubmissionDialog.doSubmission(self)
        else:
            with utils.create_directories_on():
                if nuke.Root().modified():
                    if not nuke.scriptSave():
                        return (False, False)
                submission_dialog.SubmissionDialog.doSubmission(self)
            
    @classmethod
    def createFromNukeNode(cls, node, autoValidate=False):
        '''
        Creates a NukeSubmissionDialog based off the value of a Conductor Nuke node.
        
        :param node: A Conductor submitter node
        :type node: Nuke.Node        
        '''
        
        kwargs = {"should_scrape_assets": True}
        submissionPayload = utils.resolve_submission(node, **kwargs)
    
        autosave = bool(node.knob("cio_do_autosave").getValue())
        cio_filename = node.knob("cio_autosave_template").getValue()
        
        validators = validation.get_validators(node)
        
        
        dialog = cls(submitter=submissionPayload, 
                     autosave=autosave,
                     autosave_filename = cio_filename,
                     validators=validators,
                     autoValidate=autoValidate,
                     parent=QtWidgets.QApplication.activeWindow()
                     )
        
        return dialog   