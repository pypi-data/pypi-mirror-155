import webbrowser

from PySide2 import QtWidgets, QtCore

from . import icons


STYLESHEET = """
QFrame {{ border: none; margin: none; padding:none;}}
"""


class NoticeGrp(QtWidgets.QFrame):

    def __init__(self, text, severity="info", url=None):
        super(NoticeGrp, self).__init__()

        self.url = url
        if severity not in ["info", "warning", "error", "success"]:
            severity = "error"

        self.scale_factor = self.logicalDpiX() / 96.0

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setLineWidth(2)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        layout.setMargin(0)
        layout.setSpacing(0)
        
        icon = icons.StatusIcon.getIconForSeverity(severity)

        img_label = QtWidgets.QLabel(self)
        img_label.setPixmap(icon)
        img_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        img_label.setFixedWidth(40 * self.scale_factor)
        layout.addWidget(img_label)

        if self.url:
            self.label = QtWidgets.QPushButton(text)
            self.label.setAutoDefault(False)
            self.label.clicked.connect(self.on_click)
        else:
            self.label = QtWidgets.QLabel()
            self.label.setMargin(10)
            self.label.setWordWrap(True)
            self.label.setText(text)

        layout.addWidget(self.label)
        self.setStyleSheet(STYLESHEET)

    def on_click(self):
        webbrowser.open(self.url)
