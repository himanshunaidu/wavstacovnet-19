import os
import math
import pywt
import numpy as np
from PIL import Image, ImageOps

from config import train_path, test_path
from config import covid_path_name, covid_std_path_name, covid_dwt_path_name, covid_dwt_path_name_2
from config import normal_path_name, normal_std_path_name, normal_dwt_path_name
from config import bacterial_path_name, bacterial_std_path_name, bacterial_dwt_path_name
from config import viral_path_name, viral_std_path_name, viral_dwt_path_name

#Main function for creating DWT sets from datasets
def gen_DWTs(root_path, src_path, dst_path):
    dir_path = os.path.join(root_path, src_path)
    data_files = os.listdir(dir_path)

    for file in data_files:
        image_path = os.path.join(root_path, src_path, file)
        img_norm_cA = get_dwt2(image_path)
        img_norm_cA.save(os.path.join(root_path, dst_path, 'dmey_dwt_' + file))
        print(file)

#Creates DWT of single images
def get_dwt2(image_path):
    img_bgr = Image.open(image_path)
    print(img_bgr.size)
    np_bgr = np.asarray(img_bgr)

    #cA = pywt.wavedec2(np_bgr, 'db2', mode='periodization', level=2)[0]
    #Single-Level decomposition
    cA, coEffs = pywt.dwt2(np_bgr, 'dmey', axes=(0, 1))
    print(cA.shape)
    norm_cA = normalize(cA)
    print(norm_cA.shape)
    norm_cA = norm_cA.astype(np.uint8)
    #print(norm_cA)
    img_norm_cA = Image.fromarray(norm_cA)
    img_norm_cA = img_norm_cA.resize((224,224))
    return img_norm_cA

    # cH = coEffs[0]
    # norm_cH = normalize(cH)
    # norm_cH = norm_cH.astype(np.uint8)
    # img_norm_cH = Image.fromarray(norm_cH)#.convert('L')
    # # return img_norm_cH

    # cV = coEffs[1]
    # norm_cV = normalize(cV)
    # norm_cV = norm_cV.astype(np.uint8)
    # img_norm_cV = Image.fromarray(norm_cV)#.convert('L')

    # cD = coEffs[2]
    # norm_cD = normalize(cD)
    # norm_cD = norm_cD.astype(np.uint8)
    # img_norm_cD = Image.fromarray(norm_cD)#.convert('L')

    # img_hor1 = get_concat_h(img_norm_cA, img_norm_cH)
    # img_hor2 = get_concat_h(img_norm_cV, img_norm_cD)
    # img_ver = get_concat_v(img_hor1, img_hor2)
    # img_ver.save(os.path.join(train_path, 'all.png'))

#Normalize images whose pixel values range goes beyond (0, 255)
def normalize(array):
    #img = Image.fromarray(img)
    #array = np.asarray(img)

    max = -math.inf
    min = math.inf
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            for k in range(array.shape[2]):
                if array[i][j][k]>max:
                    max = array[i][j][k]
                if array[i][j][k]<min:
                    min = array[i][j][k]
    print(min, max)

    array1 = (array-min)*255/(max-min)
    return array1

def get_concat_h(im1, im2):
    dst = Image.new('L', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('L', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

if __name__ == '__main__':
    gen_DWTs(train_path, covid_std_path_name, covid_dwt_path_name)
    # gen_DWTs(test_path, normal_std_path_name, normal_dwt_path_name)
    # gen_DWTs(test_path, bacterial_std_path_name, bacterial_dwt_path_name)
    # gen_DWTs(test_path, viral_std_path_name, viral_dwt_path_name)
    #gen_DWTs(train_path, normal_std_path_name, normal_dwt_path_name)
    #get_dwt2('E:\\Research\\5. Covid DWT\\Train\\COVID_STD\\0a7faa2a.png')