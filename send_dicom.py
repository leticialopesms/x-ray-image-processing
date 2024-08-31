import os
import requests

# Configurações
ORTHANC_URL = "http://localhost:8042/instances" # Endpoint do Orthanc para envio de arquivos
ORTHANC_USERNAME = "orthanc"  # Usuário padrão do Orthanc
ORTHANC_PASSWORD = "orthanc"  # Senha padrão do Orthanc
DICOM_DIR = os.getcwd() + "/dicom_samples"      # Diretório onde os arquivos DICOM estão armazenados

def send_dicom_to_orthanc(file_path):
    """
    Envia um arquivo DICOM para o Orthanc usando a API REST.
    Args:
        file_path (str): Caminho completo do arquivo DICOM.
    """
    with open(file_path, 'rb') as dicom_file:
        files = {'file': (os.path.basename(file_path), dicom_file, 'application/dicom')}
        response = requests.post(
            ORTHANC_URL,
            files=files,
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)
        )
        if response.status_code == 200:
            print(f"Arquivo {file_path} enviado com sucesso!")
        else:
            print(f"Falha ao enviar o arquivo {file_path}. Código de status: {response.status_code}")
            print("Resposta:", response.text)

def main():
    # Verifica se o diretório DICOM_DIR existe
    if not os.path.exists(DICOM_DIR):
        print(f"Diretório {DICOM_DIR} não encontrado.")
        return

    # Percorre todos os arquivos no diretório DICOM_DIR
    for root, dirs, files in os.walk(DICOM_DIR):
        for file in files:
            if file.lower().endswith(".dcm"):  # Verifica se o arquivo é um DICOM
                file_path = os.path.join(root, file)
                send_dicom_to_orthanc(file_path)

if __name__ == "__main__":
    main()

