import sys, threading, requests, time
import server
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QFileDialog, \
    QPushButton, QDialog, QMessageBox, QTabWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen


class Server(QWidget):
    def __init__(self):
        super().__init__()
        self.minecraft_path = ""
        self.isServerOn = False
        self.sharemode = 0 #0:파일 호스팅, 1:구글 드라이브
        self.initUI()

    def shareMode(self, ind):
        self.sharemode = ind

    def selectMinecraftPath(self):
        self.minecraft_path = QFileDialog.getOpenFileName(self, 'Open file', './minecraft_file', 'zip File(*.zip)')[0]
        self.minecraftpath_button.setText(self.minecraft_path)
        
    def runServer(self):
        if self.isServerOn:
            QMessageBox.warning(self, '경고', '서버가 이미 가동되어 있습니다. 재가동을 하려면 프로그램을 껐다 켜주세요.', QMessageBox.Yes, QMessageBox.Yes)
            return
        else:
            server_ip = self.serverip_input.text()
            server_port = self.serverport_input.text()
            package_name = self.packagename_input.text()
            version_name = self.versionname_input.text()
            minecraft_path = self.minecraft_path
            driveid = self.driveid.text()

            if server_ip == "" or server_ip == None:
                QMessageBox.warning(self, '경고', '서버 ip를 채워주세요.', QMessageBox.Yes, QMessageBox.Yes)
                return
            elif server_port == "" or server_port == None:
                QMessageBox.warning(self, '경고', '서버 포트를 채워주세요.', QMessageBox.Yes, QMessageBox.Yes)
                return
            elif package_name == "" or package_name == None:
                QMessageBox.warning(self, '경고', '패키지 이름을 채워주세요.', QMessageBox.Yes, QMessageBox.Yes)
                return
            elif version_name == "" or version_name == None:
                QMessageBox.warning(self, '경고', '버전 이름을 채워주세요.', QMessageBox.Yes, QMessageBox.Yes)
                return
            elif self.sharemode == 0:
                if minecraft_path == "" or minecraft_path == None:
                    QMessageBox.warning(self, '경고', 'Minecraft 파일 경로를 선택해주세요.', QMessageBox.Yes, QMessageBox.Yes)
                    return
            elif self.sharemode == 1:
                if driveid == "" or driveid == None:
                    QMessageBox.warning(self, '경고', '구글 드라이브 ID를 입력해주세요', QMessageBox.Yes, QMessageBox.Yes)
                    return

            reply = QMessageBox.question(self, '경고', '서버를 가동할까요?\n서버 가동 후에 종료시에는 프로그램을 종료해주시면 됩니다.', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.isServerOn = True
                print(self.sharemode)
                if self.sharemode == 0:
                    flaskThread = threading.Thread(target=server.run, args=(server_ip, server_port, package_name, version_name, self.sharemode, minecraft_path))
                elif self.sharemode == 1:
                    flaskThread = threading.Thread(target=server.run, args=(server_ip, server_port, package_name, version_name, self.sharemode, driveid))
                flaskThread.daemon = True
                flaskThread.start()
            else :
                return

    def initUI(self):
        maingrid = QGridLayout()

        serverset_groupbox = QGroupBox('서버 셋팅')
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel('서버 IP :'), 0, 0)
        grid.addWidget(QLabel('서버 포트 :'), 1, 0)
        self.serverip_input = QLineEdit()
        self.serverport_input = QLineEdit()
        grid.addWidget(self.serverip_input, 0, 1)
        grid.addWidget(self.serverport_input, 1, 1)
        serverset_groupbox.setLayout(grid)

        shareset_groupbox = QGroupBox('공유 셋팅')
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel('패키지 이름 :'), 0, 0)
        grid.addWidget(QLabel('버전 이름 :'), 1, 0)
        grid.addWidget(QLabel('minecraft 파일 :'), 2, 0)
        self.packagename_input = QLineEdit()
        self.versionname_input = QLineEdit()
        self.minecraftpath_button = QPushButton("파일 링크")
        self.minecraftpath_button.clicked.connect(self.selectMinecraftPath)
        self.driveid = QLineEdit()

        self.tab = QTabWidget()

        tab1 = QWidget()
        tab1_layout = QHBoxLayout()
        tab1_layout.addWidget(QLabel("압축 파일 경로 :"))
        tab1_layout.addWidget(self.minecraftpath_button)
        tab1.setLayout(tab1_layout)
        tab2 = QWidget()
        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(QLabel("구글 드라이브 ID : "))
        tab2_layout.addWidget(self.driveid)
        tab2.setLayout(tab2_layout)
        self.tab.addTab(tab1, "파일 호스팅")
        self.tab.addTab(tab2, "구글 드라이브")

        self.tab.currentChanged.connect(self.shareMode)


        grid.addWidget(self.packagename_input, 0, 1)
        grid.addWidget(self.versionname_input, 1, 1)
        grid.addWidget(self.tab, 2, 1)
        shareset_groupbox.setLayout(grid)

        self.serverrun_button = QPushButton("서버 가동")
        self.serverrun_button.clicked.connect(self.runServer)

        maingrid.addWidget(serverset_groupbox, 0, 0)
        maingrid.addWidget(shareset_groupbox, 1, 0)
        maingrid.addWidget(self.serverrun_button, 2, 0)


        self.setLayout(maingrid)

        self.setWindowTitle('DelphiLauncher Server')
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(600, 500)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Server()
    sys.exit(app.exec_())