HOST=0.0.0.0
PORT=8081
.PHONY: clean run install
install: app/graph/algorithm/image/yolov3/yolov3.weights
	pip3 install -r requirements.txt --user -i https://pypi.tuna.tsinghua.edu.cn/simple

app/graph/algorithm/image/yolov3/yolov3.weights:
	wget -P algorithm/image/yolov3 https://pjreddie.com/media/files/yolov3.weights 

run:
	python3 manage.py runserver -h ${HOST} -p ${PORT}

clean:
	find . -name "__pycache__" -type d -exec rm -rf '{}' \; -prune
	find . -name "*.pyc" -type f -exec rm -rf '{}' \; -prune
	rm back.log

