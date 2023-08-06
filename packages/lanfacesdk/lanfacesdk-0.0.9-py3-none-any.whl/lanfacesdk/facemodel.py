import grpc
import cv2
from .proto_2 import facerec_pb2
from .proto_2 import facerec_pb2_grpc
import numpy as np
import math

class BaseFaceMoel:
    def __init__(self, filename, channel, *, is_full=False, min_area=-1):
        self.filename = filename 
        self.channel = channel
        self.is_full = is_full
        self.min_area = min_area

    def _channel(self):
        channel = self.channel
        if callable(channel):
            return channel()
        elif type(channel)==str:
            return grpc.insecure_channel(channel)
        elif isinstance(channel, grpc._channel.Channel):
            return channel
        else:
            raise Exception("错误的grpc参数")

    def lens(self):
        pass

    def features(self):
        pass
