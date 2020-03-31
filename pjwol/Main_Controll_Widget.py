from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Magic_Packet import send_packet_class
from Remote_Off import Remote_off_class
from pj_Class import ProjectorClass
import sys, threading, subprocess, platform,os
from File_class import File_class
from pypjlink import Projector
import time
from datetime import timedelta


class Controll_Widget(QWidget):
    now = time.localtime()

    def __del__(self):
        self.timer_status.stop()
        self.timer_sec.stop()

    def __init__(self):
        super().__init__()
        self.dir_path = os.getcwd()
        self.init_file_class()
        self.init_Info_list()
        self.is_it_openTime = False
        self.quit_flag = 0   #종료시간 이후에도 킬 수 있게 만든 장치
        self.quit_flag2 = 0  #종료명령을 한번만 하게 하려고..

        self.computer_name = []  #원소가 없는 상태에서 = 연산자로 대입 불가능함. append나 insert 둘 중 하나로 해야됨.
        self.computer_status = []
        self.computer_on_btn = []
        self.computer_off_btn = []

        self.projector_name = []  #원소가 없는 상태에서 = 연산자로 대입 불가능함. append나 insert 둘 중 하나로 해야됨.
        self.projector_status = []
        self.projector_on_btn = []
        self.projector_off_btn = []

        self.init_class()
        self.initUI()
        self.initBtn()
        self.initTd()
        if self.check_schedule():
            self.initTimerRoutine()
        else :
            print(f'오늘은 전시장 오픈날이 아니므로 루틴을 실행시키지 않습니다.')

    def init_class(self):

        self.list_of_packetClass = []
        self.list_of_psexecClass = []
        for i in range (0,len(self.list_of_ComName)):
            self.list_of_psexecClass.insert(i, Remote_off_class(self.list_of_ComIP[i]))
        for i in range (0,len(self.list_of_ComName)):
            self.list_of_packetClass.insert(i, send_packet_class(self.list_of_MAC[i]))
        for i in range (0,len(self.list_of_PjName)):
            self.list_of_pjClass.insert(i, ProjectorClass(self.list_of_PjIp[i]))

    def init_file_class(self):

        self.Computer_IP = File_class('Computer_IP')  # IP 클래스
        self.Computer_MAC = File_class('Computer_MAC')  # MAC 클래스
        self.Computer_name = File_class('Computer_name')  # 컴퓨터 클래스
        self.Projector_name = File_class('Projector_name')  # 프로젝터 name 클래스
        self.Projector_IP = File_class('Projector_IP')  # 프로젝터 IP 클래스
        self.Weekly_schedule = File_class('Weekly_schedule')  # 주간 스케줄 클래스
        self.Computer_start_time = File_class('Computer_start_time')  # start_time 클래스
        self.Computer_end_time = File_class('Computer_end_time')  # end_time 클래스

    def init_Info_list(self):

        self.list_of_pjClass = []
        self.list_of_ComName = self.Computer_name.call_the_list()   #컴퓨터 리스트
        self.list_of_ComIP = self.Computer_IP.call_the_list()       #컴퓨터 IP 리스트
        self.list_of_MAC = self.Computer_MAC.call_the_list()        #컴퓨터 MAC 리스트
        self.list_of_PjName = self.Projector_name.call_the_list()   #프로젝터 name 리스트
        self.list_of_PjIp = self.Projector_IP.call_the_list()       #프로젝터 IP 리스트
        self.list_of_week_TF = self.Weekly_schedule.call_the_list()  # 주간 스케줄
        self.list_of_computer_start_time = self.Computer_start_time.call_the_list()  # start_time 리스트
        self.list_of_computer_end_time = self.Computer_end_time.call_the_list()  # end_time 리스트
        self.museum_start_time = File_class('Weekly_start_time').call_the_list()[self.now.tm_wday].split(':')  # 전시장 오픈시간 리스트
        self.museum_end_time = File_class('Weekly_end_time').call_the_list()[self.now.tm_wday].split(':')  # 전시장 마감시간 리스트

    def initUI(self):

        #전체 제어 박스
        '''
        self.whole_box = QGroupBox('전체 제어')

        self.all_button = QPushButton('All Power On', self) #뒤에 self는 속할 부모클래스를 지정해줌
        self.all_button.setStyleSheet("background-color: gray; font: bold 14px;  padding: 6px; color : white; ") # 보더 스타일시트를 변경 할경우 누르는 이펙트가 사라지게 된다.
        self.all_button.clicked.connect(self.All_btn_clicked)

        self.whole_layout = QHBoxLayout()
        self.whole_layout.addStretch(1)
        self.whole_layout.addWidget(self.all_button)
        self.whole_layout.addStretch(1)
        self.whole_box.setLayout(self.whole_layout)
        '''

        #컴퓨터 리스트 박스
        self.com_power_box = QGroupBox('컴퓨터 모니터링')

        #컴퓨터 라벨과 버튼들
        for i in range(0, len(self.list_of_ComName)):
            self.computer_name.insert(i, QLabel(self.list_of_ComName[i], self))
            self.computer_name[i].setStyleSheet("bold 11px; ")
            self.computer_status.insert(i, QLabel())
            self.computer_on_btn.insert(i, QPushButton('Power on', self))
            self.computer_off_btn.insert(i, QPushButton('Power off', self))

        self.computer_layout = QGridLayout()

        for i in range(0, len(self.list_of_ComName)):
            self.computer_layout.addWidget(self.computer_name[i], i, 0)
            self.computer_layout.addWidget(self.computer_status[i], i, 1)
            self.computer_layout.addWidget(self.computer_on_btn[i], i, 2)
            self.computer_layout.addWidget(self.computer_off_btn[i], i, 3)

        self.com_power_box.setLayout(self.computer_layout)

        # 프로젝터 리스트 박스
        self.projector_power_box = QGroupBox('프로젝터 모니터링')

        # 프로젝터 라벨과 버튼들
        for i in range(0, len(self.list_of_PjName)):
            self.projector_name.insert(i, QLabel(self.list_of_PjName[i], self))
            self.projector_name[i].setStyleSheet("bold 11px; ")
            self.projector_status.insert(i, QLabel())
            self.projector_on_btn.insert(i, QPushButton('Lamp on', self))
            self.projector_off_btn.insert(i, QPushButton('Lamp off', self))

        self.projector_layout = QGridLayout()

        for i in range(0, len(self.list_of_PjName)):
            self.projector_layout.addWidget(self.projector_name[i], i, 0)
            self.projector_layout.addWidget(self.projector_status[i], i, 1)
            self.projector_layout.addWidget(self.projector_on_btn[i], i, 2)
            self.projector_layout.addWidget(self.projector_off_btn[i], i, 3)

        self.projector_power_box.setLayout(self.projector_layout)

        self.HGrid = QGridLayout()
        self.HGrid.addWidget(self.com_power_box,0, 0)
        self.HGrid.addWidget(self.projector_power_box,0, 1)

        self.Totallayout = QVBoxLayout()
        ##self.Totallayout.addWidget(self.whole_box) 전체제어 layout.. 불필요해서 일단 뺌(12/26)
        self.Totallayout.addLayout(self.HGrid)

        self.setLayout(self.Totallayout)

    def All_btn_clicked(self):

        for i in range (0, len(self.list_of_ComName)):
            self.list_of_packetClass[i].send_packet()

    def onActivated(self, text):

        self.Label_Combo.setText(text)
        self.Label_Combo.adjustSize()

    def onChanged(self, text):

        self.Label_Test.setText(text)
        self.Label_Test.adjustSize() # adjustSize() 메서드로 텍스트의 길이에 따라 라벨의 길이를 조절해주도록 합니다.

    def initStatusUpdate(self):  # 다중쓰레드 핑 테스트, 모든 컴퓨터들을 다 테스트해봄.

        for i in range(0, len(self.list_of_ComName)):
            ping_test_thread = threading.Thread(target=self.pingOk, args=(i,))  # args 튜플 끝 부분에 쉼표를 붙여줘야한다.
            ping_test_thread.setDaemon(True) # 데몬쓰레드는 메인 프로그램이 종료될때 자동으로 같이 종료한다.
            ping_test_thread.start()

        for i in range(0, len(self.list_of_PjIp)):
            pj_test_thread = threading.Thread(target=self.pjTest, args=(i,))  # args 튜플 끝 부분에 쉼표를 붙여줘야한다.
            pj_test_thread.setDaemon(True)  # 데몬쓰레드는 메인 프로그램이 종료될때 자동으로 같이 종료한다.
            pj_test_thread.start()

    def pingOk(self, i): #매15초마다 테스트하는것
        try:
            output = subprocess.check_output(
                "ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', self.list_of_ComIP[i]),
                shell=True)
            self.computer_status[i].setText('작동 중')
            self.computer_status[i].setStyleSheet("color : darkgreen; font: bold 13px;")
            print(f'{QTime.currentTime().toString()} : {i+1}번 컴퓨터(' + self.list_of_ComIP[i] +') 핑테스트 성공')
        except Exception as e:
            try:
                self.computer_status[i].setText('연결 끊김')
                self.computer_status[i].setStyleSheet("color : gray ")
                print(f'{QTime.currentTime().toString()} : {i+1}번 컴퓨터(' + self.list_of_ComIP[i] + ') 네트워크 연결 실패')
            except RuntimeError:
                print("객체 삭제")
            return False
        return True

    def pjTest(self, i): #매15초마다 테스트하는것
        try:
            status = self.list_of_pjClass[i].get_power()
            self.projector_status[i].setText(f'램프 {status}')
            self.projector_status[i].setStyleSheet("color : darkgreen; font: bold 13px;")
            print(f'{QTime.currentTime().toString()} : {self.list_of_PjName[i]} {status}')
            if self.is_it_openTime:       #전시시간에
                if status == 'off':               #프로젝터가 꺼져있으면
                    print(f'{QTime.currentTime().toString()} : {self.list_of_PjName[i]}를 다시 켭니다. -----------------------------')
                    for j in range(0, 6) :
                        self.list_of_pjClass[i].lamp_on()
                        time.sleep(0.1)
            if not self.is_it_openTime:   # 전시시간이 아닐때
                if status == 'on':                # 프로젝터가 켜져있으면
                    print(f'{QTime.currentTime().toString()} : {self.list_of_PjName[i]}를 다시 끕니다. -----------------------------')
                    for j in range(0, 6) :
                        self.list_of_pjClass[i].lamp_off()
                        time.sleep(0.1)
        except Exception as e:
            try:
                self.projector_status[i].setText('연결 끊김')
                self.projector_status[i].setStyleSheet("color : gray ")
                print(f'{QTime.currentTime().toString()} : {self.list_of_PjName[i]} + 프로젝터 네트워크 연결 실패 / 랜 연결 확인바랍니다.')
            except RuntimeError:
                print("객체 삭제")
            return False
        return True

    def initTimerRoutine(self):

        self.timer_status = QTimer()
        self.timer_status.timeout.connect(self.initStatusUpdate)
        self.timer_status.start(15000)

        self.timer_sec = QTimer()
        self.timer_sec.timeout.connect(self.secTimer)
        self.timer_sec.start(1000)

    def initTd(self):
        self.start_td = timedelta(hours=int(self.museum_start_time[0]), minutes=int(self.museum_start_time[1]))
        self.end_td = timedelta(hours=int(self.museum_end_time[0]), minutes=int(self.museum_end_time[1]))

    def secTimer(self):  # 매 1초마다 실행되는 함수
        time_temp = QTime.currentTime().toString().split(':')
        seconds_now = timedelta(hours=int(time_temp[0]), minutes=int(time_temp[1]), seconds=int(time_temp[2]))
        if self.start_td < seconds_now and self.end_td > seconds_now:
            self.is_it_openTime = True

    def initBtn(self):

        for i in range (0,len(self.list_of_ComName)):
            self.computer_off_btn[i].clicked.connect(self.list_of_psexecClass[i].power_off)

        for i in range (0,len(self.list_of_ComName)):
            self.computer_on_btn[i].clicked.connect(self.list_of_packetClass[i].send_packet)

        for i in range (0,len(self.list_of_PjName)):
            self.projector_on_btn[i].clicked.connect(self.list_of_pjClass[i].lamp_on)
            self.projector_off_btn[i].clicked.connect(self.list_of_pjClass[i].lamp_off)

    def allProjectorOn(self):
        threads = []
        for IP in self.list_of_PjIp:
            t = threading.Thread(target=self.turn_on_projector_method,
                                 args=(IP,))  # 쓰레딩 할때... iterable형으로 args를 넣어야하는걸 잊지마라. 즉 쉼표 붙여주란소리임.
            threads.append(t)
        for t in threads:
            t.start()
            time.sleep(0.1)
        for t in threads:
            t.join()
            time.sleep(0.1)

    def check_schedule(self):
        if int(self.list_of_week_TF[self.now.tm_wday]) == 2:
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Controll_Widget()
    sys.exit(app.exec_())