# Este script processa um diretório de arquivos DICOM utilizando o modelo pré-treinado TorchXRayVision
# para detecção de patologias em imagens de raio-x, e salva os resultados em um arquivo JSON.

import os
import sys
import numpy as np
import argparse
from tqdm import tqdm
import pandas as pd
import torch
import torchxrayvision as xrv
import json
import torchvision, torchvision.transforms

# Configuração de argumentos de linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('dicom_dir', type=str, help='Directory with DICOM files to process')
parser.add_argument('output', type=str, help='File to write the outputs')
parser.add_argument('-weights', type=str, default="densenet121-res224-all", help='Model weights to use')
parser.add_argument('-cuda', default=False, action='store_true', help='Run on cuda (GPU)')
parser.add_argument('-resize', default=False, action='store_true', help='Resize images to 224x224')
cfg = parser.parse_args()

# Verifica se o diretório de DICOMs existe
if not os.path.isdir(cfg.dicom_dir):
    print('dicom_dir must be a directory')
    sys.exit(1)

# Carrega o modelo especificado
model = xrv.models.get_model(cfg.weights)

# Move o modelo para a GPU se disponível
if cfg.cuda:
    model = model.cuda()

# Define a transformação a ser aplicada nas imagens
if cfg.resize:
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),
                                                xrv.datasets.XRayResizer(224)])
else:
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop()])

# Lista para armazenar os resultados
outputs = []

# Itera recursivamente sobre todos os arquivos em dicom_dir e subdiretórios
for root, dirs, files in os.walk(cfg.dicom_dir):
    for file in tqdm(files):
        file_path = os.path.join(root, file)
        filename = os.path.basename(file_path)

        # Processa apenas arquivos DICOM (ignora outros tipos de arquivos e diretórios)
        if file.lower().endswith('.dcm'):
            try:
                # Carrega o arquivo DICOM utilizando torchxrayvision
                # Os argumentos voi_lut e fix_monochrome são necessários para corrigir problemas relacionados ao max value image
                dicom = xrv.utils.read_xray_dcm(file_path, voi_lut=True, fix_monochrome=True)
                
                # Verifica se as imagens são arrays 2D
                if len(dicom.shape) > 2:
                    dicom = dicom[:, :, 0]
                if len(dicom.shape) < 2:
                    print("Error: dimension lower than 2 for image")

                dicom = dicom[None, :, :]   # Adiciona dimensão de cor

                dicom = transform(dicom)    # Aplica transformação

                with torch.no_grad():
                    dicom = torch.from_numpy(dicom).unsqueeze(0)  # Adiciona dimensão de batch

                    if cfg.cuda:
                        dicom = dicom.to('cuda')
                    
                    # Realiza a predição com o modelo
                    preds = model(dicom).cpu()
                    output = {pathology: float(pred) for pathology, pred in zip(xrv.datasets.default_pathologies, preds[0])}
                    output['filename'] = filename
                    outputs.append(output)

            except Exception as e:
                print(f'Error with DICOM file {filename}: {e}')

print(f'Processed {len(outputs)} DICOM files')

# Salva os resultados em um arquivo JSON
with open(cfg.output, 'w') as json_file:
    json.dump(outputs, json_file, indent=4)

# Salva os resultados em um arquivo CSV
# df = pd.DataFrame(outputs).set_index('filename')
# df.to_csv(cfg.output)