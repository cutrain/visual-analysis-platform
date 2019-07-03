import os
import json

from tool import safepath
from config import DATA_DIR

__all__ = [
    'data_instream',
    'data_outstream',
    'sql_instream',
    'sql_outstream',
    'model_instream',
    'model_outstream',
    'image_instream',
    'image_outstream',
    'graph_instream',
    'graph_outstream',
    'video_instream',
    'video_outstream',
    'seq_instream',
    'seq_outstream',
    'text_instream',
    'text_outstream',
]

def datapath(path):
    global DATA_DIR
    path = safepath(path)
    path = os.path.join(DATA_DIR, path)
    return path

def remake_path(path, suffix):
    s = os.path.splitext(path)[1]
    if s == '':
        return path + '.' + suffix
    if s == '.':
        return path + suffix
    return path

def data_instream(**kwargs):
    import pandas as pd
    num = int(kwargs.pop('read_number'))
    header = kwargs.pop('header')
    path = kwargs.pop('path')
    path = datapath(path)
    if num == 0:
        num = None
    if header == 'True':
        df = pd.read_csv(path, nrows=num)
    else:
        df = pd.read_csv(path, nrows=num, header=None)
        df.columns = list(map(str, df.columns))
    return df

def data_outstream(data, **kwargs):
    import pandas as pd
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'csv')
    data.to_csv(path, encoding='utf-8', index=False)

def sql_instream(**kwargs):
    import pandas as pd
    from sqlalchemy import create_engine
    dbtype = kwargs.pop('database_type')
    host = kwargs.pop('address')
    port = int(kwargs.pop('port'))
    user = kwargs.pop('user')
    passwd = kwargs.pop('password')
    dbname = kwargs.pop('database_name')
    command = kwargs.pop('command')
    if dbtype == 'MySQL':
        URI = "mysql+pymysql://" + \
                user + ':' + \
                passwd + '@' + \
                host + ':' + \
                str(port) + '/' + \
                dbname
    else:
        raise NotImplementedError

    sql_engine = create_engine(URI)
    data = pd.read_sql(command, sql_engine)
    return data

def sql_outstream(data, **kwargs):
    import pandas as pd
    from sqlalchemy import create_engine
    dbtype = kwargs.pop('database_type')
    host = kwargs.pop('address')
    port = int(kwargs.pop('port'))
    user = kwargs.pop('user')
    passwd = kwargs.pop('password')
    dbname = kwargs.pop('database_name')
    table_name = kwargs.pop('table_name')
    exist_method = kwargs.pop('if_exists')
    if dbtype == "MySQL":
        URI = "mysql+pymysql://" + \
                user + ':' + \
                passwd + '@' + \
                host + ':' + \
                str(port) + '/' + \
                dbname
    else:
        raise NotImplementedError

    sql_engine = create_engine(URI)
    data.to_sql(table_name, con=sql_engine, if_exists=exist_method)

def model_instream(**kwargs):
    from sklearn.externals import joblib
    path = kwargs.pop('path')
    path = datapath(path)
    model = joblib.load(path)
    return model

def model_outstream(model, **kwargs):
    from sklearn.externals import joblib
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'model')
    joblib.dump(model, path)

def image_instream(**kwargs):
    import cv2
    path = kwargs.pop('path')
    gray = kwargs.pop('gray')
    num = int(kwargs.pop('num'))
    path = datapath(path)
    images = []
    names = []
    cnt = 0
    if num <= 0:
        num = None
    if os.path.isdir(path):
        for f in sorted(os.listdir(path)):
            p = os.path.join(path, f)
            if os.path.isfile(p):
                if gray == 'true':
                    image = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
                else:
                    image = cv2.imread(p)
                if image is not None:
                    images.append(image)
                    names.append(f)
                    cnt += 1
                    if num is not None and cnt >= num:
                        break
    else:
        if gray == 'true':
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(path)
        if image is not None:
            images.append(image)
            names.append(os.path.basename(path))
    if len(images) == 0:
        raise FileNotFoundError("There is no images")
    ret = [images, names]
    return ret

def image_outstream(images_in, **kwargs):
    import cv2
    path = kwargs.pop('path')
    path = datapath(path)
    images = images_in[0]
    names = images_in[1]
    if len(images) == 1:
        cv2.imwrite(path, images[0])
    else:
        if not os.path.exists(path):
            os.mkdir(path)
        for i, image in enumerate(images):
            cv2.imwrite(os.path.join(path, names[i]), image)

def video_instream(**kwargs):
    import cv2
    path = kwargs.pop('path')
    path = datapath(path)
    video = cv2.VideoCapture(path)
    if video.isOpened() == False:
        raise FileNotFoundError
    video.release()
    return [path]

def video_outstream(video_opt_list, **kwargs):
    import cv2
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'avi')
    fourcc = kwargs.pop('codecc')
    fps = int(kwargs.pop('fps'))
    width = int(kwargs.pop('width'))
    height = int(kwargs.pop('height'))
    frame_start = int(kwargs.pop('frame_start'))
    frame_length = int(kwargs.pop('frame_length'))

    cap = cv2.VideoCapture(video_opt_list[0])

    if fps == 0:
        fps = cap.get(cv2.CAP_PROP_FPS)
    else:
        cap.set(cv2.CAP_PROP_FPS, fps)
    if width == 0:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    if height == 0:
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

    if frame_start != 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)


    funcs = []
    for i in range(1, len(video_opt_list)):
        if callable(video_opt_list[i]):
            funcs.append(video_opt_list[i])
        else:
            raise NotImplementedError

    if fourcc == 'origin':
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    else:
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
    videoWriter = cv2.VideoWriter(path, fourcc, fps, (width, height))
    if not videoWriter.isOpened():
        raise Exception("Video couldn't not write, please check codec, path or storage")
    cnt = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret and (frame_length != 0):
            cnt += 1
            if cnt % 10 == 0:
                print('have solve {} frames'.format(cnt), flush=True)
            for func in funcs:
                frame = func(frame)
            if frame.shape[0] != height or frame.shape[1] != width:
                frame = cv2.resize(frame, (width, height))
            videoWriter.write(frame)
            frame_length -= 1
        else:
            break
    cap.release()
    videoWriter.release()

def graph_instream(**kwargs):
    from .graph.graphio import from_json_dicts, from_json_lists, from_mat_matrix
    path = kwargs.pop('path')
    path = datapath(path)
    graph = from_json_dicts(path)
    if graph is None:
        graph = from_json_lists(path)
    if graph is None:
        graph = from_mat_matrix(path)
    if graph is None:
        raise NotImplementedError
    return graph

def graph_outstream(graph, **kwargs):
    import networkx
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'json')
    graph_json = networkx.to_dict_of_dicts(graph)
    data = json.dumps(graph_json)
    with open(path, 'w') as f:
        f.write(data)

def seq_instream(**kwargs):
    path = kwargs.pop('path')
    path = datapath(path)
    with open(path, 'r') as f:
        seq = json.load(f)
    return seq

def seq_outstream(seq, **kwargs):
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'json')
    with open(path, 'w') as f:
        json.dump(seq, f)

def text_instream(**kwargs):
    method = kwargs.pop('method')
    if method == 'file':
        path = kwargs.pop('path')
        path = datapath(path)
        with open(path, 'r') as f:
            text = f.read()
    else:
        text = kwargs.pop('text')
    return text

def text_outstream(text, **kwargs):
    path = kwargs.pop('path')
    path = datapath(path)
    path = remake_path(path, 'txt')
    with open(path, 'w') as f:
        f.write(text)
