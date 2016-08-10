import logging
import sys
import socket
# import serial
import threading

import time


class LS2D:

    def __init__(self, ip, port, sensor_address):
        self.logger = logging.getLogger('opt_core')
        self.logger.info("*** LS2D START ***")
        self.address = sensor_address
        self.logger.info("Sensor address set to {0}".format(self.address))
        self.port = port
        self.ip = ip

        # ## SOCKET ###

        self._connect(ip, self.port, 10)

        self.logger.info("Connecting to: {0}".format(self.port))

        self.firmware = None
        self.serial_number = None
        self.FPP = 5
        self._packets = []
        self._recv = None
        self._socket_lock = threading.Lock()
        # self._packets_lock = threading.Lock()
        self.go = False
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.logger.debug("Buffer size: {0}".format(self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))

        self.rcv_expo = False
        self.expo_ok = False

        self.setup()
        self.logger.info("Connected")
        self.logger.info("Ready to go")

    def setup(self):
        self.socket.sendto(bytes.fromhex('f3'), ('192.168.1.255', self.port))
        self._read(6)
        self.socket.sendto(bytes.fromhex('f3'), ('192.168.1.255', self.port))
        self._read(6)
        self._send([0x51, 0x7e, 0x00, 0x00])
        self._read(258)
        self.read_id_data()
        self._send([0x51, 0x7d, 0x00, 0x00])
        self._read(258)

        self.logger.info("Setup complete")

    @property
    def packets(self):
        p = self._packets[:]
        self._packets = []
        return p

    def read_id_data(self):
        self.logger.info("Reading id data from sensor...")
        self._send([0x51, 0x7f, 0x00, 0x00])
        id_data = self._read()
        self.logger.debug("ID data: {0}".format(id_data))
        # id_data_string = ""
        # for i, letter in enumerate(id_data):
        #     if letter < 128:
        #         print(i, letter, chr(letter))
        #         id_data_string.join(chr(letter))
        #     else:
        #         id_data_string.join("?")
        # print("DATA: ", id_data_string)
        return id_data

    def set_exposition(self, expo):
        self.logger.info("SET EXPO: setting exposition to {0} ms.".format(expo))
        if (expo > 65535) or (expo < 1):
            self.logger.error("SET EXPO: exposition value not in range [1, 65535]. ")
            return False
        else:
            bytes = [0x74, expo >> 8, expo & 0xFF]
            self._send(bytes)
            # response = self._read(1)
            # if response == 0x74:
            #     self.logger.info("SET EXPO: successful")
            #     return True
            self.rcv_expo = True

    def start_reading(self):
        loop = threading.Thread(target=self.loop)
        loop.start()

    def loop(self):
        while True:
            self.read_single_packet()

    def read_single_packet(self):
        self._send([0x41])
        self._send([0x42])
        data = self._read(4104)
        if (len(data) == 1) and (data == [0x74]):
            if self.rcv_expo:
                self.rcv_expo = False
                self.expo_ok = True
                self.logger.info("RSP: Expo set OK")
            else:
                self.logger.warn("RSP: Unexpected 'set expo' response")
        elif len(data) == 4104:
                timestamp = time.perf_counter()
                self.logger.debug("RSP: Coords packet have been read")
                parsed = self._parse_coords(data[8:]) # 7 ms
                self._packets = [(parsed, timestamp)]
        else:
            self.logger.warn("Unknown packet has been discarded")


    def _send(self, data):
        if len(data) > 65535:
            self.logger.error("SEND: Data length exceeds 65536")
            raise ValueError("Data length exceeds 65536")

        self._socket_lock.acquire()
        self.logger.debug("Sending {0} to {1}:{2}".format(data, self.ip, self.port))
        try:
            self.socket.sendto(bytes(data), (self.ip, self.port))
        except ConnectionResetError as e:
            self.logger.error("Send error: {0}".format(e))
        self._socket_lock.release()
        return data

    def _read(self, size=4096):
        ok = True
        response = []
        self.logger.debug("Waiting for available data...")
        try:
            response, addr = self.socket.recvfrom(size)
            response = list(response)
        except ConnectionResetError as e:
            self.logger.error("Send error: {0}".format(e))
        self.logger.debug("RECV: response length: {0}".format(len(response)))
        data = response
        if ok:
            return list(data)


    def _get_float_x(self, b1, b2):
        add_code = (b1 << 8) + b2
        add_code = -(add_code & 0b1000000000000000) | (add_code & 0b0111111111111111)
        return add_code / (2 ** self.FPP)

    def _parse_coords(self, coords):
        parsed = []
        if len(coords) == 1024 * 4:
            for i in range(1024):
                # start_time = time.perf_counter()
                w_little = coords.pop()
                w_big = coords.pop()
                h_little = coords.pop()
                h_big = coords.pop()
                # print("pop: {0}".format((time.perf_counter() - start_time) * 1000))

                parsed.append([self._get_float_x(h_big, h_little), self._get_float_x(w_big, w_little)])
                # print("append: {0}".format((time.perf_counter() - start_time) * 1000))

        else:
            self.logger.error("Parsing coords: wrong data length")
            # raise ValueError("wrong data length: {0}".format(len(coords)))
        self.logger.debug("Parsing coords: returning {0} points".format(len(parsed)))
        return parsed

    def _connect(self, address, port, attempts):
        a = attempts

        while a > 0:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                # self.socket.settimeout(5)
                # self.socket.connect((address, port))
                self.socket.bind(("0.0.0.0", 1024))
            except (ConnectionRefusedError, socket.timeout, OSError) as e:
                self.logger.error("Connection error: {0}. {1} attempts left".format(e, a))
                a -= 1
                if a == 0:
                    self.logger.error("Cannot connect. Shutting down...")
                    # self._recv.stop()
                    print("recv stop")
                    sys.exit()
            else:
                a = 0
                self.logger.info("Connection successful")

