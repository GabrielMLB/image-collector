from datetime import datetime
from loguru import logger
from gps import GPSSocket
import pyrealsense2 as rs
import numpy as np
import cv2


class Realsense:

    def __init__(self):
        self.pipeline = rs.pipeline(rs.context())
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        self.align = rs.align(rs.stream.color)
        self.colorizer = rs.colorizer(color_scheme=2)
        self.pipeline.start(self.config)

    def read_frames(self):
        frames = self.pipeline.wait_for_frames()
        frames = self.align.process(frames)

        return frames

    def save_frames(self, path, seconds):
        server = {"host": '', "port": 5555}
        gps_connection = GPSSocket(ip=server['host'], port=server['port'])
        start = datetime.now()
        first_image = 1

        while True:
            try:
                gps_data = gps_connection.read()
                lat, lon, heading = gps_data['latitude'], gps_data['longitude'], gps_data['course']

                frames = self.read_frames()

                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()

                depth_frame = np.asanyarray(self.colorizer.colorize(depth_frame).get_data())
                color_frame = np.asanyarray(color_frame.get_data())

                process_time = datetime.now() - start

                if first_image:
                    cv2.imwrite('default.jpg', color_frame)
                    print("first image saved")
                    first_image = 0

                if process_time.seconds >= seconds:
                    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
                    name_image = f"{current_time};{lat};{lon};{heading}.jpg"
                    cv2.imwrite(f"{path}/{name_image}", color_frame)
                    start = datetime.now()
                    print(f"{name_image} saved.")

            except Exception as e:
                logger.error(e)
