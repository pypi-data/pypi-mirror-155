import os

from PySide2 import QtGui

from cionuke.const import PLUGIN_DIR


class StatusIcon(QtGui.QPixmap):
    
    SEVERITY = ""
    
    def __init__(self, *args, **kwargs):
        
        super(StatusIcon, self).__init__(*args, **kwargs)  
        
        icon_size = 24 if self.logicalDpiX() < 150 else 48
                
        icon_filename = "Conductor{0}_{1}x{1}.png".format(self.SEVERITY.capitalize(), icon_size)
        iconPath = os.path.join(PLUGIN_DIR, 'icons', icon_filename)
        
        if not self.load(iconPath):
            raise Exception("Unable to load icon {}".format(iconPath))
        
    @staticmethod
    def getIconForSeverity(severity):
        
        icon = None
        
        for klass in StatusIcon.getSubClasses():
            if klass.SEVERITY == severity:
                icon = klass()
                break
            
        if icon is None:
            raise Exception("Unable to find icon for severity level '{}'".format(severity))
                
        return icon
        
    @classmethod
    def getSubClasses(cls):
        class_names = []
        sub_classes = []
        for sub_class in cls.__subclasses__():
            if sub_class.__name__ not in class_names:
                sub_classes.append(sub_class)
                class_names.append(sub_class.__name__)
        
        return sub_classes        

class SuccessStatusIcon(StatusIcon):
    SEVERITY = "success"
    
class WarningStatusIcon(StatusIcon):
    SEVERITY = "warning"
    
class ErrorStatusIcon(StatusIcon):
    SEVERITY = "error"
    
class SubmitStatusIcon(StatusIcon):
    SEVERITY = "submit"
    
class InfotatusIcon(StatusIcon):
    SEVERITY = "info"                 
    
