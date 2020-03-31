import os, sys, threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from Main_Controll_Widget import Controll_Widget
from Com_Info_Widget import ComputerInfoPrint
from Timer_Widget import ComputerTimePrint
from pj_Info_Widget import ProjectorInfoPrint
from Loading_Widget import Loding_Widget
from wakeonlan import send_magic_packet
from datetime import timedelta
from pypjlink import Projector
from Remote_Off import Remote_off_class
import time
from File_class import File_class


class MainWindow(QMainWindow): #메인윈도우에선 layout 못쓴다. 자체레이아웃을 갖고있기때문
    now = time.localtime()

    def __init__(self):
        super().__init__()

        current_time = QTime.currentTime().toString().split(':')
        print(f'{current_time}')

        self.dir_path = os.getcwd()
        self.file_to_list()
        self.quit_flag = 0  #종료시간 이후에도 킬 수 있게 만든 장치
        self.quit_flag2 = 0 #종료명령을 한번만 하게 하려고..

        self.initUI()

        QTimer.singleShot(4000, self.Loading_Main_Controll_Widget)
        self.showLoadingMovie()
        if self.check_schedule():
            self.initTimer()
            QTimer.singleShot(1500, self.showLoadingMovie2)
            QTimer.singleShot(2000, lambda: self.initPowerOn())
        else:
            print('지정된 요일이 아니므로 프로그램 작동 X')
            self.statusBar().showMessage('오늘은 지정된 요일이 아니므로, 컴퓨터와 프로젝터를 키지 않습니다. 5분후 자동으로 꺼집니다.')
            QTimer.singleShot(60*5*1000, lambda: os.system("shutdown /s /t 3"))

    def check_schedule(self):
        if int(self.list_of_week_TF[self.now.tm_wday]) == 2:
            return True
        else:
            return False

    def initUI(self):
        self.setWindowTitle('PC & Projector 통합 제어 시스템 - huliac (ver2.2)')
        self.setWindowIcon(QIcon(f'{self.dir_path}\\png\\huliacLogo.png'))

        #메인 툴바
        list_toolbar = QAction(QIcon(f'{self.dir_path}\\png\\poweron.png'), '전원제어', self)
        list_toolbar.setStatusTip('컴퓨터를 제어합니다.')
        list_toolbar.triggered.connect(self.Loading_Main_Controll_Widget)
        self.toolbar = self.addToolBar('list_toolbar')
        self.toolbar.addAction(list_toolbar)

        #컴퓨터 정보 변경
        Cominfo_toolbar = QAction(QIcon(f'{self.dir_path}\\png\\computer.png'), '컴퓨터 정보 변경', self)
        Cominfo_toolbar.setStatusTip('컴퓨터 정보를 변경합니다.')
        Cominfo_toolbar.triggered.connect(self.showComputerInfo)
        self.toolbar = self.addToolBar('Cominfo_toolbar')
        self.toolbar.addAction(Cominfo_toolbar)

        #프로젝터 정보 변경
        PJinfo_toolbar = QAction(QIcon(f'{self.dir_path}\\png\\projector.png'), '프로젝터 정보 변경', self)
        PJinfo_toolbar.setStatusTip('프로젝터 설정')
        PJinfo_toolbar.triggered.connect(self.showProjectorInfo)
        self.toolbar = self.addToolBar('PJinfo_toolbar')
        self.toolbar.addAction(PJinfo_toolbar)

        time_toolbar = QAction(QIcon(f'{self.dir_path}\\png\\time.png'), '스케줄설정', self)
        time_toolbar.setStatusTip('종료 시간을 설정합니다.')
        time_toolbar.triggered.connect(self.showComputerTime)
        self.toolbar = self.addToolBar('time_toolbar')
        self.toolbar.addAction(time_toolbar)

        Cominfo_toolbar.setEnabled(False)
        list_toolbar.setEnabled(False)
        time_toolbar.setEnabled(False)
        PJinfo_toolbar.setEnabled(False)

        QTimer.singleShot(3000, lambda: Cominfo_toolbar.setEnabled(True))
        QTimer.singleShot(3000, lambda: list_toolbar.setEnabled(True))
        QTimer.singleShot(3000, lambda: time_toolbar.setEnabled(True))
        QTimer.singleShot(3000, lambda: PJinfo_toolbar.setEnabled(True))

        self.statusBar()
        self.initWindowWhere()
        self.resize(1000,600)
        self.show()

    def initPowerOn(self):
        #컴퓨터 시작예약
        print(f'현재시각 {QTime.currentTime().toString()}')
        current_time = QTime.currentTime().toString().split(':')

        for i in range(0, len(self.list_of_com_MAC)):
            start_time_temp = self.list_of_computer_start_time[i].split(':')  #설정된 시간을 리스트로 뽑아낸다. 시 / 분 / 초
            start_td = timedelta(hours=int(start_time_temp[0]), minutes=int(start_time_temp[1]), seconds=int(start_time_temp[2]))
            current_td = timedelta(hours=int(current_time[0]), minutes=int(current_time[1]), seconds=int(current_time[2]))
            remaining_td = start_td - current_td  #설정된 시간과 현재시간간의 시간차를 구한다.

            self.OnTimePowerControll((int(remaining_td.seconds)*1000), str(self.list_of_com_MAC[i]))
            #self.Timer.singleShot((int(remaining_td.seconds)*1000), lambda : send_magic_packet(str(self.list_of_com_MAC[i]))) # 이렇게하면 MAC[10]만 나간다. 박제하자.
            print(f'{remaining_td.seconds}초 후에 {(i+1)}번 컴퓨터({str(self.list_of_com_MAC[i])})를 켭니다.')
        '''
        #프로젝터 일괄 시작
        threads = []
        for IP in self.list_of_PjIp:
            t = threading.Thread(target=self.turn_on_projector_method,
                                 args=(IP,))  # 쓰레딩 할때... iterable형으로 args를 넣어야하는걸 잊지마라. 즉 쉼표 붙여주란소리임.
            threads.append(t)
            ##각각의 쓰레드를 시작하고 및 끝날때까지 기다림(조인)
        for t in threads:
            t.start()
            time.sleep(0.1)
        for t in threads:
            t.join()
            time.sleep(0.1)
        '''

    def OnTimePowerControll(self, remainingTime, MAC):
        QTimer.singleShot(remainingTime, lambda : send_magic_packet(MAC))

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.MainTimer)
        self.timer.start(1000)

    def MainTimer(self): # 매초마다 연산하는 타이머.. 어떤 시간종속적인 일을 하고싶다면 여기에 넣으면 된다.
        date = QDate.currentDate()
        time = QTime.currentTime().toString()
        time_temp = time.split(':')

        remaining_hour = int(self.museum_end_time[0]) - int(time_temp[0])
        remaining_minute = int(self.museum_end_time[1]) - int(time_temp[1])

        if remaining_hour == 0 and remaining_minute == 0 and self.quit_flag == 0:
            self.quit_flag = 1
            print(f'{QTime.currentTime().toString()} : pc와 프로젝터를 일괄종료합니다')
            QTimer.singleShot(200, lambda : self.turn_off_all())

        if self.quit_flag == 0:
            self.statusBar().showMessage(date.toString(Qt.DefaultLocaleLongDate) +'  ' + time + f'  개장 예약 :{self.museum_start_time[0]}시 {int(self.museum_start_time[1])}분  종료 예약 :{self.museum_end_time[0]}시 {int(self.museum_end_time[1])}분') #시간표시
        elif self.quit_flag == 1:
            self.statusBar().showMessage('모든 컴퓨터를 종료한 뒤 자동으로 꺼집니다. 전원을 끄지 말아주세요.')
            if self.quit_flag2 == 1:
                print(f'{QTime.currentTime().toString()} : @@@@@@@@@@통합제어 컴퓨터를 종료합니다@@@@@@@@@@')
                QTimer.singleShot(500000, lambda : os.system("shutdown /s /t 15"))
                self.quit_flag2 = 0 # 한번만 명령받기

    def turn_off_all(self):
        threads = []
        for IP in self.list_of_com_IP:
            t = threading.Thread(target=self.turn_off_computer_method,
                                 args=(IP,))  # 쓰레딩 할때... iterable형으로 args를 넣어야하는걸 잊지마라. 즉 쉼표 붙여주란소리임.
            threads.append(t)

        for IP in self.list_of_PjIp:
            t = threading.Thread(target=self.turn_off_projector_method,
                                 args=(IP,))  # 쓰레딩 할때... iterable형으로 args를 넣어야하는걸 잊지마라. 즉 쉼표 붙여주란소리임.
            threads.append(t)

        ##각각의 쓰레드를 시작하고 및 끝날때까지 기다림(조인)
        for t in threads:
            t.start()
            time.sleep(10)
        for t in threads:
            t.join()
            time.sleep(10)

        self.quit_flag2 = 1 #컴퓨터 종료 허락

    def turn_off_projector_method(self, IP):
        print(f'프로젝터 {IP}를 끕니다')
        try:
            with Projector.from_address(IP) as projector:
                projector.authenticate()
                projector.set_power('off')
        except:
            print(f'프로젝터{IP}는 잘못된 연결입니다.')

    def turn_off_computer_method(self, IP):
        quit_temp = Remote_off_class(IP)
        quit_temp.power_off()
        print(IP + '를 종료했습니다!!!')

    def initWindowWhere(self): #처음 켜지는 창 윈도우에서의 위치 정하는 함수. 일단 정중앙으로 위치하게 만든거임.
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def Loading_Main_Controll_Widget(self):
        Controll_Widget_print = Controll_Widget()
        self.setCentralWidget(Controll_Widget_print) #센터 레이아웃에 꼭 추가해줘야한다.


    def showComputerInfo(self):
        SettingComputer = ComputerInfoPrint()
        self.setCentralWidget(SettingComputer) #센터 레이아웃에 꼭 추가해줘야한다.


    def showLoadingMovie(self):
        loading_widget = Loding_Widget("스케줄 확인중...")
        self.setCentralWidget(loading_widget)  # 센터 레이아웃에 꼭 추가해줘야한다.


    def showLoadingMovie2(self):
        loading_widget = Loding_Widget("컴퓨터/프로젝터 전원 켜는중...")
        self.setCentralWidget(loading_widget)  # 센터 레이아웃에 꼭 추가해줘야한다.


    def showComputerTime(self):
        ComputerTimeWidget = ComputerTimePrint()
        self.setCentralWidget(ComputerTimeWidget)


    def showProjectorInfo(self):
        ProjectorInfoWidget = ProjectorInfoPrint()
        self.setCentralWidget(ProjectorInfoWidget)


    def file_to_list(self):

        self.list_of_com_IP = File_class('Computer_IP').call_the_list()      #IP 리스트
        self.list_of_com_MAC = File_class('Computer_MAC').call_the_list()    #MAC 리스트
        self.list_of_com_name = File_class('Computer_name').call_the_list()  #컴퓨터 이름 리스트
        self.list_of_PjName = File_class('Projector_name').call_the_list()   #프로젝터 name 리스트
        self.list_of_PjIp = File_class('Projector_IP').call_the_list()       #프로젝터 IP 리스트
        self.list_of_week_TF = File_class('Weekly_schedule').call_the_list()    #주간 스케줄
        self.list_of_computer_start_time = File_class('Computer_start_time').call_the_list()   #컴퓨터 시작시간 리스트
        self.list_of_computer_end_time = File_class('Computer_end_time').call_the_list()   #컴퓨터 종료시간 리스트
        self.museum_start_time = File_class('Weekly_start_time').call_the_list()[self.now.tm_wday].split(':')  # 전시장 오픈시간 리스트
        self.museum_end_time = File_class('Weekly_end_time').call_the_list()[self.now.tm_wday].split(':')  # 전시장 마감시간 리스트

    '''
    def turn_on_projector_method(self, IP):
        for i in range(1,2):  #비비텍 프로젝터때문에 10번 신호 반복송출
            print(f'프로젝터 {IP}에 {i}번째 power on 신호를 전송합니다')
            try:
                with Projector.from_address(IP) as projector:
                    projector.authenticate()
                    projector.set_power('on')
            except:
                print(f'프로젝터{IP}는 잘못된 연결입니다. 잠시후 다시 시도해주세요.')
    '''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())