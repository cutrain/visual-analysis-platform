# Visual Analysis Platform

## 使用指南
见[wiki](https://github.com/cutrain/visual-analysis-platform/wiki "数据分析平台wiki")

### 运行环境要求
```
redis
python >= 3.4
```

### Ubuntu 安装
Install python3 & pip & redis
```bash
sudo apt-get install python3 python3-pip
sudo apt-get install redis-server
```
Download source
```bash
git clone https://github.com/cutrain/visual-analysis-platform
```
Install enviroments
```bash
cd visual-analysis-platform
make install
```
or
```bash
cd visual-analysis-platform
pip install -r requirements.txt
wget -P app/graph/algorithm/image/yolov3 https://pjreddie.com/media/files/yolov3.weights 
```

### windows(x64) 安装
```
download python3 from "https://www.python.org/downloads/"
download redis from "https://github.com/MicrosoftArchive/redis/releases"
pip install -r requirements.txt
download yolov3 weights from https://pjreddie.com/media/files/yolov3.weights, and put in app/graph/algorithm/image/yolov3

```


## 运行
```bash
python3 manage.py runserver -p 8080
```
or
```bash
make run
```
访问 http://localhost:8080 可以使用

# 参与开发
查看[手册](https://github.com/cutrain/visual-analysis-platform/blob/master/manual.doc "手册")


bug反馈或其它问题请联系 duanyuge@qq.com 或 微信 cutrain_

