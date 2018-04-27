import json as js
from urllib import request

if __name__ == "__main__":
    args = {}
    all_nodes = {
        'data-instream1':'data-instream'
    }
    all_lines = {}
    nodes_details = {
        'data-instream1':{
            'path':'/home/cutrain/project/visual-analysis-platform/test/HTRU_2.csv'
        }
    }
    args.update(
        {
            'all_nodes':all_nodes,
            'all_lines':all_lines,
            'nodes_details':nodes_details
        }
    )
    url = "http://localhost:8081"
    args = js.dumps(args).encode()
    req = request.urlopen(url + '/main/run', args)
    print(req)

