# yuan-tool

御安python项目的公共库，包含：```数据库连接 ip处理 端口处理 网址处理 编码解码 路径处理 shell执行```等多个通用模块


## **切记不要随意改动已有方法并更新！！！可能会导致现有程序报错！！！**


## 安装

   ```pip install yuan-tool ```

## 功能清单

es/kafka/mongodb/mq/mysql/rabbitmq/redis/sqlite的连接工具类

网页的识别，请求处理

ip的识别，切分，合并处理

端口的切分，合并处理

协程工具类

加密/解密工具类

文件操作工具类

路径操作（拼接，绝对路径，相对路径）工具类

shell执行工具类

时间转换工具类

## 更新

   由于已经编写好了```upload.py```脚本，更新流程如下：

   1. 增加```setup.py```中的版本号
   
   2. 更新引入包列表（如果有的话）
   
   3. 根据情况调整一下```upload.py```的内容（python3/python之类的）
   
   4. 执行```upload.py```
   
   5. 查看是否更新成功/更新项目
   
      ``````shell
       $ pip install -i https://pypi.python.org/pypi/ yuan-tool --upgrade

   > 目前设置上传到pypi的只有yuantool目录下的内容，关于上传非包文件:
   > 在setup.py同级目录下创建MANIFEST.in文件，里面的内容是需要上传的文件
   >
   > 例如，如果要包括项目下的所有文件：
   > recursive-include fastproject *
   >
   > 为了将这些文件在安装时复制到site-packages中的包文件夹，需要将setup中的include_package_data设置为True

## 新建公共库


   1. 获取项目下所有引入的包
   
      ```shell
      $ pipreqs ./yuantool --force
      ```
   
   2. 预备工作
   
      ```shell
      $ python3 -m pip install setuptools wheel twine
      ```
   
   3. 创建分发
   
      ```shell
      $ python3 setup.py sdist bdist_wheel
      ```
   
   4. 上传包
   
      ```shell
      $ python3 -m twine upload dist/*
      ```





