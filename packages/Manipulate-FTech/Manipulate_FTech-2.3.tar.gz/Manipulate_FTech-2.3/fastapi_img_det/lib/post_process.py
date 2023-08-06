import numpy as np
import cv2
import torch
from torch.nn import functional as F


def post_process_img(pred, size):
    pred = F.upsample(input=pred, size=(size[-2], size[-1]), mode='bilinear')
    pred = torch.squeeze(pred, 0)
    pred = F.softmax(pred, dim=0)[1]
    pred = pred.cpu().numpy()
    pred = (pred * 255).astype(np.uint8)

    return pred

def check_aligned_result(align_result, seg_threshold):
#    if len(align_result) == 0:
#        print(">> Detection nothing on image", image_path)
#        return None, None, None, None

    # Get layout
    image_type, (align_image, align_pred) = align_result[0]
    align_image = cv2.cvtColor(align_image, cv2.COLOR_BGR2RGB)
    binary = np.where(align_pred / 255 > seg_threshold, 1, 0).astype(np.uint8)

    return image_type, align_image, binary, align_pred 
