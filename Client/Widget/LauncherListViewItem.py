import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QFileDialog, \
    QPushButton, QDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QInputDialog, QLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QPixmap, QIntValidator
from data.DB import *

class LauncherListViewItem(QWidget):
    def __init__(self, launcher_profile, width=1280, height=678, parent=None):
        super().__init__()
        self.width = width
        self.height = height
        self.parent = parent

        self.launcher_profile = launcher_profile
        self.initUI()

    def initUI(self):
        mainlayout = QVBoxLayout()
        mainlayout.setSizeConstraint(QLayout.SetFixedSize)

        package_name_label = QLabel(self.launcher_profile['package_name'])
        font_title = package_name_label.font()
        font_title.setPointSize(30)
        package_name_label.setFont(font_title)

        version_name_label = QLabel("버전 : {0}".format(self.launcher_profile['version_name']))
        minecraft_path_label = QLabel("경로 : {0}".format(self.launcher_profile['minecraft_path']))

        rename_button = QPushButton("패키지 이름 수정")
        remove_button = QPushButton("패키지 제거")
        play_button = QPushButton("패키지 플레이")

        rename_button.clicked.connect(self.rename)
        remove_button.clicked.connect(self.remove)
        play_button.clicked.connect(self.play)

        button_layout = QHBoxLayout()
        button_layout.addWidget(rename_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(play_button)

        mainlayout.addWidget(package_name_label)
        mainlayout.addWidget(version_name_label)
        mainlayout.addWidget(minecraft_path_label)
        mainlayout.addLayout(button_layout)

        self.setLayout(mainlayout)



    def rename(self):
        if not self.parent.isInstalling:
            newname, ok = QInputDialog().getText(self, "이름", "수정할 패키지 이름을 입력해주세요 :")
    
            if ok:
                if newname==None:
                    QMessageBox.information(self, '경고', '공백은 이름으로 사용할 수 없습니다.', QMessageBox.Yes, QMessageBox.Yes)
                elif newname=="":
                    QMessageBox.information(self, '경고', '공백은 이름으로 사용할 수 없습니다.', QMessageBox.Yes, QMessageBox.Yes)
                else:
                    rename_launcher_profile(self.launcher_profile['id'], newname)
            else:
                QMessageBox.information(self, '경고', '예상하지 못한 오류가 발생하였습니다.', QMessageBox.Yes, QMessageBox.Yes)
            self.parent.Update()
        else :
            QMessageBox.information(self, '경고', '다운받고 있는 패키지가 존재합니다.\n다운이 끝난 후에 수정이 가능합니다.', QMessageBox.Yes, QMessageBox.Yes)


    def remove(self):
        if not self.parent.isInstalling:
            removeBool = QMessageBox.information(self, '경고', '해당 패키지를 정말로 삭제하시겠습니까?', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
            if removeBool == QMessageBox.Yes:
                remove_launcher_profile(self.launcher_profile['id'])
            self.parent.Update()
        else :
            QMessageBox.information(self, '경고', '다운받고 있는 패키지가 존재합니다.\n다운이 끝난 후에 제거가 가능합니다.', QMessageBox.Yes, QMessageBox.Yes)

    def play(self):
        if not self.parent.isInstalling :
            self.parent.parent.launch_profile = self.launcher_profile
            self.parent.parent.run_game()
        else :
            QMessageBox.information(self, '경고', '다운받고 있는 패키지가 존재합니다.\n다운이 끝난 후에 플레이가 가능합니다.', QMessageBox.Yes, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LauncherListViewItem({'id': 0, 'package_name': 'test1', 'version_name': 'test2', 'minecraft_path': './minecraft_files/0'})
    ex.show()
    sys.exit(app.exec_())


