import grpc
import cv2
import base64
import numpy as np

from .proto_1 import face_grpc_pb2
from .proto_1 import face_grpc_pb2_grpc
from .proto_1 import facerecog_pb2
from .facemodel import BaseFaceMoel

def get_features(frame_path, channel):
    """
    get the features of img

    args:
        frame_path: path of img
        addr: the address(ip:port) of face_cpp docker 
    return:
        face_infos:
            feature of faces in img which path is frame_path
    """

    # print("正在处理图片")
    try:
        # 使用图片进行人脸识别的三个步骤
        cvimg = cv2.imread(frame_path) # 1.使用 cv2.imread 读入
        cvimg_encode = cv2.imencode(".jpg", cvimg)[1] # 2.使用cv2.imencode 按照  ".jpg" 编码
        req1 = base64.b64encode(cvimg_encode) # 3.使用base64 做转换: Encode the bytes-like object s using Base64 and return a bytes object

        stub = face_grpc_pb2_grpc.face_grpcServiceClsStub(channel)
        response = stub.face_grpc(face_grpc_pb2.face_grpcRequest(req=req1), timeout=10)
        response_facerecog = facerecog_pb2.FaceRecogResponse()
        response_facerecog.ParseFromString(response.res)

        face_infos = []
        for face in response_facerecog.faces:  # 获取的若干张人脸的数据

            feature = np.array([[face_feature for face_feature in face.face_feature]])
            bounding_box = np.array([face.rect.x, face.rect.y, face.rect.x + face.rect.width, face.rect.y + face.rect.height])
            landmarks = np.array([(lm.x, lm.y) for lm in face.landmarks])

            face_infos.append((feature, bounding_box, landmarks))

        return face_infos, cvimg

    except Exception as e:
        print("人脸特征获取出错， 请检查人脸docker服务是否正常， 错误信息：\n {} ".format(repr(e)))
        return None,None 

class FaceModel(BaseFaceMoel):
    def __init__(self, filename, channel, *, is_full=False):
        super().__init__(filename, channel, is_full=is_full)

        self._features = [] 
        self._load_features()

    def _load_features(self):
        #print(filename)
        with self._channel() as ch:
            # 调用face app 获取人脸特征，执行比对，将所有超过阈值的结果发送给IOU任务队列。
            features, cvimg = get_features(self.filename, ch)
            #print(cvimg.shape)
            height, width, _ = cvimg.shape
            self.height = height
            self.width = width
            self._features = features

    def lens(self):
        return len(self._features)

    def features(self):
        for feature,box,lm  in self._features:
            box = [int(item) for item in box]
            yield feature,box,lm,1
