import sys, threading, requests, time
import server
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QFileDialog, \
    QPushButton, QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QPen


class Server(QWidget):
    def __init__(self):
        super().__init__()
        self.minecraft_path = ""
        self.isServerOn = False
        self.initUI()
        

    def draw_rect(self, qp):
        qp.setBrush(QColor(255, 255, 255))
        qp.setPen(QPen(QColor(60, 60, 60), 3))
        qp.drawRect(20, 20, 100, 100)

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
            elif minecraft_path == "" or minecraft_path == None:
                QMessageBox.warning(self, '경고', 'Minecraft 파일 경로를 선택해주세요.', QMessageBox.Yes, QMessageBox.Yes)
                return

            reply = QMessageBox.question(self, '경고', '서버를 가동할까요?\n서버 가동 후에 종료시에는 프로그램을 종료해주시면 됩니다.', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.isServerOn = True
                flaskThread = threading.Thread(target=server.run, args=(server_ip, server_port, package_name, version_name, minecraft_path))
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
        grid.addWidget(QLabel('minecraft 파일 경로 :'), 2, 0)
        self.packagename_input = QLineEdit()
        self.versionname_input = QLineEdit()
        self.minecraftpath_button = QPushButton("파일 선택")
        self.minecraftpath_button.clicked.connect(self.selectMinecraftPath)
        grid.addWidget(self.packagename_input, 0, 1)
        grid.addWidget(self.versionname_input, 1, 1)
        grid.addWidget(self.minecraftpath_button, 2, 1)
        shareset_groupbox.setLayout(grid)

        self.serverrun_button = QPushButton("서버 가동")
        self.serverrun_button.clicked.connect(self.runServer)

        maingrid.addWidget(serverset_groupbox, 0, 0)
        maingrid.addWidget(shareset_groupbox, 1, 0)
        maingrid.addWidget(self.serverrun_button, 2, 0)
        
        

        self.setLayout(maingrid)

        self.setWindowTitle('DelphiLauncher Server')
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(600, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Server()
    sys.exit(app.exec_())