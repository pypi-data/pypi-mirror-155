import torch 
import os 
import torchvision.transforms as transforms 
from torch import nn  
import cv2  
from models.mobilenetv3 import mobilenetv3_large, mobilenetv3_small    
import time
import numpy as np 
from tqdm import tqdm
import argparse


dataTransform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(100),
        transforms.ToTensor()
        ])

def prediction_rid(model, Img, device="cuda"): 
    labels = ['Nature', 'Recaptured']
    numClasses = 2
    t_pp_1 = time.time()
    img = np.array(Img)
    image = dataTransform(img )
    image  = image.unsqueeze(0).to(device)
    t_pp_2 = time.time() - t_pp_1
#    print("RID preprocess time: ", t_pp_2, "#"*90)
    outputs = model ( image )
    m = nn.Softmax(dim=1)
    output = m( outputs )
    _, predicted = torch.max( output.data ,1 )
    predict = labels[predicted]
    acc = output.data[0][predicted] 
#    print("RID Prediction time: ", time.time() - t_pp_2, "#"*90)
    return predict
    
def RID_detection(device, model_path):
    t_init_1 = time.time()
#    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model= mobilenetv3_small(num_classes=2).to(device)
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    model.eval()
#    print("Initialize RID model: ", time.time() - t_init_1, "#"*90)

    return model

