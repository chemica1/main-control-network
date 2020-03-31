from wakeonlan import send_magic_packet


class send_packet_class:

    def __init__(self, _MAC):
        self.MAC = _MAC

    def send_packet(self):
        send_magic_packet(self.MAC)
        print(self.MAC)

    def send_packet_(self, MAC):
        send_magic_packet(MAC)
        print(MAC)