"""
Row of action buttons at the top of the submitter.

Currently, Connect, Validate, Submit
"""
import os

import nuke
from ciocore import data as coredata


from cionuke import const as k
from cionuke.widgets import nuke_submission_dialog
from cionuke.components import instance_type, project, software

# In development, you can use fixtures for packages, projects, instance types.
# It saves time. Fixtures
FIXTURES_DIR = os.path.expanduser(os.path.join("~", "conductor_fixtures"))
 
CONNECT_TOOLTIP = """
Connects to your acccount on Conductor. You may be asked to log in. 
Once connected, you'll see the software, project, and machine type dropdown menus are populated.
"""

SUBMIT_TOOLTIP = """
Validates and Submits the job to Conductor's render service.
Runs several validations to check that your scene is in a fit state to submit. 
If there are critical errors the submission will be blocked.
"""

def build(submitter):
    """Build action knobs."""

    knob = nuke.PyScript_Knob("cio_connect", "Connect")
    knob.setTooltip(CONNECT_TOOLTIP)
    submitter.addKnob(knob)

    knob = nuke.PyScript_Knob("cio_submit", "Validate/Submit")
    knob.setTooltip(SUBMIT_TOOLTIP)
    submitter.addKnob(knob)


def knobChanged(node, knob):
    """
    Respond to button pushes.

    Submit has a validate step before submission. 
    """
    knob_name = knob.name()
    if knob_name == "cio_connect":
        connect(node)
    elif knob_name == "cio_submit":
        
        dialog = nuke_submission_dialog.NukeSubmissionDialog.createFromNukeNode( node=node, 
                                                          autoValidate=True)
        dialog.show()


def affector_knobs():
    """
    Knobs in this component that affect the payload when changed.

    If a write node is added, or if the connect button is pressed, the payload needs to be updated.
    """

    return ["inputChange", "cio_connect"]

def connect(submitter):
    """
    Connect to Conductor in order to access users account data.

    Menus must be repopulated.
    """

    coredata.init(product="nuke")
    if k.FEATURE_DEV:
        use_fixtures = submitter.knob("cio_use_fixtures").getValue()
        fixtures_dir = FIXTURES_DIR if use_fixtures else None
        coredata.set_fixtures_dir(fixtures_dir)

    try:
        coredata.data(force=True)
    except BaseException as ex:
        print(str(ex))
        print("Try again after deleting your credentials file (~/.config/conductor/credentials)")
    if coredata.valid():
        project.rebuild_menu(submitter, coredata.data()["projects"])
        instance_type.rebuild_menu(submitter, coredata.data()["instance_types"])
        software.rebuild_menu(submitter, coredata.data().get("software"))
