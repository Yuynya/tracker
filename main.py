import mouse
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

name=''
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(718, 558)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.loadProgressBar.setGeometry(QtCore.QRect(160, 420, 371, 21))
        self.loadProgressBar.setProperty("value", 0)
        self.loadProgressBar.setObjectName("loadProgressBar")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(490, 460, 171, 21))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.start)
        '''self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 671, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 671, 411))
        self.graphicsView.setObjectName("graphicsView")'''
        self.lbl = QtWidgets.QLabel(self)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главная"))
        self.startButton.setText(_translate("MainWindow", "Запуск программы управления"))
    async def start(self):
        print('нажатие прошло')
        mouse.mouseMenegement()
        self.showCam()

    def showCam(self):
        print('вызов картинки')
        name=f'{mouse.indexImg}.jpg'
        print(name)
        self.pix = QtGui.QPixmap(name)
        print(45)
        self.lbl.setPixmap(self.pix)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Ui_MainWindow()
    application.show()
    sys.exit(app.exec())