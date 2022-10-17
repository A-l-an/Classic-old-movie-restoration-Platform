import argparse
import os
import cv2
import numpy as np
import torch
import time
import config
from imgproc import tensor2image, image2tensor
from model import CARN


def main(args):
    # Initialize the model
    model = CARN(config.upscale_factor)
    model = model.to(memory_format=torch.channels_last, device=config.device)
    print("Build CARN model successfully.")

    # Load the SRGAN model weights
    checkpoint = torch.load(args.weights_path, map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint["state_dict"])
    print(f"Load CARN model weights `{args.weights_path}` successfully.")

    # Start the verification mode of the model.
    model.eval()
    path = './input'            # input path
    path_list = os.listdir(path)

    for i in range(len(path_list)):
        lr_image = path + '/' + path_list[i]
        # print("Input:",lr_image)

        # Read LR image and HR image
        lr_image = cv2.imread(lr_image, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0

        # Convert BGR channel image format data to RGB channel image format data
        lr_image = cv2.cvtColor(lr_image, cv2.COLOR_BGR2RGB)

        # Convert RGB channel image format data to Tensor channel image format data
        lr_tensor = image2tensor(lr_image, False, False).unsqueeze_(0)

        # Transfer Tensor channel image format data to CUDA device
        lr_tensor = lr_tensor.to(device=config.device, memory_format=torch.channels_last, non_blocking=True)
        start_t = time.time()

        # Use the model to generate super-resolved images
        with torch.no_grad():
            sr_tensor = model(lr_tensor)
        print("model runtime: {:.3f}".format(time.time() - start_t))

        # Save image
        sr_image = tensor2image(sr_tensor, False, False)
        sr_image = cv2.cvtColor(sr_image, cv2.COLOR_RGB2BGR)

        outpath = './output/out' + str(i + 1) + '.png'

        cv2.imwrite(outpath, sr_image)

        print(f"SR image save to `{outpath}`\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Using the CARN model generator super-resolution images.")
    # parser.add_argument("--weights_path", default="./models/pretrained_models/CARN_x2.pth.tar", type=str)
    parser.add_argument("--weights_path", default="./models/pretrained_models/CARN_x4.pth.tar",type=str)
    args = parser.parse_args()

    main(args)
