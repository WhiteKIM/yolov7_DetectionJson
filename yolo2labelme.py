import numpy as np
import cv2
from collections import OrderedDict
import json
import os

additional_num = 5  # 발, 손과 같이 물체의 가장자리 부분을 잘 못잡는 부분을 보완하기 위해 추가적으로 더할 픽셀값

def convYolo2Labelme(result, img, imgName, save_path):
    fileData = OrderedDict()
    height, width, channel = img.shape
    fileData['version'] = "5.0.1"
    fileData['flags'] = {}
    fileData['shapes'] = []
    for data in result:
        bBox = []
        x = data[0]
        label = data[1]
        if int(x[0])+additional_num < width :
            x0 = int(x[0])+additional_num
        else:
            x0 = int(x[0])

        if int(x[1])+additional_num < height:
            y0 = int(x[1])+additional_num
        else:
            y0 = int(x[1])

        if int(x[2])+additional_num < width :
            x1 = int(x[2])+additional_num
        else:
            x1= int(x[2])

        if int(x[3])+additional_num < height:
            y1 = int(x[3])+additional_num
        else:
            y1 = int(x[3])

        c1 = (x0, y0)
        c2 = (x1, y1)
        bBox.append(c1)
        bBox.append(c2)
        fileData['shapes'].append({
            "label":label,
            "points":bBox,
            "group_id":None,
            "shape_type":"rectangle",
            "flags":{}
        })
    fileData['imagePath'] = imgName
    fileData['imageData'] = None
    fileData['imageHeight'] = height
    fileData['imageWidth'] = width
    jsonName = os.path.splitext(imgName)[0]+'.json'
    with open(str(save_path)+'/'+jsonName, 'w') as makeJson:
        json.dump(fileData, makeJson, ensure_ascii=False, indent='\t')
        makeJson.close()

