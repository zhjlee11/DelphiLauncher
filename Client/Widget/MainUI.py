import sys, threading, glob, random, time
import minecraft_launcher_lib
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QFileDialog, \
    QPushButton, QDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLayout, QProgressBar
from PyQt5.QtGui import QIcon, QColor, QPen, QPixmap, QIntValidator
from qt_material import apply_stylesheet

from Install import Install
from Widget.LauncherListViewItem import LauncherListViewItem
from data.DB import load_launcher_profile



class MainUI(QWidget):
    def __init__(self, width=1280, height=678, parent=None):
        super().__init__()
        self.width = width
        self.height = height
        self.isInstalling = False
        self.parent = parent

        self.initUI()



    def initUI(self):
        self.mainlayout = QGridLayout()


        groupbox_install = self.installUI()
        groupbox_select = self.selectUI()


        self.mainlayout.addWidget(groupbox_install, 0, 0)
        self.mainlayout.addWidget(groupbox_select, 0, 1)

        self.setLayout(self.mainlayout)

        self.setWindowTitle('델포이 런처')
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(self.width, self.height)
        self.show()

    def installUI(self):
        groupbox_install = QGroupBox("설치")
        groupbox_install

        install_input_layout = QGridLayout()

        install_input_layout.addWidget(QLabel("공유 서버 주소 : "), 0, 0)
        install_input_layout.addWidget(QLabel("공유 서버 포트 : "), 1, 0)

        self.serverIP_Input = QLineEdit()
        install_input_layout.addWidget(self.serverIP_Input, 0, 1)

        self.serverPORT_Input = QLineEdit()
        self.onlyInt = QIntValidator()
        self.serverPORT_Input.setValidator(self.onlyInt)
        install_input_layout.addWidget(self.serverPORT_Input, 1, 1)


        self.install_button = QPushButton("설치")
        self.install_button.clicked.connect(self.install_file)

        install_layout = QVBoxLayout()
        install_layout.addLayout(install_input_layout)
        install_layout.addWidget(self.install_button)

        groupbox_install.setLayout(install_layout)

        return groupbox_install

    def selectUI(self):
        groupbox_select = QGroupBox("패키지")

        self.listwidget = QListWidget()
        for dict in load_launcher_profile(db_path=".\\data\\DelphiDB.db").values():
            itemN = QListWidgetItem(self.listwidget)

            itemwidget = LauncherListViewItem(dict, parent=self)
            apply_stylesheet(itemwidget, theme=self.parent.theme)
            itemwidget.setContentsMargins(0, 0, 0, 0)
            itemN.setSizeHint(itemwidget.sizeHint())

            self.listwidget.addItem(itemN)
            self.listwidget.setItemWidget(itemN, itemwidget)

        select_layout = QVBoxLayout()
        select_layout.addWidget(self.listwidget)

        groupbox_select.setLayout(select_layout)
        return groupbox_select

    def install_file(self):
        ip = self.serverIP_Input.text()
        port = self.serverPORT_Input.text()

        if not self.isInstalling:
            if ip==None or ip=="":
                QMessageBox.warning(self, '경고', '공유 서버 주소를 입력해주세요.', QMessageBox.Yes, QMessageBox.Yes)
            elif port==None or port=="":
                QMessageBox.warning(self, '경고', '공유 서버 포트를 입력해주세요.', QMessageBox.Yes, QMessageBox.Yes)
            else :
                self.isInstalling = True
                result = Install.install(ip, int(port), ui=self)
                self.isInstalling = False
                if result == None:
                    QMessageBox.information(self, '경고', '서버 주소 및 포트가 잘못되었습니다.', QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, '정보', result['package_name']+'이/가 성공적으로 설치되었습니다.', QMessageBox.Yes, QMessageBox.Yes)
        else :
            QMessageBox.information(self, '경고', '이미 다운받고 있는 패키지가 존재합니다.', QMessageBox.Yes, QMessageBox.Yes)
        self.Update()

    def Update(self):
        self.listwidget.clear()
        for dict in load_launcher_profile(db_path=".\\data\\DelphiDB.db").values():
            itemN = QListWidgetItem(self.listwidget)

            itemwidget = LauncherListViewItem(dict, parent=self)
            apply_stylesheet(itemwidget, theme=self.parent.theme)
            itemwidget.setContentsMargins(0, 0, 0, 0)
            itemN.setSizeHint(itemwidget.sizeHint())

            self.listwidget.addItem(itemN)
            self.listwidget.setItemWidget(itemN, itemwidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
