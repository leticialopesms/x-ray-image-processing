# This script processes DICOM files using the pre-trained TorchXRayVision model
# for pathology detection in X-ray images, then saves the results in a JSON file.


import os
import json
import torch, torchvision
import torchxrayvision as xrv
from read_xray_dicom import read_xray_dcm


DICOM_DIR = "./dicom_samples"                       # Directory with DICOM files
OUTPUT = "./results/results_torchxrayvision.json"   # Output file


def process_dcm(file_path:str) -> dict:
    """
    Processes a dicom file using the pre-trained model from the TorchXRayVision library.
    Reference: https://github.com/mlmed/torchxrayvision

    Args:
        file_path (str): path to the dicom file.

    Returns:
        result(dict): dictionary with the prediction results.
    """
    # Preparing the DICOM file:
    dcm = read_xray_dcm(file_path)
    # or
    # dcm = xrv.utils.read_xray_dcm(file_path, voi_lut=True, fix_monochrome=True)
    
    dcm = dcm[None, ...] # Make single color channel

    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])
    dcm = transform(dcm)

    dcm = torch.from_numpy(dcm)

    # Loading model and process image
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    outputs = model(dcm[None,...]) 

    # Creating a dictionary with the results
    result = {pathology: float(pred) for pathology, pred in zip(model.pathologies, outputs[0])}
    result["file_path"] = file_path
    print(f"Processed {os.path.basename(file_path)}")
    return result


def main():
    results = []

    # Iterating over all files in DICOM_DIR and subdirectories
    for root, _, files in os.walk(DICOM_DIR):
        for file in files:
            if file.lower().endswith(".dcm"):
                file_path = os.path.join(root, file)
                results.append(process_dcm(file_path))

    print(f"Processed {len(results)} DICOM files")

    # Saving the results in a JSON file
    with open(OUTPUT, "w") as json_file:
        json.dump(results, json_file, indent=4)


if __name__ == "__main__":
    main()
