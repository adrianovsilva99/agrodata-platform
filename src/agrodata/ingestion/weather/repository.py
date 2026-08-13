from psycopg.types.json import Jsonb

from agrodata.database.connection import get_connection

import hashlib
import json


def save_raw_response(
    latitude,
    longitude,
    start_date,
    end_date,
    parameters,
    payload,
):

    request_content = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "parameters": sorted(parameters),
    }

    request_hash = hashlib.sha256(
        json.dumps(
            request_content,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    data_content = payload["properties"]["parameter"]
    data_hash = hashlib.sha256(
        json.dumps(
            data_content,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    sql = """
        INSERT INTO raw.nasa_power_api_response (
            latitude,
            longitude,
            start_date,
            end_date,
            requested_parameters,
            request_hash,
            data_hash,
            payload
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING id;
    """

    requested_parameters = ",".join(parameters)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    latitude,
                    longitude,
                    start_date,
                    end_date,
                    requested_parameters,
                    request_hash,
                    data_hash,
                    Jsonb(payload),
                ),
            )

            inserted_id = cursor.fetchone()[0]

    return inserted_id