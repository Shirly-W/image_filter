import cv2
import numpy as np
import os
import re
import matplotlib.pyplot as plt
# import PyQt5
import argparse
# dirname = os.path.dirname(PyQt5.__file__)
# plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def image_colorfulness(image_path):
    """

    :param image_path: 图片的路径
    :return: 图片的色彩鲜艳度
    """
    image = cv2.imread(image_path)

    #将图片分为B,G,R三部分（注意，这里得到的R、G、B为向量而不是标量）
    (B, G, R) = cv2.split(image.astype("float"))

    #rg = R - G
    rg = np.absolute(R - G)

    #yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)

    #计算rg和yb的平均值和标准差
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))

    #计算rgyb的标准差和平均值
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

    # 返回颜色丰富度C
    return stdRoot + (0.3 * meanRoot)

if __name__ == '__main__':
    #获取数据文件夹的名字
    parser = argparse.ArgumentParser(description='image_analyse')
    parser.add_argument("--file_name", required=True,help='obtain path ', type=str)
    args = parser.parse_args()
    img_dir=os.path.join(BASE_DIR,"image_data",args.file_name)
    # 获取所有图片的名字
    name_imgs = [p for p in os.listdir(img_dir) if p.endswith(('.png','.jpeg','.jpg'))]
    #获取所有图片的路径
    path_imgs = [os.path.join(img_dir, name) for name in name_imgs]
    #获取所有图片的鲜艳度
    colorfulness_list=[image_colorfulness(p) for p in path_imgs ]
    index_imgs=[int(re.findall("\d+",n)[0]) for n in name_imgs]
    #绘图
    plt.scatter(index_imgs,colorfulness_list)
    for x,y in zip(index_imgs,colorfulness_list):
        plt.text(x,y,x)
    plt.show()