import pandas as pd
from fetch_weather_data import fetch_IMS_region_metadata, fetch_IMS_station_metadata


def process_regions(data):
    df = pd.json_normalize(data)
    df.set_index("regionId", inplace=True)

    # Remove regions without stations
    df = df[df["stations"].apply(lambda x: len(x) != 0)]

    # Remove region 0 - only NAZARET which appears in a different location
    df.drop(index=0, inplace=True)

    # Drop 'stations' column
    df.drop(columns=['stations'], errors='ignore', inplace=True)
    
    return df


def process_full_region_table(data):
    df = pd.json_normalize(data,
                           "stations",
                           ["regionId"],
                           meta_prefix="_")
    return df

def create_channels_df(monitors_df):
    # There is on
    rain_degC = monitors_df.loc[(monitors_df["name"] == "Rain") & (monitors_df["units"] == "degC")]
    df = monitors_df[["name", "units"]].drop_duplicates()
    df.loc[(df["name"] == "Rain") & (df["units"] == "degC"), "name"] = "Rain_degC"
    df.set_index("name", verify_integrity=True, inplace=True)
    df.drop("Id", inplace=True)
    return

def process_stations(data):
    # Create table of channel names and units
    monitors_df = pd.json_normalize(data,record_path=["monitors"], meta="stationId")
    channels_df = create_channels_df(monitors_df)

    # Create table of stations metadata
    stations_df = pd.json_normalize(data)
    stations_df.drop(columns=["stationsTag", "monitors", "StationTarget"], inplace=True)
    stations_df.set_index("stationId", inplace=True)

    # Filter stations that get measurements every 10 mins only.
    stations_df = stations_df[stations_df["timebase"] == 10]
    stations_df.drop(columns=["timebase"], inplace=True)

    return stations_df, channels_df


if __name__ == "__main__":
    region_metadata = fetch_IMS_region_metadata()
    region_df = process_regions(region_metadata)
    
    # full_region_df = process_full_region_table(region_metadata)

    station_metadata = fetch_IMS_station_metadata()
    process_stations(station_metadata)