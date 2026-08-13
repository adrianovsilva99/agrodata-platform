CREATE TABLE staging.weather_daily (
    id BIGSERIAL PRIMARY KEY,

    ibge_code VARCHAR(7) NOT NULL,
    location_name TEXT NOT NULL,
    state_code VARCHAR(2) NOT NULL,

    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,

    observation_date DATE NOT NULL,

    temperature_avg_c DOUBLE PRECISION,
    temperature_min_c DOUBLE PRECISION,
    temperature_max_c DOUBLE PRECISION,
    precipitation_mm DOUBLE PRECISION,
    relative_humidity_pct DOUBLE PRECISION,
    wind_speed_10m_ms DOUBLE PRECISION,

    source TEXT NOT NULL,

    raw_response_id BIGINT NOT NULL
        REFERENCES raw.nasa_power_api_response(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_weather_daily
        UNIQUE (ibge_code, observation_date, source)
);