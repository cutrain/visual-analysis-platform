__all__ = [
    'video_size',
    'video_monorec',
]

def video_size(video_opt_list, **kwargs):
    import cv2
    left = int(kwargs.pop('left'))
    top = int(kwargs.pop('top'))
    right = int(kwargs.pop('right'))
    bottom = int(kwargs.pop('bottom'))
    ret = video_opt_list.copy()
    ret.append(lambda x:x[top:bottom,left:right])
    return ret

def video_monorec(video_opt_list, **kwargs):
    import cv2
    from ..image.image_monorec import image_monorec

    class_ = kwargs.pop('class_')
    func = lambda x:image_monorec([x], class_=class_)[0]

    ret = video_opt_list.copy()
    ret.append(func)
    return ret
