import sys
from PySide6 import QtWidgets
from gui.main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("G4Cam GUI-Only")
    app.setStyle("Fusion")
    win = MainWindow()
    win.resize(1200, 720)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
