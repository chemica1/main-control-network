import sys, os
from PyQt5.QtWidgets import *
from File_class import File_class


class ProjectorInfoPrint(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = os.getcwd()

        self.list_of_pj_name = []
        self.list_of_pj_IP = []
        self.init_file_class()
        self.init_pjInfo_list()
        self.input_mask_index = 0

        self.initUI()
        self.init_INFO()

    def init_file_class(self):
        self.Projector_name = File_class('Projector_name') # IP 클래스
        self.Projector_IP = File_class('Projector_IP')  # MAC 클래스

    def init_pjInfo_list(self):
        self.list_of_pj_name = self.Projector_name.call_the_list()  # IP 리스트
        self.list_of_pj_IP = self.Projector_IP.call_the_list()  # MAC 리스트

    def init_INFO(self):
        self.name_txt.setPlainText(self.Projector_name.read_the_list())
        self.IP_txt.setPlainText(self.Projector_IP.read_the_list())

    def initUI(self):
        # IP MAC 변경
        self.input_mask_group = QGroupBox('프로젝터 정보 변경')

        self.input_mask_label = QLabel('프로젝터 목록 :')
        self.input_mask_cb = QComboBox()
        self.input_mask_cb.addItem('목록')
        for i in self.list_of_pj_name:
            self.input_mask_cb.addItem(i)
        self.input_mask_name = QLineEdit()
        self.input_mask_IP = QLineEdit()
        self.save_btn = QPushButton('저장', self)
        self.save_btn.setEnabled(False)

        self.input_mask_name.setPlaceholderText('프로젝터 이름')
        self.input_mask_IP.setPlaceholderText('IP 주소')

        self.input_mask_layout = QGridLayout()
        self.input_mask_layout.addWidget(self.input_mask_label, 0, 0)
        self.input_mask_layout.addWidget(self.input_mask_cb, 0, 1)
        self.input_mask_layout.addWidget(self.save_btn, 0, 2)
        self.input_mask_layout.addWidget(self.input_mask_name, 1, 0)
        self.input_mask_layout.addWidget(self.input_mask_IP, 1, 1)

        self.input_mask_group.setLayout(self.input_mask_layout)

        # IP MAC 정보
        self.txt_group = QGroupBox('현재 프로젝터 정보')

        self.text_label_name = QLabel('이름')
        self.text_label_IP = QLabel('IP')
        self.text_label_MAC = QLabel('MAC')
        self.name_txt = QPlainTextEdit()
        self.IP_txt = QPlainTextEdit()

        self.txt_grid = QGridLayout()
        self.txt_grid.addWidget(self.text_label_name, 0, 0)
        self.txt_grid.addWidget(self.text_label_IP, 0, 5)
        self.txt_grid.addWidget(self.name_txt, 1, 0)
        self.txt_grid.addWidget(self.IP_txt, 1, 5)
        self.txt_group.setLayout(self.txt_grid)

        # activated.connect
        self.input_mask_cb.activated.connect(self.input_mask_changed)
        self.save_btn.clicked.connect(self.btn_clicked)

        #전체 구조
        self.layout = QGridLayout()
        self.layout.addWidget(self.txt_group, 0, 0)
        self.layout.addWidget(self.input_mask_group, 1, 0)
        self.setLayout(self.layout)

        self.setWindowTitle('프로젝터 변경')

    def input_mask_changed(self, index):
        print(f'{index}번 프로젝터를 변경합니다.')
        if not index == 0:
            self.save_btn.setEnabled(True)
            self.input_mask_name.setInputMask(f'{index}. xxxxxxxxxxxx; ')
            self.input_mask_IP.setInputMask('xxx.xxx.xxx.xxx; ')
            self.input_mask_index = index

    def btn_clicked(self):
        name = self.input_mask_name.text() #착각하면 안된다. 여기서 나오는 반환값은 String이 아니라 QString이다...
        IP = self.input_mask_IP.text()
        IP.replace(" ", "")
        index = self.input_mask_index - 1

        self.Projector_name.save_the_list(index, name)
        self.Projector_IP.save_the_list(index, IP)
        self.init_INFO()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectorInfoPrint()
    sys.exit(app.exec_())