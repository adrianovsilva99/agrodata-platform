from datetime import datetime


PARAMETER_MAPPING = {
    "T2M": "temperature_avg_c",
    "T2M_MIN": "temperature_min_c",
    "T2M_MAX": "temperature_max_c",
    "PRECTOTCORR": "precipitation_mm",
    "RH2M": "relative_humidity_pct",
    "WS10M": "wind_speed_10m_ms",
}


def normalize_value(value, fill_value):
    if value == fill_value:
        return None

    return value


def parse_daily_weather(payload):
    parameter_data = payload["properties"]["parameter"]

    fill_value = payload.get("header", {}).get(
        "fill_value",
        -999,
    )

    dates = sorted(
        {
            date
            for parameter_values in parameter_data.values()
            for date in parameter_values.keys()
        }
    )

    records = []

    for raw_date in dates:
        record = {
            "date": datetime.strptime(
                raw_date,
                "%Y%m%d",
            ).date()
        }

        for nasa_parameter, field_name in PARAMETER_MAPPING.items():
            value = parameter_data.get(
                nasa_parameter,
                {},
            ).get(raw_date)

            record[field_name] = normalize_value(
                value,
                fill_value,
            )

        records.append(record)

    return records