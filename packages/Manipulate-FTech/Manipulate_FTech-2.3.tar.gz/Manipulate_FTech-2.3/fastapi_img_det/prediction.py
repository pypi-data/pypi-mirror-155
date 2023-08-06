import sys, os

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './mmdetection')
if path not in sys.path:
    sys.path.insert(0, path)


from fastapi_img_det.Splicing.data.preprocess import Preprocess
import argparse
import numpy as np
from tqdm import tqdm
import time
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.nn import functional as F

from lib import models
from lib.config import config
from lib.config import update_config
from lib.utils.utils import FullModel
from mmdetection.tools.id_card_detection.infer import align_image as align_image_function
from matplotlib import pyplot as plt
from PIL import Image
import cv2

from lib.post_process import post_process_img, check_aligned_result

seg_threshold = 0.8

LAYOUT = {
      "passport": {
        "bbImg3x4": (0.054317, 0.27, 0.275067, 0.7),
        "bbText": (0.302877, 0.15, 0.975143, 0.78) ,
      },
      "blx_front": {
        "bbImg3x4": (0.054317, 0.3, 0.275067, 0.7),
        "bbText": (0.302877, 0.26, 0.975143, 0.971924) ,
      },
      "cccd_1_back": {
        "bbText": (0.307623,0.304473, 0.974887, 0.546857),
        # "bbFinger": (0.004484,0.271284, 0.252914, 0.988455),
        "bbSignature": (0.639596,0.606060, 0.862780, 0.972582),
        "bbID": (0.033183,0.020202, 0.985650, 0.230880),
        "bbTem": (0.323766,0.6666666, 0.5004484, 0.946608),
      },
      "cccd_1_front": {
        "bbImg3x4": (0.022556,0.368729, 0.325456, 0.75),
        "bbText": (0.328141,0.279264, 0.9323308, 0.9790966),
      },
      "cccd_2_back": {
        "bbText": (0.0025738, 0.017139, 0.536033, 0.1901446),
        # "bbFinger": (0.537406, 0.017139, 0.992450, 0.4542046),
        "bbSignature": (0.261105, 0.263524, 0.454939, 0.6272094),
        "bbID": (0.024269, 0.6561328, 0.964653, 0.9003745),
      },
      "cccd_2_front": {
        "bbImg3x4": (0.014268, 0.347724, 0.269092, 0.75),
        "bbText": (0.282178, 0.401983, 0.975609, 0.982497),
        # "bbQR": (0.800375, 0.052509, 0.943339, 0.266627),
      },
      "cmnd_back": {
        # "bbFinger": (0.015677, 0.015339, 0.390457, 0.974041),
        "bbText": (0.403587, 0.015677, 0.944756, 0.444248),
        "bbSignature": (0.409933, 0.477286, 0.978350, 0.974041),
      },
      "cmnd_front": {
        "bbImg3x4": (0.054317, 0.401931, 0.275067, 0.7),
        "bbText": (0.302877, 0.26, 0.975143, 0.971924) ,
       }
}

def ManipulationDetection(device, model_path):
    # model_path ="weights/CAT_full_v2.pth.tar"
    print(">> Starting load model from", model_path)
    t_model_1 = time.time()

    CUDNN_BENCHMARK = False # True if the model and input size aren't changed.
    CUDNN_DETERMINISTIC = False
    CUDNN_ENABLED = True
        ## Config ##
    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    gpus = f'({os.environ["CUDA_VISIBLE_DEVICES"]},)'
    args = argparse.Namespace(cfg='./experiments/CAT_full.yaml', opts=['TEST.FLIP_TEST', 'False', 'TEST.NUM_SAMPLES', '0', "GPUS", gpus])
    update_config(config, args)
        # cudnn related setting
    cudnn.benchmark = CUDNN_BENCHMARK
    cudnn.deterministic = CUDNN_DETERMINISTIC
    cudnn.enabled = CUDNN_ENABLED


    model = models.network_CAT.get_seg_model(config, is_init_weight=False)
    model = FullModel(model, None)
    checkpoint = torch.load(model_path)
    model.model.load_state_dict(checkpoint['state_dict'])
    model = model.to(device)
    model.eval()
#    print("Initialize model: ", time.time() - t_model_1,"#*90")
    # Preprocess
    preprocess = Preprocess()
        
    return model, preprocess
        
def prediction(model, preprocess, input_image):
     with torch.no_grad():
        pil_image = input_image.copy()
        # preprocess
        img_temp = input_image.convert('RGB').save("temp.jpg", quality=100)
        image_path = "./temp.jpg"
        image, label, qtable, size = preprocess._create_tensor(image_path, None, pil_image)
        #Prediction
        t_pred_1 = time.time()
        pred = model(image, label, qtable)
        #print("Prediction time: ", time.time() - t_pred_1, "#"*90)
        
        # Postprocess
        t_post_pr_1 = time.time()
        pred = post_process_img(pred, size)
        #print("Post Process: ", time.time() - t_post_pr_1, "#"*90)

        # Align
        t_align_1 = time.time()
        align_result = align_image_function(pil_image, pred)
        #print("Align: ",time.time() - t_align_1,"#"*90)

        if len(align_result) == 0:
            return 1

        ## Check if segment an ID document
        t_check_align_1 = time.time()
        image_type, align_image, binary, align_pred = check_aligned_result(align_result, seg_threshold)
        #print("Check align: ", time.time() - t_check_align_1, "#"*90)

        clone_binary = binary.copy()
        h = align_image.shape[0]
        w = align_image.shape[1]
        count_fake_pixel = 0
        # Loop all interested area
        for key in LAYOUT[image_type]:
            bbox = LAYOUT[image_type][key]
            # Draw bouding box to image, just for debug
            cv2.rectangle(align_image, (int(bbox[0]*w),int(bbox[1]*h)), (int(bbox[2]*w), int(bbox[3]*h)), (127,0,0), thickness=1) 
            cv2.rectangle(binary, (int(bbox[0]*w),int(bbox[1]*h)), (int(bbox[2]*w), int(bbox[3]*h)), (127,0,0), thickness=1) 
            cv2.rectangle(align_pred, (int(bbox[0]*w),int(bbox[1]*h)), (int(bbox[2]*w), int(bbox[3]*h)), (127,0,0), thickness=1) 
            # Conut fake pixel
            count_fake_pixel += np.count_nonzero(clone_binary[int(bbox[1]*h): int(bbox[3]*h), int(bbox[0]*w): int(bbox[2]*w)])
            # Ignore small if on face
            if count_fake_pixel < 0 and key == "bbImg3x4":
                count_fake_pixel = 0
                    
        # Predict
        is_real = count_fake_pixel == 0

        # Return
        return is_real
