from pypjlink import Projector
import threading

class ProjectorClass:

    def __init__(self, _IP):
        self.IP = _IP

    def lamp_on(self):
        thread = threading.Thread(target=self.lamp_on_)  # args 튜플 끝 부분에 쉼표를 붙여줘야한다.
        thread.setDaemon(True)  # 데몬쓰레드는 메인 프로그램이 종료될때 자동으로 같이 종료한다.
        thread.start()

    def lamp_on_(self):
        print(f'프로젝터 {self.IP}를 킵니다')
        try:
            with Projector.from_address(self.IP) as projector:
                projector.authenticate()
                projector.set_power('on')
        except:
            print(f'프로젝터{self.IP}는 잘못된 연결입니다.')

    def lamp_off(self):
        thread = threading.Thread(target=self.lamp_off_)  # args 튜플 끝 부분에 쉼표를 붙여줘야한다.
        thread.setDaemon(True)  # 데몬쓰레드는 메인 프로그램이 종료될때 자동으로 같이 종료한다.
        thread.start()

    def lamp_off_(self):
        print(f'프로젝터 {self.IP}를 끕니다')
        try:
            with Projector.from_address(self.IP) as projector:
                projector.authenticate()
                projector.set_power('off')
        except:
            print(f'프로젝터{self.IP}는 잘못된 연결입니다.')

    def get_power(self):
        with Projector.from_address(self.IP) as projector:
            projector.authenticate()
            return projector.get_power()

    def get_status(self):
        try:
            with Projector.from_address(self.IP) as projector:
                projector.authenticate()
                return projector.get_errors()
        except:
            print(f'프로젝터{self.IP}는 잘못된 연결입니다.')

    def get_lampHour(self):
        try:
            with Projector.from_address(self.IP) as projector:
                projector.authenticate()
                return projector.get_lamps()
        except:
            print(f'프로젝터{self.IP}는 잘못된 연결입니다.')


if __name__ == '__main__':
    with Projector.from_address('192.168.200.12') as projector:
        projector.authenticate()
        print(projector.get_lamps())