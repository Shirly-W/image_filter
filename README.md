# 图片爬取+筛选

## 所需库

pip3 install -r requirements.txt

或者

pip install umap-learn   
pip install opencv-python   
pip install matplotlib  
pytorch  
 


  
## 数据加载
将数据放到image_data文件夹下


## 运行   
运行初级数据筛选(file_name放在image_data文件夹下图片文件夹的名字)：
```
python img_primary_filter.py --file_name
```   
   
运行高级数据筛选(file_name放在image_data文件夹下图片文件夹的名字)：
```
python img_advanced_filter.py --file_name

```  
查看图片鲜艳度(file_name放在image_data文件夹下图片文件夹的名字)：
```
python img_analyse.py --file_name
```   
 
