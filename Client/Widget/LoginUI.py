import sys, threading, glob, random, time
import minecraft_launcher_lib
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QFileDialog, \
    QPushButton, QDialog, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QPixmap

def loadBackgroudImage():
    path = ".\\resources\\background\\*"
    file_list = glob.glob(path)
    file_list_py = [file for file in file_list if file.endswith(".jpg") or file.endswith(".png")]
    return file_list_py

class LoginUI(QWidget):
    def __init__(self, width=1280, height=678, parent=None):
        super().__init__()
        self.width = width
        self.height = height
        self.parent = parent
        self.backgroundlist = loadBackgroudImage()

        self.initUI()

        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.backgroundUpdate)
        self.timer.start()

    def initUI(self):
        self.setBackground()
        self.loginWindow()

        self.setWindowTitle('델포이 런처')
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(self.width, self.height)
        self.show()

    def setBackground(self):
        backgroundPixmap = QPixmap()
        backgroundPixmap.scaled(self.maximumWidth(), self.maximumHeight())
        backgroundPixmap.load(random.choice(self.backgroundlist))

        self.backgroundLabel = QLabel("", self)
        self.backgroundLabel.move(0, 0)
        self.backgroundLabel.setFixedWidth(self.maximumWidth())
        self.backgroundLabel.setFixedHeight(self.maximumHeight())
        self.backgroundLabel.setPixmap(backgroundPixmap)

    def loginWindow(self):
        maingroup = QGroupBox("", self)
        maingroup.move(680, 100)
        maingroup.setStyleSheet("color: white;"
                        "background-color: rgba( 0, 0, 0, 0.7 );"
                                "margin: 10px;")


        loginGrid = QGridLayout()

        logolabel = QLabel()
        logolabel.setStyleSheet("color: white;"
                        "background-color: rgba( 0, 0, 0, 0 );")
        logopixmap = QPixmap()
        logopixmap.load(".\\resources\\logo\\logo_white.png")
        logopixmap.scaledToWidth(400)
        logolabel.setPixmap(logopixmap)

        commentlabel = QLabel("마인크래프트 런처의 새로운 패러다임,\n델포이에 오신 것을 환영합니다.")
        commentlabel.setAlignment(Qt.AlignCenter)
        commentlabel.setStyleSheet("color: white;"
                                "background-color: rgba( 0, 0, 0, 0 );")

        idlabel = QLabel('ID :')
        idlabel.setStyleSheet("color: white;"
                       "background-color: rgba( 0, 0, 0, 0 );")

        pwlabel = QLabel('Password :')
        pwlabel.setStyleSheet("color: white;"
                       "background-color: rgba( 0, 0, 0, 0 );")

        loginGrid.addWidget(idlabel, 0, 0)
        loginGrid.addWidget(pwlabel, 1, 0)

        self.login_inputID = QLineEdit()
        self.login_inputPW = QLineEdit()
        self.login_inputPW.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")

        self.login_button.setStyleSheet("color: white;"
                       "background-color: rgba( 0, 0, 0, 0 );"
                                        "border-style: solid;"
                                        "border-width: 2px;"
                                        "border-color: #FFFFFF;"
                                        "border-radius: 3px")
        self.login_button.clicked.connect(self.login)

        loginGrid.addWidget(self.login_inputID, 0, 1)
        loginGrid.addWidget(self.login_inputPW, 1, 1)

        copyright_text = QLabel('Copyright 2021. Laplace. All rights reserved.')
        copyright_text.setStyleSheet("color: white;"
                       "background-color: rgba( 0, 0, 0, 0 );")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(logolabel)
        vbox.addWidget(commentlabel)
        vbox.addLayout(loginGrid)
        vbox.addWidget(self.login_button)
        vbox.addWidget(copyright_text)
        vbox.addStretch(1)

        maingroup.setLayout(vbox)


    def backgroundUpdate(self):
        backgroundPixmap = QPixmap()
        backgroundPixmap.scaled(self.width, self.height)
        backgroundPixmap.load(random.choice(self.backgroundlist))
        self.backgroundLabel.setPixmap(backgroundPixmap)

    def login(self):
        id = self.login_inputID.text()
        pw = self.login_inputPW.text()
        if id == None or id == "" :
            QMessageBox.warning(self, '경고', 'ID를 입력해주세요.', QMessageBox.Yes, QMessageBox.Yes)
        elif pw == None or pw == "" :
            QMessageBox.warning(self, '경고', '비밀번호를 입력해주세요.', QMessageBox.Yes, QMessageBox.Yes)
        else:
            login_data = minecraft_launcher_lib.account.login_user(id, pw)
            if "error" not in list(login_data.keys()):
                self.parent.login_data = login_data
                self.parent.show_main()
            else:
                QMessageBox.warning(self, '경고', 'ID 및 비밀번호가 잘못되었습니다.', QMessageBox.Yes, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginUI()
    sys.exit(app.exec_())