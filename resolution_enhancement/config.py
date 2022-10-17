import random

import numpy as np
import torch
from torch.backends import cudnn

# Random seed to maintain reproducible results
random.seed(0)
torch.manual_seed(0)
np.random.seed(0)
# Use GPU for training by default
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu', 0)
# Turning on when the image size does not change during training can speed up training
cudnn.benchmark = True
# When evaluating the performance of the SR model, whether to verify only the Y channel image data
only_test_y_channel = True
# Image magnification factor
upscale_factor = 4
# Current configuration parameter method
mode = "test"
# Experiment name, easy to save weights and log files
exp_name = "CARN_x4"

# if mode == "train":
#     # Dataset address
#     train_image_dir = "./data/DIV2K/CARN/train"
#     test_lr_image_dir = f"./data/Set5/LRbicx{upscale_factor}"
#     test_hr_image_dir = f"./data/Set5/GTmod12"
#
#     image_size = int(upscale_factor * 64)
#     batch_size = 64
#     num_workers = 4
#
#     # Incremental training and migration training
#     resume = ""
#
#     # Total num epochs (600,000 iters)
#     epochs = 1234
#
#     # Optimizer parameter
#     model_lr = 1e-4
#     model_betas = (0.9, 0.999)
#
#     # Dynamically adjust the learning rate policy (400,000 iters)
#     lr_scheduler_milestones = [int(epochs * 0.667)]
#     lr_scheduler_gamma = 0.5
#
#     # How many iterations to print the training result
#     print_frequency = 200

if mode == "test":
    # Test data address
    # lr_dir = f"./data/Set5/LRbicx{upscale_factor}"
    # sr_dir = f"./results/test/{exp_name}"
    # hr_dir = f"./data/Set5/GTmod12"
    lr_dir = f"./figure"
    sr_dir = f"./output"
    hr_dir = f"./hr"

    # model_path = "./models/pretrained_models/CARN_x2.pth.tar"
    model_path = "./models/pretrained_models/CARN_x4.pth.tar"
