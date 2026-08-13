import requests


BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"


def fetch_daily_weather(
    latitude,
    longitude,
    start_date,
    end_date,
    parameters,
):
    request_parameters = {
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "parameters": ",".join(parameters),
        "format": "JSON",
        "time-standard": "UTC",
    }

    response = requests.get(
        BASE_URL,
        params=request_parameters,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    parameters = [
        "T2M",
        "T2M_MIN",
        "T2M_MAX",
        "PRECTOTCORR",
        "RH2M",
        "WS10M",
    ]

    weather_data = fetch_daily_weather(
        latitude=-16.77,
        longitude=-47.60,
        start_date="20240101",
        end_date="20240107",
        parameters=parameters,
    )

    returned_parameters = weather_data["properties"]["parameter"].keys()

    print("Parameters returned by NASA POWER:")
    print(list(returned_parameters))