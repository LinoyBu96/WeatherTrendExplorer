import requests
from dotenv import load_dotenv
import os
import typing
import logging

logging.basicConfig(level=logging.ERROR)


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()


def get_env_variable(var_name, default=None):
    """Get the environment variable or return an exception."""
    try:
        return os.getenv(var_name, default)
    except KeyError:
        logging.error(f"Environment variable {var_name} not found.")
        raise


def handle_IMS_API_request(url: str, err_msg: str):
    api_key = get_env_variable("IMS_API_KEY")
    response = requests.get(url, headers={"Authorization" : f"ApiToken {api_key}"})
    
    if response.status_code != 200:
        print(err_msg)
        print(f"Received status code {response.status_code}.")
        logging.error(err_msg)
        logging.error(f"Received status code {response.status_code}.")
        raise
    if 'application/json' not in response.headers.get('Content-Type', ''):
            content_type = response.headers.get('Content-Type')
            print(f"Unexpected content type: {content_type}")
            logging.error(f"Unexpected content type: {content_type}")
            raise
    return response


def get_location_data_from_openweathermap(location_name: str) -> typing.Dict:
    """_summary_

    Args:
        location_name (str): City name, state code (only for the US) and country code divided by comma.
        Please use ISO 3166 country codes.

    Returns:
        typing.Dict: Returns a dict of location name, latitude, longitude, and country of the given location,
        according to 'openweathermap' api. 
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": location_name,
        "appid": get_env_variable("OPENWEATHERMAP_API_KEY"),
        "limit": "1"}  # TODO: Change limit.
    response = requests.get(url, params)
    
    if response.status_code != 200:
        logging.error(f"Could not fetch data for location: {location_name}, received status code {response.status_code}.")
        raise
    data = response.json()[0]  # Limited to one object/location.
    # del data["local_names"]
    return data