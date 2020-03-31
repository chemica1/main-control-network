import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from File_class import File_class




class ComputerTimePrint(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = os.getcwd()
        self.now = time.localtime()
        self.init_the_file_class()
        self.init_the_list()
        self.start_time_comboBox_index = 0

        self.initUI()
        self.init_INFO()

    def init_the_file_class(self):
        self.Computer_name = File_class('Computer_name')
        self.Computer_start_time = File_class('Computer_start_time')
        self.Computer_end_time = File_class('Computer_end_time')
        self.Weekly_schedule = File_class('Weekly_schedule')
        self.Weekly_end_time = File_class('Weekly_end_time')
        self.Weekly_start_time = File_class('Weekly_start_time')

    def init_the_list(self):
        self.week = ('월', '화', '수', '목', '금', '토', '일')
        self.list_of_Computer_name = self.Computer_name.call_the_list()
        self.list_of_Computer_startTime =  self.Computer_start_time.call_the_list()
        self.list_of_Computer_endTime = self.Computer_end_time.call_the_list()
        self.list_of_schedule = self.Weekly_schedule.call_the_list()
        self.list_of_Weekly_endTime = self.Weekly_end_time.call_the_list()
        self.list_of_Weekly_startTime = self.Weekly_start_time.call_the_list()
        self.list_of_endTimeEdit = []
        self.list_of_startTimeEdit = []
        self.list_of_week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        self.list_of_week_checkBox = []

    def initUI(self):

        #요일 스케줄
        self.week_group = QGroupBox('전시장 운영 요일 설정')
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.checkBox_group = QButtonGroup()
        self.checkBox_group.setExclusive(False)
        for i, v in enumerate(self.list_of_week):
            self.list_of_week_checkBox.insert(i, QCheckBox(f'{v}', self))
            self.hbox.addWidget(self.list_of_week_checkBox[i])
            self.checkBox_group.addButton(self.list_of_week_checkBox[i], i)
        self.vbox.addLayout(self.hbox)
        self.checkBox_save_btn = QPushButton('스케줄 저장',self)
        self.vbox.addWidget(self.checkBox_save_btn)
        self.week_group.setLayout(self.vbox)

        # 현재 스케줄
        self.computer_schedule_group = QGroupBox('컴퓨터 시작&종료 시간 설정')

        self.computer_schedule_text_label_name = QLabel('이름')
        self.computer_schedule_text_label_startTime = QLabel('시작시간')
        self.computer_schedule_text_label_endTime = QLabel('종료시간')
        self.computer_schedule_textEdit_name = QPlainTextEdit()
        self.computer_schedule_textEdit_startTime = QPlainTextEdit()
        self.computer_schedule_textEdit_endTime = QPlainTextEdit()

        self.computer_schedule_txt_grid = QGridLayout()
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_text_label_name, 0, 0)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_text_label_startTime, 0, 1)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_text_label_endTime, 0, 2)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_textEdit_name, 1, 0)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_textEdit_startTime, 1, 1)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_textEdit_endTime, 1, 2)

        self.computer_schedule_combo = QComboBox()
        self.computer_schedule_combo.addItem('컴퓨터 목록')

        for i in self.list_of_Computer_name:
            self.computer_schedule_combo.addItem(i)

        self.computer_starttime_lineEdit = QLineEdit()
        self.computer_endtime_lineEdit = QLineEdit()

        self.computer_schedule_titleLabel = QLabel('────────────────컴퓨터 스케줄 변경────────────────')
        self.computer_schedule_titleLabel.setAlignment(Qt.AlignHCenter)
        self.computer_starttime_lineEdit.setPlaceholderText('시작 시간')
        self.computer_endtime_lineEdit.setPlaceholderText('종료 시간')
        self.computer_starttime_save_btn = QPushButton('저장', self)
        self.computer_starttime_save_btn.setEnabled(False)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_titleLabel,2,0,3,3)
        self.computer_schedule_txt_grid.addWidget(self.computer_schedule_combo, 5,0)
        self.computer_schedule_txt_grid.addWidget(self.computer_starttime_lineEdit,5,1)
        self.computer_schedule_txt_grid.addWidget(self.computer_endtime_lineEdit,5,2)
        self.computer_schedule_txt_grid.addWidget(self.computer_starttime_save_btn,6,0,7,3)

        self.computer_schedule_group.setLayout(self.computer_schedule_txt_grid)

        # 전시장 시작시간 박스
        self.start_time_group = QGroupBox('전시장 시작 시간 설정 (Projector 일괄시작)')
        self.start_time_Grid = QGridLayout()

        for i, v in enumerate(self.week):
            tp = QLabel(v)
            self.start_time_Grid.addWidget(tp, 0, i)
            tp.setAlignment(Qt.AlignCenter)

        for i in range(0, 7):
            self.list_of_startTimeEdit.insert(i, QTimeEdit(self))
            self.start_time_Grid.addWidget(self.list_of_startTimeEdit[i], 1, i)
            self.list_of_startTimeEdit[i].setDisplayFormat('hh:mm')
            temp_startTime = self.list_of_Weekly_startTime[i].split(':')
            self.list_of_startTimeEdit[i].setTime(QTime(int(temp_startTime[0]), (int(temp_startTime[1]))))  # 리스트에 저장된 현재 설정을 세팅

        self.start_time_save_btn = QPushButton('저장', self)
        self.start_time_vLayout = QVBoxLayout()
        self.start_time_vLayout.addLayout(self.start_time_Grid)
        self.start_time_vLayout.addWidget(self.start_time_save_btn)
        self.start_time_group.setLayout(self.start_time_vLayout)

        # 전시장 마감시간 박스
        self.end_time_group = QGroupBox('전시장 마감 시간 설정 (PC & Projector 일괄종료)')
        self.end_time_Grid = QGridLayout()

        for i, v in enumerate(self.week):
            tp = QLabel(v)
            self.end_time_Grid.addWidget(tp, 0, i)
            tp.setAlignment(Qt.AlignCenter)

        for i in range(0, 7):
            self.list_of_endTimeEdit.insert(i, QTimeEdit(self))
            self.end_time_Grid.addWidget(self.list_of_endTimeEdit[i], 1, i)
            self.list_of_endTimeEdit[i].setDisplayFormat('hh:mm')
            temp_endTime = self.list_of_Weekly_endTime[i].split(':')
            self.list_of_endTimeEdit[i].setTime(QTime(int(temp_endTime[0]), (int(temp_endTime[1])))) #리스트에 저장된 현재 설정을 세팅

        self.end_time_save_btn = QPushButton('저장', self)
        self.vLayout = QVBoxLayout()
        self.vLayout.addLayout(self.end_time_Grid)
        self.vLayout.addWidget(self.end_time_save_btn)
        self.end_time_group.setLayout(self.vLayout)

        # activated.connect
        self.computer_schedule_combo.activated.connect(self.combo_changed)
        self.computer_starttime_save_btn.clicked.connect(self.computer_start_time_save_btn_clicked)
        self.end_time_save_btn.clicked.connect(self.end_time_save_btn_clicked)
        self.start_time_save_btn.clicked.connect(self.start_time_save_btn_clicked)
        self.checkBox_group.buttonClicked.connect(self.radioBtn_Clicked)
        self.checkBox_save_btn.clicked.connect(self.radioBtn_saveBtn_Clicked)

        #전체 구조
        self.layout = QGridLayout()
        self.layout.addWidget(self.week_group,0, 0)
        self.layout.addWidget(self.computer_schedule_group, 1, 0)
        self.layout.addWidget(self.start_time_group, 2, 0)
        self.layout.addWidget(self.end_time_group, 3, 0)
        self.setLayout(self.layout)

    def init_INFO(self):
        self.computer_schedule_textEdit_name.setPlainText(self.Computer_name.read_the_list())
        self.computer_schedule_textEdit_startTime.setPlainText(self.Computer_start_time.read_the_list())
        self.computer_schedule_textEdit_endTime.setPlainText(self.Computer_end_time.read_the_list())
        for i, v in enumerate(self.list_of_schedule):
            if int(v) == 2:
                self.list_of_week_checkBox[i].setCheckState(2) #2가 갈매기표임

    def combo_changed(self, index):
        if not index == 0:
            self.computer_starttime_save_btn.setEnabled(True)
            self.computer_starttime_lineEdit.setInputMask('99:99:99; ')
            self.computer_endtime_lineEdit.setInputMask('99:99:99; ')
            self.start_time_comboBox_index = index

    def computer_start_time_save_btn_clicked(self):
        start_time = str(self.computer_starttime_lineEdit.text()) #착각하면 안된다. 여기서 나오는 반환값은 String이 아니라 QString이다... #temp = int(name[0])  #Qstring을 int로 바꾼다. #7/19 여기 수정해야됨. 10이 1로되는현상. #7/25 수정함 전역변수를 사용해서
        end_time = str(self.computer_endtime_lineEdit.text())
        index = self.start_time_comboBox_index - 1
        start_time.replace(" ", "")
        end_time.replace(" ", "")
        self.Computer_start_time.save_the_list(index, start_time)
        self.Computer_end_time.save_the_list(index, end_time)
        self.init_INFO()

    def end_time_save_btn_clicked(self):
        tempList = []
        for i in range(0,7):
            tempList.append(self.list_of_endTimeEdit[i].text())
        with open(f'{self.dir_path}\\txt\\Weekly_end_time.txt', 'w', encoding='UTF8') as fp:
            for i in tempList:
                data = str(i)
                fp.write(data + '\n')

    def start_time_save_btn_clicked(self):
        tempList = []
        for i in range(0, 7):
            tempList.append(self.list_of_startTimeEdit[i].text())
        with open(f'{self.dir_path}\\txt\\Weekly_start_time.txt', 'w', encoding='UTF8') as fp:
            for i in tempList:
                data = str(i)
                fp.write(data + '\n')

    def radioBtn_Clicked(self):
        tempList = []
        for cb in self.list_of_week_checkBox:
            tempList.append(cb.checkState())
        self.list_of_schedule = tempList

    def radioBtn_saveBtn_Clicked(self):
        with open(f'{self.dir_path}\\txt\\Weekly_schedule.txt', 'w', encoding='UTF8') as fp:
            for i in self.list_of_schedule:
                data = str(i) #str을 붙여줘야한다. 왜냐하면 저 스케쥴 리스트에 든 0은 null로 간주하기 때문이다.
                fp.write(data + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ComputerTimePrint()
    sys.exit(app.exec_())