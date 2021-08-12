import sys, os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QErrorMessage,
    QWidget,
    QRadioButton,
    QLabel,
    QPlainTextEdit,
    QToolBar,
    QHBoxLayout,
    QVBoxLayout,
    QAction,
    QFileDialog,
    QMessageBox,
    QDialog,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence, QPixmap
import utm


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Coord Convertr"
        self.screen_width, self.screen_height = (
            self.geometry().width,
            self.geometry().height(),
        )
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("./static/itaxo.jpeg"))
        self.statusBar = self.statusBar()

        file_menu = self.menuBar().addMenu("&File")

        mainLayout = QVBoxLayout()

        layout1 = QHBoxLayout()
        self.editor_input = QPlainTextEdit()
        self.editor_input.setPlaceholderText("input coordinates (in csv)")
        self.editor_output = QPlainTextEdit()
        self.editor_output.setPlaceholderText("output coordinates")
        self.editor_output.setReadOnly(True)

        # self.editor.setFont(fixedFont)

        layout1.addWidget(self.editor_input)
        layout1.addWidget(self.editor_output)

        self.ll2utm_rb = QRadioButton("LatLon to UTM [latitude, logitude]")
        self.utm2ll_rb = QRadioButton(
            "UTM to LatLon [easting, northing, zone_number, zone_letter]"
        )
        self.btn = QPushButton("Convert")
        self.btn.clicked.connect(self.convert)

        mainLayout.addLayout(layout1)
        mainLayout.addWidget(self.ll2utm_rb)
        mainLayout.addWidget(self.utm2ll_rb)
        mainLayout.addWidget(self.btn)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def convert(self):
        if self.ll2utm_rb.isChecked():
            dtypes = [float, float]
            func = utm.from_latlon

        elif self.utm2ll_rb.isChecked():
            dtypes = [float, float, int, str]
            func = utm.to_latlon

        try:
            all_converted = []
            for coord in self.editor_input.toPlainText().strip().split("\n"):
                payload = [
                    dtype(param.strip())
                    for dtype, param in zip(dtypes, coord.split(","))
                ]
                converted = func(*payload)
                all_converted.append(",".join([str(param) for param in converted]))

            output = "\n".join(all_converted)
            self.editor_output.setPlainText(output)

        except:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage("Incorrect input format, try again.")

    def openAbout(self):
        mydialog = QDialog()
        mydialog.setWindowTitle("About Us")
        label = QLabel(mydialog)
        label.setText(
            "iTaxotools is a bioinformatic platform designed to facilitate the core work of taxonomists, that is, delimiting, diagnosing and describing species."
        )
        label.adjustSize()
        label.move(100, 60)
        mydialog.setWindowModality(Qt.ApplicationModal)
        mydialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolkit = AppDemo()
    toolkit.show()
    sys.exit(app.exec_())
