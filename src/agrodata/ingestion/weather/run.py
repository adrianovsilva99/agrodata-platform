from agrodata.ingestion.weather.client import fetch_daily_weather
from agrodata.ingestion.weather.repository import save_raw_response
from agrodata.ingestion.weather.parser import parse_daily_weather
from agrodata.ingestion.weather.staging_repository import upsert_weather_daily


PARAMETERS = [
    "T2M",
    "T2M_MIN",
    "T2M_MAX",
    "PRECTOTCORR",
    "RH2M",
    "WS10M",
]


def run():
    latitude = -16.77
    longitude = -47.60

    start_date = "20240101"
    end_date = "20240107"

    payload = fetch_daily_weather(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        parameters=PARAMETERS,
    )

    inserted_id = save_raw_response(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        parameters=PARAMETERS,
        payload=payload,
    )

    records = parse_daily_weather(payload)

    upsert_weather_daily(
        records=records,
        ibge_code="5206206",
        location_name="Cristalina",
        state_code="GO",
        latitude=latitude,
        longitude=longitude,
        source="NASA_POWER",
        raw_response_id=inserted_id,
    )

    print(
        f"NASA POWER ingestion completed successfully. "
        f"RAW ID: {inserted_id} | "
        f"STAGING records: {len(records)}"
    )


if __name__ == "__main__":
    run()