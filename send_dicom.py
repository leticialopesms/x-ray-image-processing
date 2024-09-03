# Este script envia arquivos DICOM para o Orthanc usando a API REST.

import os   
import requests

# Endpoint do Orthanc para envio de arquivos
ORTHANC_URL = "http://localhost:8042/instances"
# Credenciais de autenticação
ORTHANC_USERNAME = "leticia"
ORTHANC_PASSWORD = "123456"
# Diretório onde os arquivos DICOM estão armazenados
DICOM_DIR = "dicom_samples"


def send_dicom_file(file_path):
    '''
    Envia um arquivo DICOM para o Orthanc usando a API REST.
    Args:
        file_path (str): Caminho completo do arquivo DICOM.
    '''
    with open(file_path, 'rb') as dicom_file:
        # O dicionário files é usado para enviar arquivos em uma requisição HTTP
        file_name = os.path.basename(file_path)
        files = {'file': (file_name, dicom_file, 'application/dicom')}

        # Envia o arquivo DICOM para o Orthanc usando a API REST
        response = requests.post(
            ORTHANC_URL,                                # URL do Orthanc
            files=files,                                # Arquivo DICOM a ser enviado
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)   # Autenticação à requisição HTTP
        )

        # Verifica se o arquivo foi enviado com sucesso
        if response.status_code == 200:
            print(f"Arquivo {file_name} enviado com sucesso!")
        else:
            print(f"Falha ao enviar o arquivo {file_name}. Código de status: {response.status_code}")
            print("Resposta: ", response.text)


def main():
    if not os.path.exists(DICOM_DIR):
        print(f"Diretório {DICOM_DIR} não encontrado.")
        return

    for root, _, files in os.walk(DICOM_DIR):    # Percorre todos os arquivos no diretório DICOM_DIR e subdiretórios
        for file in files:
            if file.lower().endswith(".dcm"):    # Verifica se o arquivo é um DICOM
                file_path = os.path.join(root, file)
                send_dicom_file(file_path)
4

if __name__ == "__main__":
    main()