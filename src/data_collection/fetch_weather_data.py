from utils import handle_IMS_API_request, load_env
from pandas import json_normalize 
import pandas as pd

load_env()


def fetch_IMS_station_metadata(station_id: str = ""):
    url = f"https://api.ims.gov.il/V1/envista/stations/{station_id}"
    err_msg = f"Could not fetch metadata for station ID: {station_id}."
    response = handle_IMS_API_request(url, err_msg)
    data = response.json()
    return data
    

def fetch_IMS_region_metadata(region_id: str = ""):
    url = f"https://api.ims.gov.il/V1/envista/regions/{region_id}"
    err_msg = f"Could not fetch metadata for region ID: {region_id}."
    response = handle_IMS_API_request(url, err_msg)
    data = response.json()
    return data

def fetch_IMS_data(station_id: str, year: str, month: str):
    
    url = f"https://api.ims.gov.il/v1/envista/stations/{station_id}/data/monthly/{year}/{month}"
    err_msg = f"Could not fetch meteorological data for station ID: {station_id}, year: {year}, month: {month}."
    response = handle_IMS_API_request(url, err_msg)
    data = response.json()
    return data
