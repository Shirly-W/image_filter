import os
import cv2
import shutil
import numpy as np
import matplotlib.pyplot as plt
import re
import PyQt5
import argparse
# dirname = os.path.dirname(PyQt5.__file__)
# plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 检测输入图像是否需要
def check_img(img_path,img_index,img_gradient_list):
    img = cv2.imread(img_path, flags=cv2.IMREAD_COLOR)

    # file info
    file_size = os.path.getsize(img_path)
    img_height, img_width = img.shape[:2]
    if file_size < 10*1024 or img_width < 224 or img_height < 224:
        return False

    # image basic feature
    img_dy = img[:img_height-1] - img[1:]
    img_dx = img[:, :img_width-1] - img[:, 1:]
    img_gradient = np.mean(np.abs(img_dx)) + np.mean(np.abs(img_dy))
    # print(img_path, "img_gradient =", img_gradient)
    img_index.append(int(re.findall("\d+",img_path)[0]))
    img_gradient_list.append(img_gradient)
    if img_gradient < 190:
        return False
    return True

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
    # 获取数据文件夹的名字
    parser = argparse.ArgumentParser(description='image_analyse')
    parser.add_argument("--file_name", required=True, help='obtain path ', type=str)
    args = parser.parse_args()
    root_dir = os.path.join(BASE_DIR, "image_data", args.file_name)
    file_suffix = "jpeg|jpg|png"
    remove_dir = root_dir + "/remove"
    img_index=[]
    img_gradients=[]
    if not os.path.exists(remove_dir):
        os.makedirs(remove_dir)
    for img_name in os.listdir(root_dir):
        # 对处理文件的类型进行过滤
        if re.search(file_suffix, img_name) is None:
            continue
        img_path = root_dir + "/" + img_name
        if not check_img(img_path,img_index,img_gradients) or image_colorfulness(img_path)>80 or image_colorfulness(img_path)==0:
            output_path = remove_dir + "/" + img_name
            shutil.move(img_path, output_path)
    # print(img_index)
    #梯度图
    plt.scatter(img_index,img_gradients)
    plt.title("image gradient")
    for x,y in zip(img_index,img_gradients):
        plt.text(x,y,x)
    plt.show()
