# This script creates DICOM SRs from DICOM files with model results,
# saves them, and uploads the files to Orthanc using the REST API.


import os
import requests
import pydicom
from pydicom.sr.codedict import codes
import highdicom as hd
import json


ORTHANC_URL = "http://localhost:8042/instances"     # Orthanc endpoint
OUTPUT_DIR = "./results"                            # Directory with DICOM files
RESULTS = "./results/results_torchxrayvision.json"  # JSON file with model results
USER = "leticia"                                    # Orthanc user
PASSWORD = "123456"                                 # Orthanc password


def create_SR(dcm:pydicom.dataset.FileDataset, result:dict) -> hd.sr.ComprehensiveSR:
    """
    Uses the highdicom library to create the SR document. Implements the TID1500
    Measurement Report template, which provides a standardized way to store
    general measurements and evaluations from images or image regions.
    Reference: https://highdicom.readthedocs.io/en/latest/tid1500.html

    Args:
        dcm (pydicom.dataset.FileDataset): DICOM dataset.
        result (dict): dictionary with the prediction results.

    Returns:
        hd.sr.ComprehensiveSR: SR document.
    """
    # List to store measurements
    measurements = []

    # Creating a Measurement instance for each measurement
    for key, value in result.items():
        if key == "file_path":  # Skip the file_path key
            continue

        # Creating a Coded Concept for the measurement
        measurement_code = hd.sr.CodedConcept(
            value="%",
            meaning=key,
            scheme_designator="UCUM"  # Custom
        )

        # Creating a Measurement instance
        measurement = hd.sr.Measurement(
            name=measurement_code,
            value=float(value),
            unit=codes.UCUM.NoUnits,  # No unit
        )
        measurements.append(measurement)

    # A tracking identifier for this measurement group
    im_tracking_id = hd.sr.TrackingIdentifier(
        identifier="Predictions"+str(dcm.InstanceNumber),
        uid=hd.UID(),
    )

    # Constructing the measurement group
    measurement_group = hd.sr.MeasurementsAndQualitativeEvaluations(
        tracking_identifier=im_tracking_id,
        measurements=measurements,
    )

    # Information about the observer
    observer_person_context = hd.sr.ObserverContext(
        observer_type=codes.DCM.Person,
        observer_identifying_attributes=hd.sr.PersonObserverIdentifyingAttributes(name="observer")
    )
    observer_device_context = hd.sr.ObserverContext(
        observer_type=codes.DCM.Device,
        observer_identifying_attributes=hd.sr.DeviceObserverIdentifyingAttributes(uid=hd.UID())
    )

    observation_context = hd.sr.ObservationContext(
        observer_person_context=observer_person_context,
        observer_device_context=observer_device_context,
    )

    # Defining the measurement report
    measurement_report = hd.sr.MeasurementReport(
        observation_context=observation_context,
        procedure_reported=codes.LN.CTUnspecifiedBodyRegion,
        imaging_measurements=[measurement_group],
        title=codes.DCM.ImagingMeasurementReport,
    )

    # Filling in some missing attributes
    # (these are required for the SR to be valid, according to the SR template)
    if not hasattr(dcm, "PatientBirthDate"):
        dcm.PatientBirthDate = ""
    if not hasattr(dcm, "PatientSex"):
        dcm.PatientSex = ""
    if not hasattr(dcm, "StudyTime"):
        dcm.StudyTime = ""
    if not hasattr(dcm, "StudyID"):
        dcm.StudyID = dcm.PatientID

    # Creating the Structured Report instance
    sr_dataset = hd.sr.ComprehensiveSR(
        evidence=[dcm], # each dataset referenced in the SR must be part of the same study
        content=measurement_report,
        series_instance_uid=hd.UID(),
        series_number=dcm.SeriesNumber,
        sop_instance_uid=dcm.SOPInstanceUID,
        instance_number=dcm.InstanceNumber
    )
    return sr_dataset


def upload_file(file_path: str, user: str, password: str):
    """
    Uploads a sigle DICOM file to Orthanc through the REST API.

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
    # Loading the JSON file with the results
    with open(RESULTS, "r") as f:
        results = json.load(f)

    # Iterating over the results
    for result in results:
        dcm_path = result["file_path"]
        dcm_filename = os.path.splitext(os.path.basename(dcm_path))[0]
        dcm = pydicom.dcmread(dcm_path)
        # Create the SR document
        sr = create_SR(dcm, result)
        # Save the SR file
        sr_filename = dcm_filename + "_SR.dcm"
        sr_path = os.path.join(OUTPUT_DIR, sr_filename)
        sr.save_as(sr_path)
        print(f"{sr_filename} successfully saved!")
        # Send the SR file to Orthanc
        upload_file(sr_path, USER, PASSWORD)


if __name__ == "__main__":
    main()