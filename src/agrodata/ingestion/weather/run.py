from agrodata.ingestion.weather.client import fetch_daily_weather
from agrodata.ingestion.weather.repository import save_raw_response
from agrodata.ingestion.weather.parser import parse_daily_weather
from agrodata.ingestion.weather.staging_repository import upsert_weather_daily
from datetime import date, timedelta
from agrodata.ingestion.weather.staging_repository import (
    get_latest_observation_date,
    upsert_weather_daily,
)


PARAMETERS = [
    "T2M",
    "T2M_MIN",
    "T2M_MAX",
    "PRECTOTCORR",
    "RH2M",
    "WS10M",
]

IBGE_CODE = "5206206"
LOCATION_NAME = "Cristalina"
STATE_CODE = "GO"

LATITUDE = -16.77
LONGITUDE = -47.60

SOURCE = "NASA_POWER"

MAX_BATCH_DAYS = 30
DATA_LATENCY_DAYS = 3

def run():
    latest_date = get_latest_observation_date(
        ibge_code=IBGE_CODE,
        source=SOURCE,
    )

    if latest_date:
        start_date = latest_date + timedelta(days=1)
    else:
        start_date = INITIAL_DATE

    target_end_date = date.today() - timedelta(
        days=DATA_LATENCY_DAYS
    )

    if start_date > target_end_date:
        print("No new weather data to ingest.")
        return

    batch_end_date = min(
        start_date + timedelta(days=MAX_BATCH_DAYS - 1),
        target_end_date,
    )

    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = batch_end_date.strftime("%Y%m%d")

    payload = fetch_daily_weather(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        start_date=start_date_str,
        end_date=end_date_str,
        parameters=PARAMETERS,
    )

    inserted_id = save_raw_response(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        start_date=start_date_str,
        end_date=end_date_str,
        parameters=PARAMETERS,
        payload=payload,
    )

    records = parse_daily_weather(payload)

    upsert_weather_daily(
        records=records,
        ibge_code=IBGE_CODE,
        location_name=LOCATION_NAME,
        state_code=STATE_CODE,
        latitude=LATITUDE,
        longitude=LONGITUDE,
        source=SOURCE,
        raw_response_id=inserted_id,
    )

    print(
        f"NASA POWER ingestion completed successfully. "
        f"Period: {start_date} to {batch_end_date} | "
        f"RAW ID: {inserted_id} | "
        f"STAGING records: {len(records)}"
    )


if __name__ == "__main__":
    run()