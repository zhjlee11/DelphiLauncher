import subprocess
import sys

import minecraft_launcher_lib

from Install import Install
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from Widget import LoginUI, MainUI

class LauncherConrtoller:
    def __init__(self):
        self.login_data = None
        self.launch_profile = None
        self.theme = ".\\theme\\Dark.qss"

    def getStyleSheet(self):
        stream = QtCore.QFile(self.theme)
        stream.open(QtCore.QIODevice.ReadOnly)
        return QtCore.QTextStream(stream).readAll()

    def show_login(self):
        self.login = LoginUI.LoginUI(parent=self)
        self.login.setStyleSheet(self.getStyleSheet())
        self.login.show()

    def show_main(self):
        self.window = MainUI.MainUI(parent=self)
        self.window.setStyleSheet(self.getStyleSheet())
        self.login.close()
        self.window.show()

    def run_game(self, optional_options={}):

        options = {
            "username": self.login_data["selectedProfile"]["name"],
            "uuid": self.login_data["selectedProfile"]["id"],
            "token": self.login_data["accessToken"],
            "nativesDirectory": ".\\natives"
        }
        options.update(optional_options)

        try:
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(self.launch_profile['version_name'], self.launch_profile['minecraft_path'], options)
        except FileNotFoundError as e:
            QMessageBox.warning(self, '경고', '버전 이름이나 셋팅 파일 경로가 잘못되었습니다.\n삭제 후 재설치에도 해결되지 않을 경우,\n 셋팅 공유 서버 운영자분께 연락을 드려 주세요,', QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
        self.window.close()
        subprocess.call(minecraft_command)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    contorller = LauncherConrtoller()
    contorller.show_login()
    app.exec_()