# Visual Analysis Platform

## 使用指南
见[wiki](https://github.com/cutrain/visual-analysis-platform/wiki "数据分析平台wiki")

### 运行环境要求
```
redis
python >= 3.4
*MySQL # "SQL-command" require
```

### Ubuntu 安装
```bash
sudo apt-get install python3
sudo apt-get install redis-server
pip install -r requirements.txt
# if you want use SQL Server input following
# sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc 
# pip install pymssql
```

### windows(x64) 安装
```
download python3 from "https://www.python.org/downloads/"
download redis from "https://github.com/MicrosoftArchive/redis/releases"
pip install -r requirements.txt
```


## 运行
```bash
python3 manage.py runserver -p 8080
```
访问 http://localhost:8080 可以使用
数据的输入和输出如果不给绝对地址则会在项目的data 文件夹下存储，建议将需要使用的数据放到data文件夹中

# Develop
see [manual](https://github.com/cutrain/visual-analysis-platform/manual.doc "manual")


bug反馈或其它问题请联系 duanyuge@qq.com 或 微信 cutrain_

