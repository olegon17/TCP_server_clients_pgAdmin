import struct
from datetime import datetime

#from utils.crc16 import crc_16
from crc16 import _crc16
from crc16 import crc16pure
import crc16
import unittest
MSG_BODY_FMT = '=IBBBBBBI'


class TcpProtocolParser(object):
    def __init__(self):
        self.m_protocol_revision = "1.0"

    # разбор пакета
    def process_packet(self, data:bytes):
        result = None

        # проверка длины пакета
        if len(data)< 16:
            print("Message len is too short!")
            return result

        # проверка контррольной суммы
        msg_crc = struct.unpack('=H', data[-struct.calcsize("=H"):])[0]
        calc_crc = crc_16(data[:-struct.calcsize("=H")])

        if msg_crc != calc_crc:
            print("Wrong CRC16! In message: {0}; calculated: {1}!".format(hex(msg_crc), hex(calc_crc)))
            return result

        # разбор параметров
        dev_id, firmware_ver, msg_type, work_mode, fill_sensor, flip_sensor, temperature, timestamp = \
            struct.unpack(MSG_BODY_FMT, data[:struct.calcsize(MSG_BODY_FMT)])

        # упаковка в словарь
        parsed_dict = {}
        parsed_dict["dev_id"] = dev_id
        parsed_dict["firmware_version"] = firmware_ver
        parsed_dict["msg_type"] = msg_type
        parsed_dict["work_mode"] = work_mode
        parsed_dict["fill_sensor"] = fill_sensor
        parsed_dict["flip_sensor"] = flip_sensor
        parsed_dict["temperature"] = temperature-55
        parsed_dict["unix_timestamp"] = timestamp
        parsed_dict["timestamp"] = datetime.utcfromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M:%S')

        result = parsed_dict
        return result


class TcpProtocolBuilder(object):
    def __init__(self):
        self.m_protocol_revision = "1.0"

    def build_packet(self, data_dict: dict):

        dev_id = None
        firmware_ver = None
        msg_type = None
        work_mode = None
        fill_sensor= None
        flip_sensor= None
        temperature= None
        timestamp= None

        if "dev_id" in data_dict:
            if isinstance(data_dict["dev_id"], int):
                dev_id = data_dict["dev_id"]
            else:
                print("dev_id value must be an integer!")
        if "firmware_version" in data_dict:
            if isinstance(data_dict["firmware_version"], int):
                firmware_ver = data_dict["firmware_version"]
            else:
                print("firmware_ver value must be an integer!")
        if "msg_type" in data_dict:
            if isinstance(data_dict["msg_type"], int):
                msg_type = data_dict["msg_type"]
            else:
                print("msg_type value must be an integer!")
        if "work_mode" in data_dict:
            if isinstance(data_dict["work_mode"], int):
                work_mode = data_dict["work_mode"]
            else:
                print("work_mode value must be an integer!")
        if "fill_sensor" in data_dict:
            if isinstance(data_dict["fill_sensor"], int):
                fill_sensor = data_dict["fill_sensor"]
            else:
                print("fill_sensor value must be an integer!")
        if "flip_sensor" in data_dict:
            if isinstance(data_dict["flip_sensor"], int):
                flip_sensor = data_dict["flip_sensor"]
            else:
                print("flip_sensor value must be an integer!")
        if "temperature" in data_dict:
            if isinstance(data_dict["temperature"], int):
                temperature = data_dict["temperature"]
            else:
                print("temperature value must be an integer!")
        if "unix_timestamp" in data_dict:
            if isinstance(data_dict["unix_timestamp"], int):
                timestamp = data_dict["unix_timestamp"]
            else:
                print("unix_timestamp value must be an integer!")

        # если перечень не полный выходим
        data_list = [dev_id, firmware_ver, msg_type, work_mode, fill_sensor, flip_sensor, temperature, timestamp]

        if None in data_list:
            print("None value in parameter list! Can't send initial settings!", data_list)
            return None

        data = struct.pack(MSG_BODY_FMT, dev_id, firmware_ver, msg_type, work_mode, fill_sensor, flip_sensor, temperature, timestamp)
        calc_crc = crc_16(data)
        data += struct.pack("=H", calc_crc)
        return data



def main():
    msg_demo_bad_crc = b'\xEF\xBE\xAD\xDE\x01\x02\x03\x00\x01\xF1\x01\x00\x00\x00\xBE\xBA'
    msg_demo = b'\xEF\xBE\xAD\xDE\x01\x02\x03\x00\x01\xF1\x01\x00\x00\x00\x30\x04'

    parser = TcpProtocolParser()
    builder = TcpProtocolBuilder()

    parsed_dict = parser.process_packet(msg_demo)
    print("Parsed packet:")
    print(parsed_dict)

    data_dict = {
        'dev_id': 0xDEADBEEF,
        'firmware_version': 1,
        'msg_type': 2,
        'work_mode': 3,
        'fill_sensor': 0,
        'flip_sensor': 1,
        'temperature': -15,
        'unix_timestamp': 1
    }

    packet = builder.build_packet(data_dict)
    print("Builded packet:")
    print(packet)

    reparsed_dict = parser.process_packet(packet)
    print("Parsed builded packet:")
    print(data_dict)
    print(reparsed_dict)

    del reparsed_dict['timestamp']
    if reparsed_dict == data_dict:
        print("MATCH!")

if __name__ == '__main__':
    main()