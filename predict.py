from keras.layers import Input
from mask_rcnn import MASK_RCNN
from PIL import Image
import cv2
import numpy as np
import glob
import os
def SinglePredict(filename,out_path1):

    image = Image.open(filename)
    img_name = os.path.basename(filename)
    image_mask=mask_rcnn.detect_image(image)
    if type(image_mask) is np.ndarray:
        cv2.imwrite(out_path1 + img_name[0:-4] + '.png', image_mask)
    else:
         image_mask.save(out_path1+img_name[0:-4]+'.png')



def BatchPredict(DirPath):
    fileList = os.listdir(DirPath)
    for fileName in fileList:
        name = DirPath + '\\' + fileName
        SinglePredict(name,out_path1)


if __name__ == "__main__":
    mask_rcnn = MASK_RCNN()
    ImageDirPath=r'L:\2024_yangmeikeng\2024_11_17\sample1_2_5\image_clip'
    out_path1 = r'L:\2024_yangmeikeng\2024_11_17\sample1_2_5\color_clip/'
    BatchPredict(ImageDirPath)
    mask_rcnn.close_session()