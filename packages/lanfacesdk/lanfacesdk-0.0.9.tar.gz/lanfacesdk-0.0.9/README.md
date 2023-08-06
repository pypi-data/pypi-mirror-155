## 安装
```bash
pip install lanfacesdk
```



## 老模型

```python
from lanfacesdk.model_1 import FaceModel

model = FaceModel('tests/images/tfz.jpeg', '192.168.1.16:8001')

# 判断人脸数
if model.lens()>0:
    # 获取人脸特征值及人脸框
    for feature, box, _, _ in model.features():
        print(feature, box)
```



## 新模型

```python
from lanfacesdk.model_2 import FaceModel

model = FaceModel('tests/images/tfz.jpeg', '192.168.1.16:50051')

# 判断人脸数
if model.lens()>0:
    # 获取人脸特征值及人脸框
    for feature, box, _, _ in model.features():
        print(feature, box)
```

