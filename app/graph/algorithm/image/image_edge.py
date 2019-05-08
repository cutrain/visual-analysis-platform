__all__ = [
    'image_edge',
]

def image_edge(images, **kwargs):
    import cv2
    isblur = kwargs.pop('isblur')
    thresh_min = int(kwargs.pop('thresh_min'))
    thresh_max = int(kwargs.pop('thresh_max'))
    result_images = []
    for image in images:
        if isblur == 'yes':
            image = cv2.GaussianBlur(image, (5,5), 0)
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.Canny(image, thresh_min, thresh_max)
        result_images.append(image)
    return result_images
