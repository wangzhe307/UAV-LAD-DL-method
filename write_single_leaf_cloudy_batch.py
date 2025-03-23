# coding: utf-8
import glob
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy.io as sio
from skimage import measure
import time
import cv2
def single_leaf_cloudy_point(IMG_DIR,out_path,edge_path,name_str):
    jpg_files = glob.glob(os.path.join(IMG_DIR, "*.jpg"))
    uv_files = list(map(lambda x: os.path.join(os.path.dirname(x), os.path.splitext(os.path.basename(x))[0]+"_uv.txt"), jpg_files))
    pc = np.loadtxt(os.path.join(IMG_DIR, "pc.txt"))
    NUM_POINTS = pc.shape[0]
    pointVisited = np.zeros((NUM_POINTS, 1))
    extractedPointCloud = []
    rowcols = [] 
    startedLabelIndex = 0
    NUM_CAMERAS = 1
    for i in range(NUM_CAMERAS):
        img = Image.open(edge_path)
        edge = np.array(img)
        edge = edge > 0
        label_image = measure.label(edge)  
        max_val = label_image.max()
        label_image[label_image > 0] += startedLabelIndex
        startedLabelIndex += max_val
        [img_rows, img_cols] = edge.shape
        uv = np.loadtxt(uv_files[i])
        if len(uv) > 0:
            for j in range(NUM_POINTS):
                print("j:",j)
                row = int(np.floor(uv[j][1]))
                col = int(np.floor(uv[j][0]))
                if (pointVisited[j] == 0) and (0 <= row <= img_rows-1) and (0 <= col <= img_cols-1):
                    if label_image[row][col] > 0:
                        extractedPointCloud.append(list(pc[j, :])+[label_image[row][col]]+[row, col])

                        pointVisited[j] = 1
    extractedPointCloud = np.array(extractedPointCloud)
    
    mat_dict = {'data': extractedPointCloud }
    sio.savemat(os.path.join(out_path, name_str + '_leaf_cloudy_point.mat'),mat_dict)

if __name__ == '__main__':
    folder_dir = r'I:\yangmeikeng_deal_2023\2023-02-16\sample3\14-30\1good'
    erzhi_dir = r'I:\yangmeikeng_deal_2023\2023-02-16\sample3\14-30\pinjie_erzhi1'
    folder_list = os.listdir(folder_dir)
    for i in range(0, len(folder_list)):
        folder_path = os.path.join(folder_dir, folder_list[i])  
        jpg_list = glob.glob(os.path.join(folder_path, "*.jpg"))  
        jpg_inpath = jpg_list[0]
        jpg_name = os.path.basename(jpg_inpath) 
        edge_file = erzhi_dir + '//' + jpg_name[0:-4] + '.png'  
        out_path = folder_path + '//' +'out1'+'//'
        if not os.path.exists(out_path):  
            os.mkdir(out_path)
        else:
             print("folder is exist")
        start_time = time.time()
        single_leaf_cloudy_point(folder_path,out_path,edge_file,jpg_name[0:-4])
        end_time = time.time()
        run_time = end_time - start_time
        print("代码执行时间为：%s秒" % run_time)
