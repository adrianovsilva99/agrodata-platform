from agrodata.database.connection import get_connection


def upsert_weather_daily(
    records,
    ibge_code,
    location_name,
    state_code,
    latitude,
    longitude,
    source,
    raw_response_id,
):
    sql = """
        INSERT INTO staging.weather_daily (
            ibge_code,
            location_name,
            state_code,
            latitude,
            longitude,
            observation_date,
            temperature_avg_c,
            temperature_min_c,
            temperature_max_c,
            precipitation_mm,
            relative_humidity_pct,
            wind_speed_10m_ms,
            source,
            raw_response_id
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (
            ibge_code,
            observation_date,
            source
        )
        DO UPDATE SET
            location_name = EXCLUDED.location_name,
            state_code = EXCLUDED.state_code,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            temperature_avg_c = EXCLUDED.temperature_avg_c,
            temperature_min_c = EXCLUDED.temperature_min_c,
            temperature_max_c = EXCLUDED.temperature_max_c,
            precipitation_mm = EXCLUDED.precipitation_mm,
            relative_humidity_pct = EXCLUDED.relative_humidity_pct,
            wind_speed_10m_ms = EXCLUDED.wind_speed_10m_ms,
            raw_response_id = EXCLUDED.raw_response_id,
            updated_at = NOW();
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    sql,
                    (
                        ibge_code,
                        location_name,
                        state_code,
                        latitude,
                        longitude,
                        record["date"],
                        record["temperature_avg_c"],
                        record["temperature_min_c"],
                        record["temperature_max_c"],
                        record["precipitation_mm"],
                        record["relative_humidity_pct"],
                        record["wind_speed_10m_ms"],
                        source,
                        raw_response_id,
                    ),
                )

def get_latest_observation_date(
    ibge_code,
    source,
):
    sql = """
        SELECT MAX(observation_date)
        FROM staging.weather_daily
        WHERE ibge_code = %s
          AND source = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    ibge_code,
                    source,
                ),
            )

            result = cursor.fetchone()

    return result[0]