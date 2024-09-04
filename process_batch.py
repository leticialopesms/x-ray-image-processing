# Este script processa um diretório de arquivos DICOM utilizando o modelo pré-treinado TorchXRayVision
# para detecção de patologias em imagens de raio-x, e salva os resultados em um arquivo JSON.

# No terminal: python3 process_batch.py dicom_samples resultados_torchxrayvision.json -resize


import os
import argparse
from tqdm import tqdm
import pandas as pd
import torch, torchvision
import torchxrayvision as xrv
import json


# Configuração de argumentos de linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('dicom_dir', type=str, help='Directory with DICOM files to process')
parser.add_argument('output', type=str, help='File to write the outputs')
parser.add_argument('-weights', type=str, default="densenet121-res224-all", help='Model weights to use')
parser.add_argument('-cuda', default=False, action='store_true', help='Run on cuda (GPU)')
parser.add_argument('-resize', default=False, action='store_true', help='Resize images to 224x224')


def process_dicom_files(file_path:str, cfg: argparse.Namespace) -> dict:
    '''
    Processa um arquivo DICOM utilizando o modelo pré-treinado da biblioteca
    TorchXRayVision para detecção de patologias em imagens de raio-x.
    Args:
        file_path (str): Caminho completo do arquivo DICOM.
        cfg (argparse.Namespace): Configuração de argumentos de linha de comando.
    Returns:
        result(dict): Dicionário com os resultados da predição.
    '''
    model = xrv.models.get_model(cfg.weights)   # Carrega o modelo especificado

    if cfg.cuda:
        model = model.cuda()    # Move o modelo para a GPU

    try:
        # Carrega o arquivo DICOM utilizando torchxrayvision.
        # Os argumentos voi_lut e fix_monochrome são necessários para corrigir problemas
        # relacionados ao max value image.
        dicom = xrv.utils.read_xray_dcm(file_path, voi_lut=True, fix_monochrome=True)
        
        # Verifica se as imagens são arrays 2D
        if len(dicom.shape) > 2:
            dicom = dicom[:, :, 0]
        if len(dicom.shape) < 2:
            print("Error: dimension lower than 2 for image")
            result = {'Error': 'dimension lower than 2 for image', 'file_path': file_path}
            return

        dicom = dicom[None, :, :]   # Adiciona dimensão de cor

        # Define a transformação a ser aplicada nas imagens
        if cfg.resize:
            transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),
                                                        xrv.datasets.XRayResizer(224)])
        else:
            transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop()])

        dicom = transform(dicom)    # Aplica transformação

        with torch.no_grad():
            dicom = torch.from_numpy(dicom).unsqueeze(0)    # Aplica nova dimensão ao tensor

            if cfg.cuda:
                dicom = dicom.to('cuda')

            # Realiza a predição com o modelo
            preds = model(dicom).cpu().numpy()
            result = {pathology: float(pred) for pathology, pred in zip(model.pathologies, preds[0])}
            result['file_path'] = file_path

    except Exception as e:
        print(f'Error with DICOM file {file_path}: {e}')
        result = {'Error': str(e), 'file_path': file_path}

    return result


def main():
    cfg = parser.parse_args()

    if not os.path.isdir(cfg.dicom_dir):
        print('Error: dicom_dir must be a directory.')
        return

    # Lista para armazenar os resultados
    outputs = []

    # Itera sobre todos os arquivos em dicom_dir e subdiretórios
    for root, _, files in os.walk(cfg.dicom_dir):
        for file in tqdm(files):
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                outputs.append(process_dicom_files(file_path, cfg))

    print(f'Processed {len(outputs)} DICOM files')

    # Salva os resultados em um arquivo JSON
    with open(cfg.output, 'w') as json_file:
        json.dump(outputs, json_file, indent=4)

    # Salva os resultados em um arquivo CSV
    # df = pd.DataFrame(outputs).set_index('filename')
    # df.to_csv(cfg.output)


if __name__ == "__main__":
    main()