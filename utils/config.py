
import numpy as np

class Config(object):

    NAME = None 


    GPU_COUNT = 1


    IMAGES_PER_GPU = 2


    STEPS_PER_EPOCH = 1000


    VALIDATION_STEPS = 50

    COMPUTE_BACKBONE_SHAPE = None


    BACKBONE_STRIDES = [4, 8, 16, 32, 64]


    FPN_CLASSIF_FC_LAYERS_SIZE = 1024


    TOP_DOWN_PYRAMID_SIZE = 256


    NUM_CLASSES = 1


    RPN_ANCHOR_SCALES = (32, 64, 128, 256, 512)

    RPN_ANCHOR_RATIOS = [0.5, 1, 2]


    RPN_ANCHOR_STRIDE = 1


    RPN_NMS_THRESHOLD = 0.7


    RPN_TRAIN_ANCHORS_PER_IMAGE = 256


    PRE_NMS_LIMIT = 6000


    POST_NMS_ROIS_TRAINING = 2000
    POST_NMS_ROIS_INFERENCE = 1000


    USE_MINI_MASK = True
    MINI_MASK_SHAPE = (56, 56)  # (height, width)

    BACKBONE = "resnet101"

    IMAGE_RESIZE_MODE = "square"
    IMAGE_MIN_DIM = 800
    IMAGE_MAX_DIM = 1024

    IMAGE_MIN_SCALE = 0
    # RGB = 3, grayscale = 1, RGB-D = 4
    IMAGE_CHANNEL_COUNT = 3

    # Image mean (RGB)
    MEAN_PIXEL = np.array([123.7, 116.8, 103.9])


    TRAIN_ROIS_PER_IMAGE = 200


    ROI_POSITIVE_RATIO = 0.33


    POOL_SIZE = 7
    MASK_POOL_SIZE = 14

    # Mask
    MASK_SHAPE = [28, 28]

    MAX_GT_INSTANCES = 100


    RPN_BBOX_STD_DEV = np.array([0.1, 0.1, 0.2, 0.2])
    BBOX_STD_DEV = np.array([0.1, 0.1, 0.2, 0.2])

    DETECTION_MAX_INSTANCES = 100


    DETECTION_MIN_CONFIDENCE = 0.7


    DETECTION_NMS_THRESHOLD = 0.3

    WEIGHT_DECAY = 0.0001


    LOSS_WEIGHTS = {
        "rpn_class_loss": 1.,
        "rpn_bbox_loss": 1.,
        "mrcnn_class_loss": 1.,
        "mrcnn_bbox_loss": 1.,
        "mrcnn_mask_loss": 1.
    }


    USE_RPN_ROIS = True


    TRAIN_BN = False 

    GRADIENT_CLIP_NORM = 5.0

    def __init__(self):
        
        self.BATCH_SIZE = self.IMAGES_PER_GPU * self.GPU_COUNT

        if self.IMAGE_RESIZE_MODE == "crop":
            self.IMAGE_SHAPE = np.array([self.IMAGE_MIN_DIM, self.IMAGE_MIN_DIM,
                self.IMAGE_CHANNEL_COUNT])
        else:
            self.IMAGE_SHAPE = np.array([self.IMAGE_MAX_DIM, self.IMAGE_MAX_DIM,
                self.IMAGE_CHANNEL_COUNT])

        self.IMAGE_META_SIZE = 1 + 3 + 3 + 4 + 1 + self.NUM_CLASSES

    def display(self):
        print("\nConfigurations:")
        for a in dir(self):
            if not a.startswith("__") and not callable(getattr(self, a)):
                print("{:30} {}".format(a, getattr(self, a)))
        print("\n")
