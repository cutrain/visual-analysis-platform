import os
import json
from config import COMPONENT_DIR

__all__ = [
    'component_detail',
]

component_detail = {}
fields = ['name', 'display', 'in_port', 'out_port', 'params']

for root, dirs, files in os.walk(COMPONENT_DIR):
    for file in files:
        if file is not 'structure.json' and file[-5:] == '.json':
            with open(os.path.join(root, file), 'rb') as f:
                data = json.load(f)
                if all([field in data for field in fields]):
                    component_detail.update({data['name']:data})
