__all__ = [
    'image_monorec',
]
def my_rectangle(img, p1, p2, color, thick):
    size = img.shape
    l = min(p1[0], p2[0])
    r = max(p1[0], p2[0])
    b = min(p1[1], p2[1])
    t = max(p1[1], p2[1])
    # left line
    for i in range(max(0, l-thick),min(img.shape[1],l+thick)):
        img[max(0,b-thick):min(img.shape[0],t+thick),i] = color
    # right line
    for i in range(max(0, r-thick),min(img.shape[1],r+thick)):
        img[max(0,b-thick):min(img.shape[0],t+thick),i] = color
    # bottom line
    for i in range(max(0, b-thick),min(img.shape[0],b+thick)):
        img[i,max(0,l-thick):min(img.shape[1],r+thick)] = color
    # top line
    for i in range(max(0, t-thick),min(img.shape[0],t+thick)):
        img[i,max(0,l-thick):min(img.shape[1],r+thick)] = color
    return img

def draw_boxes(img, bboxes, color=(255, 0, 0), thick=3, copy=True):
    import numpy as np
    if copy:
        imcopy = np.copy(img)
    else:
        imcopy = img
    for bbox in bboxes:
        # in cv2.rectangle, it's (col, row), (col, row) format
        if len(bbox) == 2:
            # bbox[[row1,col1],[row2,col2]]
            # cv2.rectangle(imcopy, (bbox[0][1], bbox[0][0]), (bbox[1][1], bbox[1][0]), color, thick)
            my_rectangle(imcopy, (bbox[0][1], bbox[0][0]), (bbox[1][1], bbox[1][0]), color, thick)
        else:
            # bbox[row1,row2,col1,col2]
            # cv2.rectangle(imcopy, (bbox[2], bbox[0]), (bbox[3], bbox[1]), color, thick)
            my_rectangle(imcopy, (bbox[2], bbox[0]), (bbox[3], bbox[1]), color, thick)
    return imcopy

def image_monorec(images_in, **kwargs):
    # class_ : see yolov3/data/coco.names
    import cv2
    import numpy as np
    from .yolov3.detect import detect
    class_ = kwargs.pop('class_').split(',')
    images = images_in[0]
    names = images_in[1]

    result_images = []
    for image in images:
        if len(image.shape) == 3:
            image = image[:,:,::-1].copy()
        bbox = detect(image, class_)
        image = draw_boxes(image, bbox, copy=False)
        if len(image.shape) == 3:
            image = image[:,:,::-1].copy()
        result_images.append(image)
    return [result_images, names]
