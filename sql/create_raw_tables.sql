CREATE TABLE raw.nasa_power_api_response (
    id BIGSERIAL PRIMARY KEY,

    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,

    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    requested_parameters TEXT NOT NULL,

    payload JSONB NOT NULL,

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    request_hash VARCHAR(64),
    data_hash VARCHAR(64)
);