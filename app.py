import sys
from PySide6 import QtWidgets, QtCore, QtGui

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("G4Cam")
    app.setStyle("Fusion")
    
    # Show splash screen while loading
    splash_pix = QtGui.QPixmap(400, 200)
    splash_pix.fill(QtGui.QColor(30, 30, 30))
    
    painter = QtGui.QPainter(splash_pix)
    painter.setPen(QtGui.QColor(255, 255, 255))
    font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
    painter.setFont(font)
    painter.drawText(splash_pix.rect(), QtCore.Qt.AlignCenter, "G4Cam\nLoading...")
    painter.end()
    
    splash = QtWidgets.QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()
    
    # Import heavy modules after showing splash
    splash.showMessage("Loading GUI components...", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtGui.QColor(200, 200, 200))
    app.processEvents()
    
    from gui.main_window import MainWindow
    
    splash.showMessage("Initializing window...", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtGui.QColor(200, 200, 200))
    app.processEvents()
    
    win = MainWindow()
    win.resize(1200, 720)
    
    splash.finish(win)
    win.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()