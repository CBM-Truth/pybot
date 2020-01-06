from PIL import Image
import numpy as np
import torch
import torchvision.transforms as T
import tqdm
import os

IMAGE_DIR = './images'

TRANSFORM = T.Compose([
    T.RandomResizedCrop(64, scale=(0.08, 1.0),
     ratio=(0.75, 1.3333333333333333), interpolation=2),
])


def transform(x):
    return TRANSFORM(x)


def load_data(dir_=IMAGE_DIR):
    data = []
    files = os.listdir(dir_)
    for idx in tqdm.tqdm(range(len(files))):
        filename = files[idx]
        ext = filename.split('.')[-1]
        if ext not in ['jpg', 'jpeg', 'png', 'tiff']:
            continue
        image = Image.open(os.path.join(IMAGE_DIR, filename))
        image = transform(image)
        data.append(np.array(image))
    return torch.tensor(data).permute(0, 3, 1, 2).double()


def main():
    data = load_data()
    print(data)
    print(data.size())


if __name__ == '__main__':
    main()
