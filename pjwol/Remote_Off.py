import subprocess
import os

class Remote_off_class:

    def __del__(self):
        print(f"{self.IP} 리모트 오프 객체가 사라짐!")

    def __init__(self, _IP):
        self.IP = _IP
        self.dir_path = os.getcwd()

    def power_off(self):
        print(f'byebye {self.IP}')
        proc = subprocess.run(['cmd', '/c', f'{self.dir_path}\\psexec', f'\\\\{self.IP}', '-u', 'remoteoff', '-p', '7150', 'shutdown', '-f', '-s', '-t', '10'])

    def power_off_etc(self, IP):
        print(f'byebye {IP}')
        proc = subprocess.run(['cmd', '/c', f'{self.dir_path}\\psexec', f'\\\\{IP}', '-u', 'remoteoff', '-p', '7150', 'shutdown', '-f', '-s', '-t', '10'])


if __name__ == '__main__':
        proc = subprocess.run(['cmd', '/c', f'{os.getcwd()}\\psexec', '\\\\192.168.200.3', '-u', 'remoteoff', '-p', '7150', 'shutdown', '-f', '-r', '-t', '100'])