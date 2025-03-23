import glob
import os
from pickle import TRUE
from typing import List
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import measure
from planefit_good import planeFit_good
from mpl_toolkits.mplot3d import *
import pandas as pd
def read_pitch_angle(metadata_list):
    metadata_path = metadata_list[0]
    alllines = open(metadata_path, 'r', encoding='UTF-8').readlines()
    pitch_angle = float(alllines[0])
    return pitch_angle

def tiqu_single_angle(IMG_DIR,out_path,name_str):
    show_angle_on_img =True
    show_proj_img = True
    data = np.loadtxt(os.path.join(IMG_DIR,name_str+ "_cloudy_point_filter1.txt"))
    data = np.array(data)
    extractedPointCloud = data[:,0:4]
    leafIDs = np.unique(data[:,3])
    rowcols = data[:,4:6]
    jpg_files = glob.glob(os.path.join(IMG_DIR, "*.jpg"))
    meta_files = list(map(lambda x: os.path.join(os.path.dirname(x), os.path.splitext(os.path.basename(x))[0] + "_pitch.txt"), jpg_files))
    angle = read_pitch_angle(meta_files)/180.0*np.pi
    v = np.array([0, np.cos(angle), np.sin(-angle)])
    leaf_angles = []
    leafIDs_new = []
    for ID in leafIDs:
        leaf_points = extractedPointCloud[extractedPointCloud[:, 3] == ID][:, 0:3]
        if leaf_points.shape[0] >= 10:
            leaf_points = np.transpose(leaf_points)
            cps, plane, normal = planeFit_good(leaf_points)
            a = plane[1]/plane[2]
            if a > 5:
                normal = np.array(normal)
                dotproduct = np.dot(v, normal)
                leaf_angle = np.arccos(dotproduct)/np.pi*180
                if dotproduct < 0:
                    leaf_angle = 180 - leaf_angle
                leaf_angles.append(leaf_angle)
                leafIDs_new.append(ID)

    LAD_file_name=name_str+'_ID_LAD.txt'
    f1 = open(os.path.join(out_path,LAD_file_name), 'w')
    if show_angle_on_img:
         img = Image.open(jpg_files[0])
         img = np.array(img)
         plt.imshow(img)
         index = 0
         for ID in leafIDs_new:
             leaf_rowcols = rowcols[extractedPointCloud[:, 3] == ID]
             if leaf_rowcols.shape[0] >= 10:
                 rowcol = leaf_rowcols.mean(0)
                 row = rowcol[0]
                 col = rowcol[1]
                 plt.text(col-5, row, "%.2f" % leaf_angles[index],fontsize=2,color="k")
                 # plt.text(col - 5, row+30, "ID: %d" % index)
                 plt.text(col - 5, row + 30, "ID: %d" % ID,fontsize=2,color="k")
                 f1.write(str(index))
                 f1.write("  ")
                 f1.write(str(round(leaf_angles[index], 2)))
                 f1.write("  ")
                 f1.write(str(ID))
                 f1.write("\n")

                 index += 1
         plt.xticks([])
         plt.yticks([])
         plt.axis('off')
         plt.savefig(os.path.join(out_path, name_str + '_LAD.png'), dpi=600, bbox_inches='tight',pad_inches=0)
         plt.close()
    if show_proj_img:
         img = Image.open(jpg_files[0])
         img = np.array(img)
         plt.imshow(img)
         index = 0
         for ID in leafIDs_new:
             leaf_rowcols = rowcols[extractedPointCloud[:, 3] == ID]
             if leaf_rowcols.shape[0] >= 10:
                 plt.plot(leaf_rowcols[:, 1], leaf_rowcols[:, 0])
                 index += 1
         plt.xticks([])
         plt.yticks([])
         plt.axis('off')
         plt.savefig(os.path.join(out_path, name_str + '_LAD_project_point.png'), dpi=600,bbox_inches='tight', pad_inches=0)
         plt.close()

if __name__ == '__main__':
    folder_dir = r'I:\yangmeikeng_deal_2023\2023-02-16\sample3\14-30\1good'
    folder_list = os.listdir(folder_dir)
    for i in range(0, len(folder_list)):
        folder_path = os.path.join(folder_dir, folder_list[i])
        jpg_list = glob.glob(os.path.join(folder_path,"*.jpg"))  
        jpg_inpath = jpg_list[0]
        jpg_name = os.path.basename(jpg_inpath)  
        out_path = folder_path + '//' + 'out1'
        if not os.path.exists(out_path): 
            os.mkdir(out_path)
        else:
            print("folder is exist")
        tiqu_single_angle(folder_path,out_path,jpg_name[0:-4])