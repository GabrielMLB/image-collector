from struct import unpack
import numpy as np
import socket


message_struct = [4, 4, 8, 8, 8, 8, 1, 1, 1, 4, 8, 4, 4, 4]

message_type = [
    np.uint32,
    np.uint32,
    np.float64,
    np.float64,
    np.float64,
    np.float64,
    np.uint8,
    np.uint8,
    np.uint8,
    np.float32,
    np.float64,
    np.float32,
    np.int32,
    np.int32,
]

message_dict = dict(zip([
    'date',
    'time',
    'latitude',
    'longitude',
    'speed',
    'course',
    'status',
    'quality',
    'satellites',
    'hdop',
    'altitude',
    'undulation',
    'age',
    'StationID'
],
    zip(
        message_struct,
        message_type
    ))
)


class GPSSocket:

    def __init__(self, ip="127.0.0.1", port=5555):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def read(self, message_size=1024):
        data, addr = self.sock.recvfrom(message_size)
        output = {}

        if len(data) == 67:
            count = 0
            for key, value in message_dict.items():
                size = value[0]
                d_type = value[1]
                output[key] = np.frombuffer(data[count:count + size], dtype=d_type)[0]
                if (d_type == np.uint8) or (d_type == np.uint32) or (d_type == np.int32):
                    output[key] = int(output[key])
                count = count + size
            output['status'] = chr(output['status'])
        elif len(data) == 68:
            message = unpack('IIddddcBBfdfii', data)

            count = 0
            for key, value in message_dict.items():
                output[key] = message[count]
                count += 1
            output['status'] = output['status'].decode()

        return output