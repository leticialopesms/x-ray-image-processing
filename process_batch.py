#!/usr/bin/env python
# coding: utf-8

import os
import sys
import numpy as np
import argparse
from tqdm import tqdm
import pandas as pd
import torch
import torchxrayvision as xrv
import torchvision, torchvision.transforms

parser = argparse.ArgumentParser()
parser.add_argument('dicom_dir', type=str, help='Directory with DICOMs to process')
parser.add_argument('output_csv', type=str, help='CSV file to write the outputs')
parser.add_argument('-weights', type=str,default="densenet121-res224-all")
parser.add_argument('-cuda', default=False, action='store_true', help='Run on cuda')
parser.add_argument('-resize', default=False, action='store_true', help='Resize images to 224x224')
cfg = parser.parse_args()

if not os.path.isdir(cfg.dicom_dir):
    print('dicom_dir must be a directory')
    sys.exit(1)

model = xrv.models.get_model(cfg.weights)

# Move model to GPU if available
if cfg.cuda:
    model = model.cuda()

# the models will resize the input to the correct size so this is optional
if cfg.resize:
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),
                                                xrv.datasets.XRayResizer(224)])
else:
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop()])

outputs = []
for file in tqdm(os.listdir(cfg.dicom_dir)):
    dicom_path = os.path.join(cfg.dicom_dir, file)
    filename = os.path.basename(dicom_path)
    try:
        # Leitura do arquivo DICOM
        dicom = xrv.utils.read_xray_dcm(dicom_path, voi_lut=True, fix_monochrome=True)

        # Check that images are 2D arrays
        if len(dicom.shape) > 2:
            dicom = dicom[:, :, 0]
        if len(dicom.shape) < 2:
            print("error, dimension lower than 2 for image")

        # Add color channel
        dicom = dicom[None, :, :]

        dicom = transform(dicom)

        output = {}
        with torch.no_grad():
            dicom = torch.from_numpy(dicom).unsqueeze(0)
            
            if cfg.cuda:
                dicom = dicom.to('cuda')
            preds = model(dicom).cpu()
            # output = dict(zip(xrv.datasets.default_pathologies,preds[0]))
            output = {pathology: float(pred) for pathology, pred in zip(xrv.datasets.default_pathologies, preds[0])}
            output['filename'] = filename
            outputs.append(output)

    except Exception as e:
        print(f'Error with {filename}: {e}')
        
df = pd.DataFrame(outputs).set_index('filename')
df.to_csv(cfg.output_csv)