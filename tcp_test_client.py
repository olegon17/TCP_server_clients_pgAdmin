import json
import random

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer, task
from twisted.internet.task import LoopingCall
from twisted.logger import Logger, eventAsText, FileLogObserver

import sys

from utils.unix_timestamp import unix_timestamp

log = Logger()
# log.observer.addObserver(FileLogObserver(sys.stdout, lambda e: eventAsText(e) + "\n"))

from tcp_protocol_parser import TcpProtocolBuilder

host = 'localhost'
port = 666


class TCPWasteClientProtocol(protocol.Protocol):
    def __init__(self):
        self.builder = TcpProtocolBuilder()
        log.debug("Start Waste Sensor Client")

    def startProtocol(self):
        self.loopObj = LoopingCall(self.sendData)
        self.loopObj.start(1, now=False)

    def stopProtocol(self):
        "Called after all transport is teared down"
        pass

    # Отправка сообщения с проверкой
    def sendData(self):
        data_dict = {
            'dev_id': 0xDEADBEEF,
            'firmware_version': random.randint(1, 2),
            'msg_type': random.randint(0, 5),
            'work_mode': random.randint(0, 2),
            'fill_sensor': random.randint(0, 1),
            'flip_sensor': random.randint(0, 1),
            'temperature': random.randint(0, 255),
            'unix_timestamp': unix_timestamp()
        }

        packet = self.builder.build_packet(data_dict)

        if packet:
            log.debug("writing")
            self.transport.write(packet)
        else:
            log.debug("loseConnection")
            # transport.loseConnection() - разрыв соединения
            self.transport.loseConnection()

    def connectionMade(self):
        self.startProtocol()

    def dataReceived(self, data):
        print(data)
        try:
            print(format(json.loads(data)))
            print("got json")
        except:
            print("filedata incoming!")
            f = open("update_firmware.hex", "a")
            f.write(data)
            f.close()
            self.transport.write("file received")


class TCPWasteClientFactory(protocol.ClientFactory):
    protocol = TCPWasteClientProtocol

    def clientConnectionFailed(self, connector, reason):
        log.warn('connection failed:' + reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        log.warn('connection lost:' + reason.getErrorMessage())
        reactor.stop()


factory = TCPWasteClientFactory()
reactor.connectTCP(host, port, factory)
reactor.run()
