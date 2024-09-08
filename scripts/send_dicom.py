# This script sends DICOM files to Orthanc using the REST API.

import os
import requests


ORTHANC_URL = "http://localhost:8042/instances" # Orthanc endpoint
DICOM_DIR = "./dicom_samples"                   # Directory with DICOM files
USER = "leticia"                                # Orthanc user
PASSWORD ="123456"                              # Orthanc password


def upload_file(file_path: str, user: str, password: str):
    """
    Uploads a sigle DICOM file to Orthanc through the REST API.
    Reference: https://book.orthanc-server.com/cookbook.html#uploading-dicom-instances

    Args:
        file_path (str): path to the dicom file.
        user (str): orthanc user.
        password (str): orthanC password.
    """
    with open(file_path, "rb") as dicom_file:
        # "files" dictionary is used to send files via HTTP request
        filename = os.path.basename(file_path)
        files = {"file": (filename, dicom_file, "application/dicom")}

        # Sending DICOM file to Orthanc using the REST API
        response = requests.post(
            ORTHANC_URL,            # URL do Orthanc
            files=files,            # Arquivo DICOM a ser enviado
            auth=(user, password)   # Autenticação à requisição HTTP
        )

        # Checking if the file was sent successfully
        if response.status_code == 200:
            print(f"{filename} successfully sent!")
        else:
            print(f"Failed to send {filename}. Status code: {response.status_code}")
            print("Response: ", response.text)


def main():
    # Iterating over all files in DICOM_DIR and subdirectories
    for root, _, files in os.walk(DICOM_DIR):
        for file in files:
            if file.lower().endswith(".dcm"):
                file_path = os.path.join(root, file)
                upload_file(file_path, USER, PASSWORD)


if __name__ == "__main__":
    main()