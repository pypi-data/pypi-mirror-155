import socket

from tsdl.config.config import CONFIG


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((CONFIG.get('EM', 'ip'), int(CONFIG.get('EM', 'port'))))

    def close(self):
        self.s.close()

    def send(self, command):
        self.connect()
        self.s.send(command.encode('utf-8'))
        result = self.s.recv(1024).decode('utf-8')
        self.s.close()
        return result


def random_num():
    command = 'UP698015:00:00;'
    result = Client().send(command)
    rn = result.split(';')[3]

    return rn


def negotiate(m_sn: str, m_counter: int):
    cs = '%08X' % (m_counter + 1)
    command = 'UP698001:04;0001000800040001;00{}{}01'.format(m_sn.upper(), cs.upper())
    result = Client().send(command)

    ar = result.split(';')[3]
    rn = ar[0:32]
    data = ar[32:96]
    mac = ar[96:]

    return {"rn": rn, "data": data, "mac": mac}


def verify_session(rn, m_sn, m_rn, m_mac):
    command = 'UP698002:05;00010008001000300004;00{}{}{}{}'.format(m_sn.upper(), rn.upper(), m_rn.upper(),
                                                                   m_mac.upper())
    result = Client().send(command)
    iv = result.split(';')[3]

    return {"iv": iv}

