Visual Analysis Platform

#enviroment
enviroment requirements
```
redis
python3
*MySQL # "SQL-command" require
```

installation for Ubuntu
```bash
sudo apt-get install python3
sudo apt-get install redis-server
pip install -r requirements.txt
```

installation for windows(x64)
```
download python3 from "https://www.python.org/downloads/"
download redis from "https://github.com/MicrosoftArchive/redis/releases"
pip install -r requirements.txt
```

#run
```bash
python3 manage.py runserver
```


#Develop this project
##How to add new type of node
add a json file `api/*/*.json`
follow the format such as
```json
{
  "name":"knn",
  "display":"k近邻",
  "inout":"in2out1",
  "attr": [
    {
      "name":"method",
      "display":"方法",
      "type":"list",
      "default":"classify",
      "list":["classify", "regress"]
    }
  ]
}
```
then input `python3 api/gen_params.py` to update api files
