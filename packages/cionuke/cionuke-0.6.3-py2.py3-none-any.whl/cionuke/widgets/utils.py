from PySide2 import QtWidgets

def getScaledScreenValue(value, referenceHeight=1080.0):
    '''
    Gets the scaled value (ex: height or width) compared to the reference height.
    
    This allows conversion for fixed values from one screen resolution to another.
    It allows UI's to be constructed in a reference resolution (default is 1920x1080)
    and scale properly to the running resolution.
    
    If a widget is to take half the screen height at 1080p, value would be 540. If the
    running resolution is 4000x3000, the returned value would be 1500.
    
    :param value: The value in the reference sceen space to scale
    :type value: float
    
    :param referenceHeight: The reference resolution (height) of value
    :type referenceHeight: float [default=1080.0]
    
    :return: The value scaled according to the referenceHeight
    :rtype: float
    '''
    
    scalingFactor = QtWidgets.QApplication.primaryScreen().geometry().height() / referenceHeight
    return scalingFactor * value 
