import os
import sys
import random
import itertools
import colorsys
import numpy as np

from skimage.measure import find_contours
from PIL import Image
import cv2

ROOT_DIR = os.path.abspath("../")

sys.path.append(ROOT_DIR)


# ---------------------------------------------------------#
#  Visualization
# ---------------------------------------------------------#
def random_colors(N, bright=True):

    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    return colors


def apply_mask(image, mask, color, alpha=0.5):

    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image


def display_instances(image, boxes, masks, class_ids, class_names,
                      scores=None, title="",
                      figsize=(16, 16),
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None):

    N = boxes.shape[0]

    if not N:
        print("\n*** No instances to display *** \n")

        img = Image.fromarray(np.zeros_like(image, dtype=np.uint8))
        return img
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]
        colors = colors or random_colors(N)


        masked_image = np.array(image, np.uint8)
        masked_image = np.zeros(masked_image.shape, dtype=float, order='C')
        for i in range(N):
            color = colors[i]

            mask = masks[:, :, i]
           
            if show_mask:
                masked_image = apply_mask(masked_image, mask, color)

        img = Image.fromarray(np.uint8(masked_image))#掩膜影像
    return img


