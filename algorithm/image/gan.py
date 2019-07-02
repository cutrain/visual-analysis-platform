import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.autograd import Variable
import torch


class Gan:

    class Generator(nn.Module):
        def __init__(self, img_shape, latent_dim):
            super().__init__()
            self.img_shape = img_shape
            self.latent_dim = latent_dim

            def block(in_feat, out_feat, normalize=True):
                layers = [nn.Linear(in_feat, out_feat)]
                if normalize:
                    layers.append(nn.BatchNorm1d(out_feat, 0.8))
                layers.append(nn.LeakyReLU(0.2, inplace=True))
                return layers

            self.model = nn.Sequential(
                *block(latent_dim, 128, normalize=False),
                *block(128, 256),
                *block(256, 512),
                *block(512, 1024),
                nn.Linear(1024, int(np.prod(img_shape))),
                nn.Tanh()
            )

        def forward(self, z):
            img = self.model(z)
            img = img.view(img.size(0), *self.img_shape)
            return img

    class Discriminator(nn.Module):
        def __init__(self, img_shape):
            super().__init__()

            self.model = nn.Sequential(
                nn.Linear(int(np.prod(img_shape)), 512),
                nn.LeakyReLU(0.2, inplace=True),
                nn.Linear(512, 256),
                nn.LeakyReLU(0.2, inplace=True),
                nn.Linear(256, 1),
                nn.Sigmoid(),
            )

        def forward(self, img):
            img_flat = img.view(img.size(0), -1)
            validity = self.model(img_flat)

            return validity

    def __init__(self, img_shape, latent_dim):
        self.generator = Gan.Generator(img_shape, latent_dim)
        self.discriminator = Gan.Discriminator(img_shape)
        self.latent_dim = latent_dim

    def train(self, num_rounds, learning_rate, batch_size, data, cuda=False):
        dataloader = DataLoader(
            data,
            num_workers=0,
            shuffle=False,
            batch_size=batch_size
        )
        Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
        adversarial_loss = torch.nn.BCELoss()
        optimizer_G = torch.optim.Adam(self.generator.parameters(), lr=learning_rate)
        optimizer_D = torch.optim.Adam(self.discriminator.parameters(), lr=learning_rate)
        for epoch in range(num_rounds):
            for i, imgs in enumerate(dataloader):

                # Adversarial ground truths
                valid = Variable(Tensor(imgs.size(0), 1).fill_(1.0), requires_grad=False)
                fake = Variable(Tensor(imgs.size(0), 1).fill_(0.0), requires_grad=False)

                # Configure input
                real_imgs = Variable(imgs.type(Tensor))

                # -----------------
                #  Train Generator
                # -----------------

                optimizer_G.zero_grad()

                # Sample noise as generator input
                z = Variable(Tensor(np.random.normal(0, 1, (imgs.shape[0], self.latent_dim))))

                # Generate a batch of images
                gen_imgs = self.generator(z)

                # Loss measures generator's ability to fool the discriminator
                g_loss = adversarial_loss(self.discriminator(gen_imgs), valid)

                g_loss.backward()
                optimizer_G.step()

                # ---------------------
                #  Train Discriminator
                # ---------------------

                optimizer_D.zero_grad()

                # Measure discriminator's ability to classify real from generated samples
                real_loss = adversarial_loss(self.discriminator(real_imgs), valid)
                fake_loss = adversarial_loss(self.discriminator(gen_imgs.detach()), fake)
                d_loss = (real_loss + fake_loss) / 2

                d_loss.backward()
                optimizer_D.step()

                print(
                    "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
                    % (epoch, num_rounds, i, len(dataloader), d_loss.item(), g_loss.item())
                )

                # batches_done = epoch * len(dataloader) + i
                # if batches_done % opt.sample_interval == 0:
                #     save_image(gen_imgs.data[:25], "images/%d.png" % batches_done, nrow=5, normalize=True)

    def predict(self, batch_size, cuda=False):
        Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
        z = Variable(Tensor(np.random.normal(0, 1, (batch_size, self.latent_dim))))
        print('1'*100)
        gen_imgs = self.generator(z)
        print('2'*100)
        return gen_imgs.detach().numpy()


if __name__ == '__main__':
    data = np.random.rand(64, 32, 32, 3)
    model = Gan((32, 32, 3), 100)
    model.train(1, 0.1, 32, data)
    s = model.predict(32)
    print(s)
    print(s.shape)
