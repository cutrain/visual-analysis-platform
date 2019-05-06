__all__ = [
    'image_resolution',
    'image_channel',
    'image_large',
    'image_small',
    'image_cut',
    'image_blur',
    'image_dilate',
    'image_erode',
    'image_close',
    'image_open',
    'image_brightness_contrast',
    'image_noiseness',
    'image_blend',
]
def image_resolution(images, **kwargs):
    import cv2
    reso = kwargs.pop('reso')
    width, height = map(int, reso.split(','))
    result_images = list(map(lambda x:cv2.resize(x, (width, height)), images))
    return result_images

def image_channel(images, **kwargs):
    import cv2
    method = kwargs.pop('method')
    mmap = {
        'BGR2GRAY':cv2.COLOR_BGR2GRAY,
        'BGR2RGB':cv2.COLOR_BGR2RGB,
        'HSV2BGR':cv2.COLOR_HSV2BGR,
        'BGR2HSV':cv2.COLOR_BGR2HSV,
    }[method]
    result_images = list(map(lambda x:cv2.cvtColor(x, mmap), images))
    return result_images

def image_large(images, **kwargs):
    import cv2
    result_images = list(map(lambda x:cv2.pyrUp(x), images))
    return result_images

def image_small(images, **kwargs):
    import cv2
    result_images = list(map(lambda x:cv2.pyrDown(x), images))
    return result_images

def image_cut(images, **kwargs):
    import cv2
    left = int(kwargs.pop('left'))
    right = int(kwargs.pop('width')) + left
    top = int(kwargs.pop('top'))
    bottom = int(kwargs.pop('height')) + top
    result_images = list(map(lambda x:x[top:bottom, left:right], images))
    return result_images

def image_blur(images, **kwargs):
    import cv2
    method = kwargs.pop('method')
    kernel = tuple(map(int,kwargs.pop('kernel_size').split(',')))
    func = {
        'linear':lambda x:cv2.blur(x, kernel),
        'gaussian':lambda x:cv2.GaussianBlur(x, kernel, 0),
        'median':lambda x:cv2.medianBlur(x, kernel[0]),
    }[method]
    result_images = list(map(func, images))
    return result_images

def image_dilate(images, **kwargs):
    import cv2
    import numpy as np
    kernel_size = tuple(map(int, kwargs.pop('kernel_size').split(',')))
    iter_n = int(kwargs.pop('iterations'))
    kernel = np.ones(kernel_size, np.uint8)
    result_images = list(map(lambda x:cv2.dilate(x, kernel, iterations=iter_n), images))
    return result_images
[0]
def image_erode(images, **kwargs):
    import cv2
    import numpy as np
    kernel_size = tuple(map(int, kwargs.pop('kernel_size').split(',')))
    iter_n = int(kwargs.pop('iterations'))
    kernel = np.ones(kernel_size, np.uint8)
    result_images = list(map(lambda x:cv2.erode(x, kernel, iterations=iter_n), images))
    return result_images

def image_close(images, **kwargs):
    import cv2
    import numpy as np
    kernel_size = tuple(map(int, kwargs.pop('kernel_size').split(',')))
    iter_n = int(kwargs.pop('iterations'))
    kernel = np.ones(kernel_size, np.uint8)
    result_images = list(map(lambda x:cv2.morphologyEx(x, cv2.MORPH_CLOSE, kernel), images))
    return result_images

def image_open(images, **kwargs):
    import cv2
    import numpy as np
    kernel_size = tuple(map(int, kwargs.pop('kernel_size').split(',')))
    iter_n = int(kwargs.pop('iterations'))
    kernel = np.ones(kernel_size, np.uint8)
    result_images = list(map(lambda x:cv2.morphologyEx(x, cv2.MORPH_OPEN, kernel), images))
    return result_imkernels

def image_noiseness(images, **kwargs):
    import cv2
    import numpy as np
    mean = float(kwargs.pop('mean'))
    std = float(kwargs.pop('std'))
    result_images = []
    for i in images:
        noise = np.random.normal(mean, std, i.shape)
        result_images.append(np.clip(i.astype('float') + noise, 0, 255).astype('uint8'))
    return result_images

def image_brightness_contrast(images, **kwargs):
    import cv2
    import numpy as np
    brightness_shift = int(kwargs.pop('brightness_shift'))
    contrast_shift = float(kwargs.pop('contrast_shift'))
    result_images = list(map(lambda x:np.clip(x.astype('float') * contrast_shift + brightness_shift, 0, 255).astype('uint8'), images))
    return result_images

def image_blend(images1, images2, **kwargs):
    import cv2
    import numpy as np
    method = kwargs.pop('method')
    gamma = int(kwargs.pop('gamma'))
    gamma = max(min(100, gamma), 0)
    gamma = gamma * 0.01
    result_images = []
    if method == 'linear':
        l = min(len(images1), len(images2))
        for i in range(l):
            result_images.append((images1[i]*(1-gamma) + images2[i]*gamma).astype('uint8'))
        for i in range(l, len(images1)):
            result_images.append(images1[i])
        for i in range(l, len(images2)):
            result_images.append(images2[i])
    elif method == 'add':
        l = min(len(images1), len(images2))
        for i in range(l):
            result_images.append(np.clip(images1[i].astype('float') + images2[i]*gamma, 0, 255).astype('uint8'))
        for i in range(l, len(images1)):
            result_images.append(images1[i])
        for i in range(l, len(images2)):
            result_images.append((images2[i] * gamma).astype('uint8'))
    else:
        raise NotImplementedError
    return result_images
