"""
coord-convertr v1.0.0
Author: akshatcx (akshat.c2k@gmail.com)
"""
import sys
import utm
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QErrorMessage,
    QWidget,
    QRadioButton,
    QLabel,
    QPlainTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QButtonGroup,
)


class CoordConvertr(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Coord Convertr"
        self.screen_width, self.screen_height = (
            self.geometry().width(),
            self.geometry().height(),
        )
        self.resize(self.screen_width * 2, self.screen_height * 2)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("./static/itaxo.jpeg"))
        self.statusBar = self.statusBar()

        mainLayout = QVBoxLayout()

        # heading
        layout1 = QHBoxLayout()
        label = QLabel("Coordinate Convertr")
        label.setStyleSheet("font: 20pt; font-weight: bold")
        layout1.addWidget(label)

        # header images
        img_label = QLabel()
        pixmap = QPixmap("static/itaxo.jpeg")
        img_label.setPixmap(pixmap)
        layout1.addWidget(img_label, alignment=Qt.AlignRight)
        mainLayout.addLayout(layout1)

        # input and output text boxes
        layout2 = QHBoxLayout()
        self.editor_input = QPlainTextEdit()
        self.editor_input.setPlaceholderText("input coordinates (in csv)")
        self.editor_output = QPlainTextEdit()
        self.editor_output.setPlaceholderText("output coordinates")
        self.editor_output.setReadOnly(True)

        layout2.addWidget(self.editor_input)
        layout2.addWidget(self.editor_output)
        mainLayout.addLayout(layout2)

        # separator radio buttons
        label_rb1 = QLabel("Separator:")
        label_rb1.setStyleSheet("font-weight: bold")

        separator_group = QButtonGroup(self)
        self.comma_rb = QRadioButton(", (comma)")
        self.semicolon_rb = QRadioButton("; (semicolon)")
        self.tab_rb = QRadioButton("\t (tab)")
        self.comma_rb.setChecked(True)
        separator_group.addButton(self.comma_rb)
        separator_group.addButton(self.semicolon_rb)
        separator_group.addButton(self.tab_rb)

        mainLayout.addWidget(label_rb1)
        mainLayout.addWidget(self.comma_rb)
        mainLayout.addWidget(self.semicolon_rb)
        mainLayout.addWidget(self.tab_rb)

        # conversion radio buttons
        label_rb2 = QLabel("Conversion:")
        label_rb2.setStyleSheet("font-weight: bold")

        conversion_group = QButtonGroup(self)
        self.ll2utm_rb = QRadioButton("LatLon to UTM [latitude, logitude]")
        self.utm2ll_rb = QRadioButton(
            "UTM to LatLon [easting, northing, zone_number, zone_letter]"
        )
        self.ll2utm_rb.setChecked(True)
        conversion_group.addButton(self.ll2utm_rb)
        conversion_group.addButton(self.utm2ll_rb)

        mainLayout.addWidget(label_rb2)
        mainLayout.addWidget(self.ll2utm_rb)
        mainLayout.addWidget(self.utm2ll_rb)

        # convert button
        self.btn = QPushButton("Convert")
        self.btn.clicked.connect(self.convert)
        mainLayout.addWidget(self.btn)

        # main container layout
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    # helper function to do the conversion
    def convert(self):
        if self.ll2utm_rb.isChecked():
            dtypes = [float, float]
            func = utm.from_latlon

        elif self.utm2ll_rb.isChecked():
            dtypes = [float, float, int, str]
            func = utm.to_latlon

        if self.comma_rb.isChecked():
            sep = ","
        elif self.semicolon_rb.isChecked():
            sep = ";"
        elif self.tab_rb.isChecked():
            sep = "\t"

        try:
            all_converted = []
            for coord in self.editor_input.toPlainText().strip().split("\n"):
                payload = [
                    dtype(param.strip().replace(",", "."))
                    for dtype, param in zip(dtypes, coord.split(sep))
                ]
                converted = func(*payload)
                converted = [
                    round(param, 3) if type(param) != str else param
                    for param in converted
                ]
                all_converted.append(sep.join([str(param) for param in converted]))
            output = "\n".join(all_converted)
            self.editor_output.setPlainText(output)

        except:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage("Incorrect input format, try again.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolkit = CoordConvertr()
    toolkit.show()
    sys.exit(app.exec_())
