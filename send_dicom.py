import os   
import requests

# Configurações
ORTHANC_URL = "http://localhost:8042/instances" # Endpoint do Orthanc para envio de arquivos
ORTHANC_USERNAME = "orthanc"                    # Usuário padrão do Orthanc
ORTHANC_PASSWORD = "orthanc"                    # Senha padrão do Orthanc
DICOM_DIR = os.getcwd() + "/dicom_samples"      # Diretório onde os arquivos DICOM estão armazenados

def send_dicom_to_orthanc(file_path):
    """
    Envia um arquivo DICOM para o Orthanc usando a API REST.
    Args:
        file_path (str): Caminho completo do arquivo DICOM.
    """
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as dicom_file:
        # O dicionário files é usado para enviar arquivos em uma requisição HTTP
        files = {'file': (file_name, dicom_file, 'application/dicom')}
        # Enviando o arquivo DICOM para o Orthanc usando a API REST
        response = requests.post(
            ORTHANC_URL,                                # URL do Orthanc
            files=files,                                # Arquivo DICOM a ser enviado
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD)   # Autenticação básica à requisição HTTP
        )
        if response.status_code == 200:
            print(f"Arquivo {file_name} enviado com sucesso!")
        else:
            print(f"Falha ao enviar o arquivo {file_name}. Código de status: {response.status_code}")
            print("Resposta: ", response.text)

def main():
    # Verifica se o diretório DICOM_DIR existe
    if not os.path.exists(DICOM_DIR):
        print(f"Diretório {DICOM_DIR} não encontrado.")
        return

    # Percorre todos os arquivos no diretório DICOM_DIR
    for root, _, files in os.walk(DICOM_DIR):    # Percorre todos os arquivos no diretório DICOM_DIR e subdiretórios
        for file in files:
            if file.lower().endswith(".dcm"):    # Verifica se o arquivo é um DICOM
                file_path = os.path.join(root, file)
                send_dicom_to_orthanc(file_path)

if __name__ == "__main__":
    main()

