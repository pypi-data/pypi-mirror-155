# cgai-io

#### 介绍
一个简单轻量又快速的数据流操作python库

支持跨平台，支持window文件以及目录的快速复制
支持文件及文件目录删除，支持目录删除保留原目录结构
支持文件及目录移动,重命名
支持文件及目录打包与解压zip

#### 安装教程

```cmd
pip install cgai-io
```

#### 快速上手

###### 1.复制文件  
```python
from cgai_io.Copy import copyfile

src1 = r'D:\MZ\bg.jpg'
des1 = r'D:\Temp\Test\bg.jpg'

copyfile(src1,des1)
```
###### 2.复制文件目录
```python
from cgai_io.Copy import copydir

src2 = r'D:\MZ'
des2 = r'D:\Temp\Test\MZ'

copydir(src2,des2)
```

###### 3.删除文件及文件目录
```python
from cgai_io.Delete import delfile,deldir,delall


# #删除文件
# path = r'\\192.168.1.248\3d\temp\a\cmd_mac.py'
# delfile(path)


# #删除文件夹
# path = r'D:\BaiduNetdiskDownload\AA'
# deldir(path,keep_dir=True)  #保留空目录结构


#无论文件或文件夹都直接删除
# path = r'D:\BaiduNetdiskDownload\ktk_103024'
# delall(path)
```

###### 4.官方案例
```python
import cgai_io as ci


# #复制文件
# src = r'D:\Temp\2.jpg'
# des = r'D:\Temp\2_bak.jpg'
# ci.copyfile(src,des)


# #复制文件目录
# src = r'D:\Temp\AA'
# des = r'D:\Temp\BB'
# ci.copydir(src,des)


# #删除文件
# des = r'D:\Temp\2_bak.jpg'
# ci.delfile(des)

# # 删除文件目录
# des = r'D:\Temp\BB'
# ci.deldir(des)

# # 删除文件或目录
# des = r'D:\Temp\BB'
# ci.delall(des)

# #移动文件
# src = r'D:\Temp\AA'
# des = r'D:\Temp\BB'
# ci.mvfile(src,des)

# # 移动文件目录
# src = r'D:\Temp\AA'
# des = r'D:\Temp\testA\AA'
# ci.mvdir(src,des)

# # 移动文件或目录
# src = r'D:\Temp\testA\AA'
# des = r'D:\Temp\AA'
# ci.mv(src,des)


# 重命名文件或目录
# src = r'D:\Temp\AA\A.jpg'
# des = r'D:\Temp\AA\B.jpg'
# ci.rename(src,des)

# src = r'D:\Temp\AA'
# des = r'D:\Temp\BB'
# ci.rename(src,des)


# # 文件添加前缀
# src = r'D:\Temp\BB\B.jpg'
# prefix = 'img_'
# ci.addPrefix(src,prefix)  # r'D:\Temp\BB\img_B.jpg'

# # 文件目录添加前缀
# src = r'D:\Temp\BB'
# prefix = 'dir_'
# ci.addPrefix(src,prefix) # r'D:\Temp\dir_BB'


# # 文件添加尾缀
# src =r'D:\Temp\dir_BB\img_B.jpg'
# suffix = '_001'
# ci.addSuffix(src,suffix) # D:\Temp\dir_BB\img_B_001.jpg

# # 文件目录添加尾缀
# src = r'D:\Temp\dir_BB'
# suffix = '_v001'
# ci.addSuffix(src,suffix)  # r'D:\Temp\dir_BB_v001'



# # 文件打包zip
# src = r'D:\Temp\dir_BB\img_B.jpg'
# des = r'D:\Temp\dir_BB\B.zip'
# ci.pack(src,des)


# # 文件目录打包zip
# src = r'D:\Temp\dir_BB'
# des = r'D:\Temp\BB.zip'
# ci.pack(src,des)



# # 解压文件或目录
# src_zip = r'D:\Temp\A\BB.zip'
# des_dir = r'D:\Temp\A\C'
# ci.unpack(src_zip,des_dir)
```

#### 交流方式
WeChat : zxzxde / 360014296