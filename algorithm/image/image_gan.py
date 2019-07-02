__all__ = [
    'image_gan',
    'image_gan_apply',
]

def image_gan(images, **kwargs):
    from .gan import Gan
    import torch
    import numpy as np
    latent_dim = int(kwargs.pop('latent_dim'))
    num_round = int(kwargs.pop('num_round'))
    learning_rate = float(kwargs.pop('learning_rate'))
    batch_size = int(kwargs.pop('batch_size'))

    shape = images[0].shape
    if len(shape) == 2:
        channel = 1
    else:
        channel = shape[2]
    height, width = shape[:2]
    data = np.stack(images)
    data = data.astype(np.float64)
    data /= 128.
    data -= 1.
    model = Gan((height, width, channel), latent_dim)
    cuda = torch.cuda.is_available()
    model.train(num_round, learning_rate, batch_size, data, cuda=cuda)
    return model

def image_gan_apply(pytorchModel, **kwargs):
    num = int(kwargs.pop('num'))
    gen = pytorchModel.predict(num)
    gen += 1.
    gen *= 128.
    gen = gen.clip(0,255)
    gen = gen.astype('uint8')
    ret = []
    for i in range(len(gen)):
        ret.append(gen[i])
    return ret


