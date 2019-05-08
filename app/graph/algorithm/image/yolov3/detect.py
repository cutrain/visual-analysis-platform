import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import os
import sys

from .util import *
from .darknet import Darknet
from .preprocess import inp_to_image, prep_image

__module_path = os.path.dirname(sys.modules[__package__].__file__)

confidence = 0.6
nms_thresh = 0.4
cfgfile = os.path.join(__module_path, 'cfg/yolov3.cfg')
weightsfile = os.path.join(__module_path, 'yolov3.weights')
reso='416'
CUDA = torch.cuda.is_available()

num_classes = 80
classes = load_classes(os.path.join(__module_path, 'data/coco.names'))

# Set up the neural network
print('Loading Yolo')
model = Darknet(cfgfile)
model.load_weights(weightsfile)

model.net_info["height"] = reso
inp_dim = int(model.net_info["height"])
assert inp_dim % 32 == 0
assert inp_dim > 32

# If there's a GPU availible, put the model on GPU
if CUDA:
    model.cuda()
# Set the model in evaluation mode
model.eval()

def detect(image, class_):
    global inp_dim, model, classes, num_classes, CUDA, confidence, nms_thresh


    batches = list(map(prep_image, [image], [inp_dim]))
    im_batches = [x[0] for x in batches]
    orig_ims = [x[1] for x in batches]
    im_dim_list = [x[2] for x in batches]
    im_dim_list = torch.FloatTensor(im_dim_list).repeat(1,2)


    if CUDA:
        im_dim_list = im_dim_list.cuda()

    i = 0

    write = False

    objs = {}


    for batch in im_batches:
        if CUDA:
            batch = batch.cuda()


        with torch.no_grad():
            prediction = model(Variable(batch), CUDA)

        prediction = write_results(prediction, confidence, num_classes, nms = True, nms_conf = nms_thresh)

        if type(prediction) == int:
            i += 1
            continue

        prediction[:,0] += i

        if not write:
            output = prediction
            write = 1
        else:
            output = torch.cat((output,prediction))

        i += 1

        # if CUDA:
            # torch.cuda.synchronize()

    try:
        output
    except NameError:
        print("No detections were made")
        exit()

    im_dim_list = torch.index_select(im_dim_list, 0, output[:,0].long())

    scaling_factor = torch.min(inp_dim/im_dim_list,1)[0].view(-1,1)


    output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim_list[:,0].view(-1,1))/2
    output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim_list[:,1].view(-1,1))/2


    output[:,1:5] /= scaling_factor

    for i in range(output.shape[0]):
        output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim_list[i,0])
        output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim_list[i,1])

    def write(x, batches, results, class_):
        cls = int(x[-1])
        if classes[cls] not in class_:
            return None
        c1 = tuple(x[1:3].int().cpu().numpy())
        c2 = tuple(x[3:5].int().cpu().numpy())
        ret = []
        ret.extend(sorted([int(c1[1]), int(c2[1])]))
        ret.extend(sorted([int(c1[0]), int(c2[0])]))
        return ret


    # torch.cuda.empty_cache()
    ret = []
    for i in output:
        a = write(i, im_batches, orig_ims, class_)
        if a is not None:
            ret.append(a)
    return ret

